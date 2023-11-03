package com.example.diagnosisdemocomposition.definition;

import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.Cluster;
import com.nedap.archie.rm.datavalues.DvCodedText;
import com.nedap.archie.rm.generic.PartyProxy;
import java.util.List;
import javax.annotation.processing.Generated;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Archetype;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Entity;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Path;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.EntryEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.NullFlavour;

@Entity
@Archetype("openEHR-EHR-EVALUATION.gender.v1")
@Generated(
    value = "org.ehrbase.openehr.sdk.generator.ClassGenerator",
    date = "2023-11-03T09:40:57.020854939+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
public class GenderEvaluation implements EntryEntity {
  /**
   * Path: diagnosis-demo/Gender/Sex assigned at birth
   * Description: The sex of an individual determined by anatomical characteristics observed and registered at birth.
   * Comment: For example: 'Male', 'Female', 'Intersex'. Coding with a terminology is recommended, where possible. Use the element 'Comment' or the SLOT 'Details' if needed to register more specific details of the individuals gender.
   */
  @Path("/data[at0002]/items[at0019]/value")
  private DvCodedText sexAssignedAtBirth;

  /**
   * Path: diagnosis-demo/Gender/Tree/Sex assigned at birth/null_flavour
   */
  @Path("/data[at0002]/items[at0019]/null_flavour|defining_code")
  private NullFlavour sexAssignedAtBirthNullFlavourDefiningCode;

  /**
   * Path: diagnosis-demo/Gender/Additional details
   * Description: Additional structured details about the individuals gender.
   * Comment: Additional structured details about the gender of an individual.
   */
  @Path("/data[at0002]/items[at0023]")
  private List<Cluster> additionalDetails;

  /**
   * Path: diagnosis-demo/Gender/Extension
   * Description: Additional information required to capture local content or to align with other reference models/formalisms.
   * Comment: For example: local information requirements or additional metadata to align with FHIR equivalents.
   */
  @Path("/protocol[at0003]/items[at0005]")
  private List<Cluster> extension;

  /**
   * Path: diagnosis-demo/Gender/subject
   */
  @Path("/subject")
  private PartyProxy subject;

  /**
   * Path: diagnosis-demo/Gender/language
   */
  @Path("/language")
  private Language language;

  /**
   * Path: diagnosis-demo/Gender/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  public void setSexAssignedAtBirth(DvCodedText sexAssignedAtBirth) {
     this.sexAssignedAtBirth = sexAssignedAtBirth;
  }

  public DvCodedText getSexAssignedAtBirth() {
     return this.sexAssignedAtBirth ;
  }

  public void setSexAssignedAtBirthNullFlavourDefiningCode(
      NullFlavour sexAssignedAtBirthNullFlavourDefiningCode) {
     this.sexAssignedAtBirthNullFlavourDefiningCode = sexAssignedAtBirthNullFlavourDefiningCode;
  }

  public NullFlavour getSexAssignedAtBirthNullFlavourDefiningCode() {
     return this.sexAssignedAtBirthNullFlavourDefiningCode ;
  }

  public void setAdditionalDetails(List<Cluster> additionalDetails) {
     this.additionalDetails = additionalDetails;
  }

  public List<Cluster> getAdditionalDetails() {
     return this.additionalDetails ;
  }

  public void setExtension(List<Cluster> extension) {
     this.extension = extension;
  }

  public List<Cluster> getExtension() {
     return this.extension ;
  }

  public void setSubject(PartyProxy subject) {
     this.subject = subject;
  }

  public PartyProxy getSubject() {
     return this.subject ;
  }

  public void setLanguage(Language language) {
     this.language = language;
  }

  public Language getLanguage() {
     return this.language ;
  }

  public void setFeederAudit(FeederAudit feederAudit) {
     this.feederAudit = feederAudit;
  }

  public FeederAudit getFeederAudit() {
     return this.feederAudit ;
  }
}
