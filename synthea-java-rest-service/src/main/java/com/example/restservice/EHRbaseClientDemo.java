package com.example.restservice;

import com.example.restservice.diagnosisdemocomposition.DiagnosisDemoComposition;
import com.example.restservice.patientcomposition.PatientComposition;
import com.example.restservice.vitalsignscomposition.VitalSignsComposition;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.client.HttpClient;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.client.HttpClientBuilder;
import org.ehrbase.openehr.sdk.client.openehrclient.OpenEhrClientConfig;
import org.ehrbase.openehr.sdk.client.openehrclient.defaultrestclient.DefaultRestClient;
import org.openehr.schemas.v1.OPERATIONALTEMPLATE;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.Optional;
import java.util.UUID;

public class EHRbaseClientDemo {
    private static final String OPEN_EHR_URL = "http://localhost:8080/ehrbase/";
    private static final String USERNAME = "user";
    private static final String PASSWORD = "foobar";

    public void interactWithEHRBaseDiagnosis(DiagnosisDemoComposition composition) throws URISyntaxException {
        CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(
                AuthScope.ANY,
                new UsernamePasswordCredentials(USERNAME, PASSWORD)
        );

        HttpClient httpClient = HttpClientBuilder.create()
                .setDefaultCredentialsProvider(credentialsProvider)
                .build();


        TemplateProviderLoader provider = new TemplateProviderLoader();

        // Setup REST client
        DefaultRestClient client = new DefaultRestClient(new OpenEhrClientConfig(new URI(OPEN_EHR_URL)),provider,httpClient);

        // Check for template otherwise upload
        Optional<OPERATIONALTEMPLATE> operationalTemplateFound =
                client.templateEndpoint().findTemplate(TemplateProviderLoader.TEMPLATE_NAME_DIAGNOSIS);

        if (operationalTemplateFound.isEmpty()){
            System.out.println("Template not found");
            client.templateEndpoint().ensureExistence(TemplateProviderLoader.TEMPLATE_NAME_DIAGNOSIS);
        }

        // Create EHR
        UUID ehr = client.ehrEndpoint().createEhr();

        System.out.println(ehr);

        // Post composition
        client.compositionEndpoint(ehr).mergeCompositionEntity(composition);

        System.out.println(composition.getVersionUid());
    }

    public void interactWithEHRBasePatient(PatientComposition composition) throws URISyntaxException {
        CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(
                AuthScope.ANY,
                new UsernamePasswordCredentials(USERNAME, PASSWORD)
        );

        HttpClient httpClient = HttpClientBuilder.create()
                .setDefaultCredentialsProvider(credentialsProvider)
                .build();


        TemplateProviderLoader provider = new TemplateProviderLoader();

        // Setup REST client
        DefaultRestClient client = new DefaultRestClient(new OpenEhrClientConfig(new URI(OPEN_EHR_URL)),provider,httpClient);

        // Check for template otherwise upload
        Optional<OPERATIONALTEMPLATE> operationalTemplateFound =
                client.templateEndpoint().findTemplate(TemplateProviderLoader.TEMPLATE_NAME_PATIENT);

        if (operationalTemplateFound.isEmpty()){
            System.out.println("Template not found");
            client.templateEndpoint().ensureExistence(TemplateProviderLoader.TEMPLATE_NAME_PATIENT);
        }

        // Create EHR
        UUID ehr = client.ehrEndpoint().createEhr();

        System.out.println(ehr);

        // Post composition
        client.compositionEndpoint(ehr).mergeCompositionEntity(composition);

        System.out.println(composition.getVersionUid());
    }


    public void interactWithEHRBaseVitalSigns(VitalSignsComposition composition) throws URISyntaxException {
        CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(
                AuthScope.ANY,
                new UsernamePasswordCredentials(USERNAME, PASSWORD)
        );

        HttpClient httpClient = HttpClientBuilder.create()
                .setDefaultCredentialsProvider(credentialsProvider)
                .build();


        TemplateProviderLoader provider = new TemplateProviderLoader();

        // Setup REST client
        DefaultRestClient client = new DefaultRestClient(new OpenEhrClientConfig(new URI(OPEN_EHR_URL)),provider,httpClient);

        // Check for template otherwise upload
        Optional<OPERATIONALTEMPLATE> operationalTemplateFound =
                client.templateEndpoint().findTemplate(TemplateProviderLoader.TEMPLATE_NAME_VITAL_SIGNS);

        if (operationalTemplateFound.isEmpty()){
            System.out.println("Template not found");
            client.templateEndpoint().ensureExistence(TemplateProviderLoader.TEMPLATE_NAME_VITAL_SIGNS);
        }

        // Create EHR
        UUID ehr = client.ehrEndpoint().createEhr();

        System.out.println(ehr);

        // Post composition
        client.compositionEndpoint(ehr).mergeCompositionEntity(composition);

        System.out.println(composition.getVersionUid());
    }

}
