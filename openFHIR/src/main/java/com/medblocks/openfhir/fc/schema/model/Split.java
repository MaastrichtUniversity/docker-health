package com.medblocks.openfhir.fc.schema.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import lombok.Data;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
        "fhir",
        "openehr"
})
@Data
public class Split {

    @JsonProperty("fhir")
    private SplitModel fhir;

    @JsonProperty("openehr")
    private SplitModel openehr;
}
