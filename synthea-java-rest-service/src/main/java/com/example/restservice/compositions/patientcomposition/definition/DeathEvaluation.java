package com.example.restservice.compositions.patientcomposition.definition;

import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.Cluster;
import com.nedap.archie.rm.generic.PartyProxy;
import java.time.temporal.TemporalAccessor;
import java.util.List;
import javax.annotation.processing.Generated;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Archetype;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Entity;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Path;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.EntryEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.NullFlavour;

@Entity
@Archetype("openEHR-EHR-EVALUATION.death_summary.v1")
@Generated(
    value = "org.ehrbase.openehr.sdk.generator.ClassGenerator",
    date = "2023-11-15T13:51:36.035718595+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
public class DeathEvaluation implements EntryEntity {
  /**
   * Path: Patient/Death/Date of death
   * Description: The known, or assumed, date and time of death.
   * Comment: Partial dates and an absence of time of death are allowed, if necessary. For example: based on findings pertaining to examination of the body and the pathologist's reconstruction of time of death based on post-mortem changes, temperature, etc. May also be known as DOD (date of death). If more than one 'Date of death alternatives' have been proposed, this data element could be renamed in a template as the 'Confirmed/Agreed date of death'.
   */
  @Path("/data[at0001]/items[at0092 and name/value='Date of death']/value|value")
  private TemporalAccessor dateOfDeathValue;

  /**
   * Path: Patient/Death/Item tree/Date of death/null_flavour
   */
  @Path("/data[at0001]/items[at0092 and name/value='Date of death']/null_flavour|defining_code")
  private NullFlavour dateOfDeathNullFlavourDefiningCode;

  /**
   * Path: Patient/Death/Date of death alternatives
   * Description: Additional details about possible alternative dates of death.
   * Comment: For example: In situations where there is no authoritative single source of death, there may be potentially conflicting dates & times of death from different sources.
   */
  @Path("/data[at0001]/items[at0104]")
  private List<Cluster> dateOfDeathAlternatives;

  /**
   * Path: Patient/Death/Structured place of death
   * Description: Structured detail about the place where the individual died.
   * Comment: For example: details about a facility or institution; or a landmark or a road intersection.
   */
  @Path("/data[at0001]/items[at0100]")
  private List<Cluster> structuredPlaceOfDeath;

  /**
   * Path: Patient/Death/Additional details
   * Description: Additional structured details related to the death.
   */
  @Path("/data[at0001]/items[at0042]")
  private List<Cluster> additionalDetails;

  /**
   * Path: Patient/Death/Extension
   * Description: Additional information required to extend the model with local content or to align with other reference models/formalisms.
   * Comment: For example: local information requirements; or additional metadata to align with FHIR.
   */
  @Path("/protocol[at0009]/items[at0102]")
  private List<Cluster> extension;

  /**
   * Path: Patient/Death/subject
   */
  @Path("/subject")
  private PartyProxy subject;

  /**
   * Path: Patient/Death/language
   */
  @Path("/language")
  private Language language;

  /**
   * Path: Patient/Death/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  public void setDateOfDeathValue(TemporalAccessor dateOfDeathValue) {
     this.dateOfDeathValue = dateOfDeathValue;
  }

  public TemporalAccessor getDateOfDeathValue() {
     return this.dateOfDeathValue ;
  }

  public void setDateOfDeathNullFlavourDefiningCode(
      NullFlavour dateOfDeathNullFlavourDefiningCode) {
     this.dateOfDeathNullFlavourDefiningCode = dateOfDeathNullFlavourDefiningCode;
  }

  public NullFlavour getDateOfDeathNullFlavourDefiningCode() {
     return this.dateOfDeathNullFlavourDefiningCode ;
  }

  public void setDateOfDeathAlternatives(List<Cluster> dateOfDeathAlternatives) {
     this.dateOfDeathAlternatives = dateOfDeathAlternatives;
  }

  public List<Cluster> getDateOfDeathAlternatives() {
     return this.dateOfDeathAlternatives ;
  }

  public void setStructuredPlaceOfDeath(List<Cluster> structuredPlaceOfDeath) {
     this.structuredPlaceOfDeath = structuredPlaceOfDeath;
  }

  public List<Cluster> getStructuredPlaceOfDeath() {
     return this.structuredPlaceOfDeath ;
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
