package com.example.restservice.transform;

import com.example.restservice.load.EHRbaseClientDemo;
import com.example.restservice.utils.TemplateProviderLoader;
import com.nedap.archie.rm.composition.Composition;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.CompositionEntity;
import org.ehrbase.openehr.sdk.serialisation.dto.GeneratedDtoToRmConverter;
import org.ehrbase.openehr.sdk.serialisation.jsonencoding.CanonicalJson;
import org.ehrbase.openehr.sdk.validation.CompositionValidator;
import org.openehr.schemas.v1.OPERATIONALTEMPLATE;
import org.openehr.schemas.v1.StringDictionaryItem;

import java.net.URISyntaxException;

public class TransformService {

    ITransformDto transformDto;
    CompositionEntity compositionEntity;
    TemplateProviderLoader provider;
    OPERATIONALTEMPLATE template;
    Composition rmObject;

    public TransformService(ITransformDto transformDto) {
        this.transformDto = transformDto;
        this.provider = new TemplateProviderLoader();
        this.template = provider.find(this.transformDto.getTemplateId()).orElseThrow();
    }

    public void transform() {
        this.compositionEntity = this.transformDto.transform();
        GeneratedDtoToRmConverter converter = new GeneratedDtoToRmConverter(provider);
        this.rmObject = (Composition) converter.toRMObject(this.compositionEntity);
    }

    public void load() throws URISyntaxException {
        EHRbaseClientDemo clientDemo = new EHRbaseClientDemo();
        clientDemo.interactWithEHRBase(this.compositionEntity, this.transformDto.getTemplateId());
    }

    public String convertToJson() {
        CanonicalJson json = new CanonicalJson();
        return json.marshal(this.rmObject);
    }

    public void verifyTemplate() {
        // Verify template version
        for (StringDictionaryItem stringDictionaryItem : this.template.getDescription().getOtherDetailsArray()) {
            if (stringDictionaryItem.getId().equals("sem_ver")) {
                String sem_ver = stringDictionaryItem.getStringValue();
                System.out.println("sem_ver");
                System.out.println(sem_ver);
                if (sem_ver.equals(this.transformDto.getTemplateSemVer())) {
                    System.out.println("Template semantic version verified successfully");
                } else {
                    System.out.println(this.transformDto.getTemplateSemVer() + " doesn't match: " + sem_ver);
                }
            }
        }
    }

    public void validateComposition() {
        // Validation
        CompositionValidator compositionValidator = new CompositionValidator();
        var result = compositionValidator.validate(this.rmObject, this.template);
        if (result.size() > 0) {
            result.forEach(System.out::println);
        } else {
            System.out.println("Composition validated successfully");
        }
    }

    public String result() throws URISyntaxException {
        this.verifyTemplate();
        this.transform();
        this.validateComposition();

        this.load();

        return this.convertToJson();
    }
}
