package com.example.restservice.compositions.patientcomposition.definition;

import java.lang.String;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.EnumValueSet;

public enum SexAssignedAtBirthDefiningCode implements EnumValueSet {
  INTERSEX("Intersex", "", "local_terms", "I"),

  MALE("Male", "", "local_terms", "M"),

  FEMALE("Female", "", "local_terms", "F");

  private String value;

  private String description;

  private String terminologyId;

  private String code;

  SexAssignedAtBirthDefiningCode(String value, String description, String terminologyId,
      String code) {
    this.value = value;
    this.description = description;
    this.terminologyId = terminologyId;
    this.code = code;
  }

  public String getValue() {
     return this.value ;
  }

  public String getDescription() {
     return this.description ;
  }

  public String getTerminologyId() {
     return this.terminologyId ;
  }

  public String getCode() {
     return this.code ;
  }
}
