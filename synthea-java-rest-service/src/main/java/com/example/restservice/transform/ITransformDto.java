package com.example.restservice.transform;

import org.ehrbase.openehr.sdk.generator.commons.interfaces.CompositionEntity;

public interface ITransformDto {

    CompositionEntity transform();

    String getTemplateId();
}
