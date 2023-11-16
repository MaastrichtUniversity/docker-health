package com.example.restservice.patientcomposition.definition;

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
@Archetype("openEHR-EHR-EVALUATION.birth_summary.v0")
@Generated(
    value = "org.ehrbase.openehr.sdk.generator.ClassGenerator",
    date = "2023-11-15T13:51:36.031988941+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
public class BirthEvaluation implements EntryEntity {
  /**
   * Path: Patient/Birth/Date of birth
   * Description: The date/time of birth of the individual.
   * Comment: May also be used to record the assumed or agreed date/time of birth for operational purposes, if the actual date/time is not formally recorded. Possible alternatives for the date/time of birth of the individual can be recorded using the CLUSTER.DOB_alternative archetype 'Date of birth details' SLOT. Partial dates are allowed.
   */
  @Path("/data[at0001]/items[at0004 and name/value='Date of birth']/value|value")
  private TemporalAccessor dateOfBirthValue;

  /**
   * Path: Patient/Birth/Item tree/Date of birth/null_flavour
   */
  @Path("/data[at0001]/items[at0004 and name/value='Date of birth']/null_flavour|defining_code")
  private NullFlavour dateOfBirthNullFlavourDefiningCode;

  /**
   * Path: Patient/Birth/DOB alternatives
   * Description: Additional details about possible alternative dates of birth.
   */
  @Path("/data[at0001]/items[at0003]")
  private List<Cluster> dobAlternatives;

  /**
   * Path: Patient/Birth/Structured place of birth
   * Description: Structured details about the place of birth.
   * Comment: Please note: there is potential duplication of the 'Country of birth' data element if the CLUSTER.address is used. 
   */
  @Path("/data[at0001]/items[at0005]")
  private List<Cluster> structuredPlaceOfBirth;

  /**
   * Path: Patient/Birth/Birth details
   * Description: A subset of persistent or summary information about the pregnancy and birth of an infant, selected for utility of use within both the maternal and infant health records.
   */
  @Path("/data[at0001]/items[at0008]")
  private List<Cluster> birthDetails;

  /**
   * Path: Patient/Birth/Additional details
   * Description: Additional structured details related to the birth.
   */
  @Path("/data[at0001]/items[at0013]")
  private List<Cluster> additionalDetails;

  /**
   * Path: Patient/Birth/Extension
   */
  @Path("/protocol[at0009]/items[at0011]")
  private List<Cluster> extension;

  /**
   * Path: Patient/Birth/subject
   */
  @Path("/subject")
  private PartyProxy subject;

  /**
   * Path: Patient/Birth/language
   */
  @Path("/language")
  private Language language;

  /**
   * Path: Patient/Birth/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  public void setDateOfBirthValue(TemporalAccessor dateOfBirthValue) {
     this.dateOfBirthValue = dateOfBirthValue;
  }

  public TemporalAccessor getDateOfBirthValue() {
     return this.dateOfBirthValue ;
  }

  public void setDateOfBirthNullFlavourDefiningCode(
      NullFlavour dateOfBirthNullFlavourDefiningCode) {
     this.dateOfBirthNullFlavourDefiningCode = dateOfBirthNullFlavourDefiningCode;
  }

  public NullFlavour getDateOfBirthNullFlavourDefiningCode() {
     return this.dateOfBirthNullFlavourDefiningCode ;
  }

  public void setDobAlternatives(List<Cluster> dobAlternatives) {
     this.dobAlternatives = dobAlternatives;
  }

  public List<Cluster> getDobAlternatives() {
     return this.dobAlternatives ;
  }

  public void setStructuredPlaceOfBirth(List<Cluster> structuredPlaceOfBirth) {
     this.structuredPlaceOfBirth = structuredPlaceOfBirth;
  }

  public List<Cluster> getStructuredPlaceOfBirth() {
     return this.structuredPlaceOfBirth ;
  }

  public void setBirthDetails(List<Cluster> birthDetails) {
     this.birthDetails = birthDetails;
  }

  public List<Cluster> getBirthDetails() {
     return this.birthDetails ;
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
