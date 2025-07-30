
package com.medblocks.openfhir.fc.schema.model;


import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * Fhir Config
 * <p>
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
        "structureDefinition"
})

public class FhirConfig {

    /**
     * (Required)
     */
    @JsonProperty("structureDefinition")
    private String structureDefinition;

    /**
     * multiple means if multiple Resources of the same type can come out of one Composition, defaults to true
     */
    @JsonProperty("multiple")
    private Boolean multiple;

    public FhirConfig copy() {
        final FhirConfig fhirConfig = new FhirConfig();
        fhirConfig.setStructureDefinition(structureDefinition);
        fhirConfig.setMultiple(multiple);
        return fhirConfig;
    }


    /**
     * (Required)
     */
    @JsonProperty("multiple")
    public Boolean getMultiple() {
        if(multiple == null) {
            return true;
        }
        return multiple;
    }

    /**
     * (Required)
     */
    @JsonProperty("multiple")
    public void setMultiple(Boolean multiple) {
        this.multiple = multiple;
    }

    public FhirConfig withMultiple(Boolean multiple) {
        this.multiple = multiple;
        return this;
    }

    /**
     * (Required)
     */
    @JsonProperty("structureDefinition")
    public String getStructureDefinition() {
        return structureDefinition;
    }

    /**
     * (Required)
     */
    @JsonProperty("structureDefinition")
    public void setStructureDefinition(String structureDefinition) {
        this.structureDefinition = structureDefinition;
    }

    public FhirConfig withStructureDefinition(String archetype) {
        this.structureDefinition = archetype;
        return this;
    }

}
