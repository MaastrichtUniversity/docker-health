package com.medblocks.openfhir.rest;

import com.medblocks.openfhir.OpenFhirEngine;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * Controller for the openFHIR Engine; mapping from openEHR to FHIR and vice versa REST endpoints are created here
 */
@RestController
@Slf4j
@Tag(name = "DataHub API", description = "Operations related to DataHub ETL FHIR message to openEHR composition")
public class DataHubController {

    private final OpenFhirEngine openFhirEngine;

    @Autowired
    public DataHubController(final OpenFhirEngine openFhirEngine) {
        this.openFhirEngine = openFhirEngine;
    }

    /**
     * Accepts a FHIR Resource (Bundle or any other) and maps it corresponding openEHR Composition  according to the
     * state of the openFHIR
     *
     * @param fhirResource incoming FHIR Resource (Bundle or any other), R4
     * @param templateId template id is an optional parameter if you want to force a specific context mapper; if
     *         no
     *         templateId is provided, then out of all context mappers, the engine will try to find one that
     *         matches the given incoming FHIR Resource (based on context mapper context.profileUrl)
     * @param reqId request id that will be logged
     * @return openEHR Composition in either flat or canonical format, depending on "flat" argument (default is
     *         canonical)
     */
    @PostMapping(value = "/datahub/toopenehr", produces = "application/json")
    @Operation(
            summary = "Maps incoming FHIR Resource to openEHR Composition",
            description = "Maps incoming FHIR Resource to openEHR Composition according to FHIR Connect state of the engine",
            responses = {
                    @ApiResponse(responseCode = "200", description = "openEHR Composition in either flat or canonical format")
            },
            requestBody = @io.swagger.v3.oas.annotations.parameters.RequestBody(
                    description = "FHIR Resource",
                    content = {
                            @Content(mediaType = "application/json")
                    }
            )
    )
    ResponseEntity toOpenEhr(@RequestBody String fhirResource,
                             @RequestParam String templateId,
                             @RequestParam String subjectId,
                             @RequestParam String openehrNodeName,
                             @RequestHeader(value = "x-req-id", required = false) final String reqId) throws IOException, InterruptedException {
        try {

            final String openEhr = openFhirEngine.toOpenEhr(fhirResource, templateId, true);

            String url = "http://etl.%s.local.dh.unimaas.nl/post_fhir?template_id=%s&subject_id=%s".formatted(openehrNodeName, templateId, subjectId);
            HttpClient client = HttpClient.newHttpClient();
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .version(HttpClient.Version.HTTP_1_1)
                    .header("Content-Type", "application/json")
                    .header("Accept", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(openEhr))
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            String etlResponse = response.body();

            if (response.statusCode() != 200) {
                return ResponseEntity.badRequest().contentType(MediaType.APPLICATION_JSON).body(etlResponse);
            }

            return ResponseEntity.ok().contentType(MediaType.APPLICATION_JSON).body(etlResponse);
        } catch (ResponseStatusException | IllegalArgumentException e) {

            return ResponseEntity.badRequest().body(e.getMessage());
        }catch (Exception e) {

            throw e;
        }
    }
}
