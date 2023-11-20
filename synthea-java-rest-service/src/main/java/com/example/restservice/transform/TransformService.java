package com.example.restservice.transform;

import com.example.restservice.load.EHRbaseClientDemo;
import com.example.restservice.utils.TemplateProviderLoader;
import com.nedap.archie.rm.composition.Composition;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.CompositionEntity;
import org.ehrbase.openehr.sdk.serialisation.dto.GeneratedDtoToRmConverter;
import org.ehrbase.openehr.sdk.serialisation.jsonencoding.CanonicalJson;
import org.ehrbase.openehr.sdk.validation.CompositionValidator;
import org.openehr.schemas.v1.OPERATIONALTEMPLATE;

import java.net.URISyntaxException;

public class TransformService {

    ITransformDto transformDto;

    CompositionEntity compositionEntity;

    EHRbaseClientDemo clientDemo;

    public TransformService(ITransformDto transformDto) {
        this.transformDto = transformDto;
        this.clientDemo = new EHRbaseClientDemo();
    }

    public void transform() {
        this.compositionEntity = this.transformDto.transform();
    }

    public void load() throws URISyntaxException {
        this.clientDemo.interactWithEHRBase(this.compositionEntity, this.transformDto.getTemplateId());
    }

    public String convertToJson() {
        TemplateProviderLoader provider = new TemplateProviderLoader();
        GeneratedDtoToRmConverter cut = new GeneratedDtoToRmConverter(provider);
        Composition rmObject = (Composition) cut.toRMObject(this.compositionEntity);
        OPERATIONALTEMPLATE template = provider.find(this.transformDto.getTemplateId()).orElseThrow();

        // Validation
        CompositionValidator compositionValidator = new CompositionValidator();
        var result = compositionValidator.validate(rmObject, template);
        if (result.size() > 0) {
            result.forEach(System.out::println);
        } else {
            System.out.println("Composition validated successfully");
        }

        CanonicalJson json = new CanonicalJson();
        return json.marshal(rmObject);
    }

}
