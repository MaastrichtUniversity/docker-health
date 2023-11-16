package com.example.restservice;

import org.apache.xmlbeans.XmlException;
import org.ehrbase.openehr.sdk.webtemplate.templateprovider.TemplateProvider;
import org.openehr.schemas.v1.OPERATIONALTEMPLATE;
import org.openehr.schemas.v1.TemplateDocument;

import java.io.IOException;
import java.io.InputStream;
import java.util.Optional;

public class PatientTemplateProvider implements TemplateProvider {
    @Override
    public Optional<OPERATIONALTEMPLATE> find(String templateId){
        InputStream stream = getClass().getResourceAsStream("/patient.opt");
        try {
            TemplateDocument template = TemplateDocument.Factory.parse(stream);
            return Optional.ofNullable(template.getTemplate());
        } catch (XmlException | IOException e){
            System.out.println("Error Happened");
            return Optional.ofNullable(null);
        }

    }
}
