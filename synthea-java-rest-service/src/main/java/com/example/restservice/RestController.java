package com.example.restservice;

import com.example.restservice.diagnosisdemocomposition.DiagnosisDemoComposition;
import com.nedap.archie.rm.composition.Composition;
import jakarta.validation.Valid;
import org.ehrbase.openehr.sdk.serialisation.dto.GeneratedDtoToRmConverter;
import org.ehrbase.openehr.sdk.serialisation.jsonencoding.CanonicalJson;
import org.ehrbase.openehr.sdk.validation.CompositionValidator;
import org.openehr.schemas.v1.OPERATIONALTEMPLATE;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;

import java.net.URISyntaxException;

@org.springframework.web.bind.annotation.RestController
public class RestController {

    private String response;

    @PostMapping("/diagnosis-demo")
    String createNew(@Valid @RequestBody DiagnosisDemoDTO diagnosisDemoDTO) throws URISyntaxException {
        GenerateComposition generateComposition = new GenerateComposition();
        DiagnosisDemoComposition composition = generateComposition.generateComposition(diagnosisDemoDTO);
        DiagnosisTemplateProvider provider = new DiagnosisTemplateProvider();
        GeneratedDtoToRmConverter cut = new GeneratedDtoToRmConverter(provider);
        Composition rmObject = (Composition) cut.toRMObject(composition);
        OPERATIONALTEMPLATE template = provider.find("diagnosis-demo").orElseThrow();

        // Validation
        CompositionValidator compositionValidator = new CompositionValidator();
        var result = compositionValidator.validate(rmObject, template);
        if (result.size() > 0) {
            result.forEach(System.out::println);
        } else {
            System.out.println("Composition validated successfully");
        }

        // Uncomment the following lines to run the interaction
        // This will:
        //  - Post the diagnosis-demo template if not found
        //  - Create an EHR
        //  - Post the composition
//        EHRbaseClientDemo ehRbaseClientDemo = new EHRbaseClientDemo();
//        ehRbaseClientDemo.interactWithEHRBase(composition);

        CanonicalJson json = new CanonicalJson();
        return json.marshal(rmObject);
    }

    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public String handleValidationExceptions(MethodArgumentNotValidException ex) {
         var list = ex.getBindingResult().getFieldErrors().stream().map(err -> err.getDefaultMessage()).collect(java.util.stream.Collectors.joining("\n"));
         return list;
    }
}