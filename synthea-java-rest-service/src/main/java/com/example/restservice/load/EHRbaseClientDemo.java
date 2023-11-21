package com.example.restservice.load;

import com.example.restservice.utils.TemplateProviderLoader;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.client.HttpClient;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.client.HttpClientBuilder;
import org.ehrbase.openehr.sdk.client.openehrclient.OpenEhrClientConfig;
import org.ehrbase.openehr.sdk.client.openehrclient.defaultrestclient.DefaultRestClient;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.CompositionEntity;
import org.openehr.schemas.v1.OPERATIONALTEMPLATE;

import java.net.URI;
import java.net.URISyntaxException;
import java.util.Optional;
import java.util.UUID;

public class EHRbaseClientDemo {
    private static final String OPEN_EHR_URL = System.getenv("EHRBASE_BASE_URL");
    private static final String USERNAME = System.getenv("EHRBASE_USERNAME");
    private static final String PASSWORD = System.getenv("EHRBASE_PASSWORD");

    public void interactWithEHRBase(CompositionEntity composition, String templateId) throws URISyntaxException {
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
        DefaultRestClient client = new DefaultRestClient(new OpenEhrClientConfig(new URI(OPEN_EHR_URL)), provider, httpClient);

        // Check for template otherwise upload
        Optional<OPERATIONALTEMPLATE> operationalTemplateFound = client.templateEndpoint().findTemplate(templateId);

        if (operationalTemplateFound.isEmpty()) {
            System.out.println("Template not found");
            client.templateEndpoint().ensureExistence(templateId);
        }

        // Create EHR
        UUID ehr = client.ehrEndpoint().createEhr();

        System.out.println(ehr);

        // Post composition
        client.compositionEndpoint(ehr).mergeCompositionEntity(composition);

        System.out.println(composition.getVersionUid());
    }
}
