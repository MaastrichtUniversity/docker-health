package com.example;

import com.example.diagnosisdemocomposition.DiagnosisDemoComposition;
import com.nedap.archie.rm.composition.Composition;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.client.HttpClient;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.client.HttpClientBuilder;
import org.ehrbase.openehr.sdk.client.openehrclient.OpenEhrClientConfig;
import org.ehrbase.openehr.sdk.client.openehrclient.defaultrestclient.DefaultRestClient;
import org.ehrbase.openehr.sdk.serialisation.dto.GeneratedDtoToRmConverter;
import org.ehrbase.openehr.sdk.serialisation.jsonencoding.CanonicalJson;
import org.ehrbase.openehr.sdk.validation.CompositionValidator;
import org.openehr.schemas.v1.OPERATIONALTEMPLATE;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.Optional;
import java.util.UUID;

public class Main {

    private static final String OPEN_EHR_URL = "http://localhost:8080/ehrbase/";
    private static final String USERNAME = "user";
    private static final String PASSWORD = "foobar";

    public static void main(String[] args) throws URISyntaxException {

        DiagnosisDemoDTO diagnosisDemoDTO = new DiagnosisDemoDTO("2011-10-18T20:29:31Z","2010-10-18T20:29:31Z","2017-10-18T20:29:31Z", "Anemia (disorder)","271737000","248153007","Male");
        GenerateComposition generateComposition = new GenerateComposition();

        DiagnosisDemoComposition composition = generateComposition.generateComposition(diagnosisDemoDTO);

        DiagnosisTemplateProvider provider = new DiagnosisTemplateProvider();
        GeneratedDtoToRmConverter cut = new GeneratedDtoToRmConverter(provider);
        Composition rmObject = (Composition) cut.toRMObject(composition);
        OPERATIONALTEMPLATE template = provider.find("diagnosis-demo").orElseThrow();


        // Validation
        CompositionValidator compositionValidator= new CompositionValidator();
        var result = compositionValidator.validate(rmObject, template);
        if (result.size() > 0){
            result.forEach(System.out::println);
        }
        else{
            System.out.println("Composition validated successfully");
        }


        // Print json
        CanonicalJson json = new CanonicalJson();
        System.out.println(json.marshal(rmObject));


        // Setup Basic Auth
        CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(
                AuthScope.ANY,
                new UsernamePasswordCredentials(USERNAME, PASSWORD)
        );

        HttpClient httpClient = HttpClientBuilder.create()
                .setDefaultCredentialsProvider(credentialsProvider)
                .build();

        // Setup REST client
        DefaultRestClient client = new DefaultRestClient(new OpenEhrClientConfig(new URI(OPEN_EHR_URL)),provider,httpClient);

        // Check for template otherwise upload
        Optional<OPERATIONALTEMPLATE> operationalTemplateFound =
                client.templateEndpoint().findTemplate("diagnosis-demo");

        if (operationalTemplateFound.isEmpty()){
            System.out.println("Template not found");
            client.templateEndpoint().ensureExistence("diagnosis-demo");
        }

        // Create EHR
        UUID ehr = client.ehrEndpoint().createEhr();

        System.out.println(ehr);

        // Post composition
        client.compositionEndpoint(ehr).mergeCompositionEntity(composition);

        System.out.println(composition.getVersionUid());


    }
}