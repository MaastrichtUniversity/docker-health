package com.medblocks.openfhir.fc.schema.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import lombok.Data;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
        "with",
        "split"
})
@Data
public class Hierarchy {

    @JsonProperty("with")
    private HierarchyWith with;

    @JsonProperty("split")
    private Split split;
}
