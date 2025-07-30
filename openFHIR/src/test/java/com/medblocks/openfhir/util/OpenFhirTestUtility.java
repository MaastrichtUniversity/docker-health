package com.medblocks.openfhir.util;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLMapper;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.medblocks.openfhir.fc.schema.context.FhirConnectContext;
import java.io.InputStream;
import java.util.Map;
import org.hl7.fhir.r4.model.Bundle;
import org.junit.Assert;
import org.openehr.schemas.v1.OPERATIONALTEMPLATE;
import org.yaml.snakeyaml.DumperOptions;
import org.yaml.snakeyaml.LoaderOptions;
import org.yaml.snakeyaml.Yaml;
import org.yaml.snakeyaml.constructor.Constructor;
import org.yaml.snakeyaml.introspector.Property;
import org.yaml.snakeyaml.introspector.PropertyUtils;
import org.yaml.snakeyaml.representer.Representer;

public class OpenFhirTestUtility {

    public static ObjectMapper getYaml() {
        final YAMLMapper mapper = new YAMLMapper();
        mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL); // skip nulls
        return mapper;
    }


}
