package com.example.restservice.diagnosisdemocomposition.definition;

import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.Cluster;
import com.nedap.archie.rm.generic.PartyProxy;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Archetype;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Entity;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Path;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.EntryEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.NullFlavour;

import javax.annotation.processing.Generated;
import java.time.temporal.TemporalAccessor;
import java.util.List;

@Entity
@Archetype("openEHR-EHR-EVALUATION.problem_diagnosis.v1")
@Generated(
    value = "org.ehrbase.openehr.sdk.generator.ClassGenerator",
    date = "2023-11-03T09:40:57.024750006+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
public class DiagnosisEvaluation implements EntryEntity {
  /**
   * Path: diagnosis-demo/Diagnosis/Diagnosis
   * Description: Identification of the problem or diagnosis, by name.
   * Comment: Coding of the name of the problem or diagnosis with a terminology is preferred, where possible.
   */
  @Path("/data[at0001]/items[at0002 and name/value='Diagnosis']/value|value")
  private String diagnosisValue;

  /**
   * Path: diagnosis-demo/Diagnosis/structure/Diagnosis/null_flavour
   */
  @Path("/data[at0001]/items[at0002 and name/value='Diagnosis']/null_flavour|defining_code")
  private NullFlavour diagnosisNullFlavourDefiningCode;

  /**
   * Path: diagnosis-demo/Diagnosis/Structured body site
   * Description: A structured anatomical location for the problem or diagnosis.
   * Comment: Use this SLOT to insert the CLUSTER.anatomical_location or CLUSTER.relative_location archetypes if the requirements for recording the anatomical location are determined at run-time by the application or require more complex modelling such as relative locations.
   *
   * If the anatomical location is included in the Problem/diagnosis name via precoordinated codes, use of this SLOT becomes redundant.
   */
  @Path("/data[at0001]/items[at0039]")
  private List<Cluster> structuredBodySite;

  /**
   * Path: diagnosis-demo/Diagnosis/Date of onset
   * Description: Estimated or actual date/time that signs or symptoms of the problem/diagnosis were first observed.
   * Comment: Data captured/imported as "Age at onset" should be converted to a date using the subject's date of birth.
   */
  @Path("/data[at0001]/items[at0077 and name/value='Date of onset']/value|value")
  private TemporalAccessor dateOfOnsetValue;

  /**
   * Path: diagnosis-demo/Diagnosis/structure/Date of onset/null_flavour
   */
  @Path("/data[at0001]/items[at0077 and name/value='Date of onset']/null_flavour|defining_code")
  private NullFlavour dateOfOnsetNullFlavourDefiningCode;

  /**
   * Path: diagnosis-demo/Diagnosis/Date clinically recognised
   * Description: Estimated or actual date/time the diagnosis or problem was recognised by a healthcare professional.
   * Comment: Partial dates are acceptable. If the subject of care is under the age of one year, then the complete date or a minimum of the month and year is necessary to enable accurate age calculations - for example, if used to drive decision support. Data captured/imported as "Age at time of clinical recognition" should be converted to a date using the subject's date of birth.
   */
  @Path("/data[at0001]/items[at0003 and name/value='Date clinically recognised']/value|value")
  private TemporalAccessor dateClinicallyRecognisedValue;

  /**
   * Path: diagnosis-demo/Diagnosis/structure/Date clinically recognised/null_flavour
   */
  @Path("/data[at0001]/items[at0003 and name/value='Date clinically recognised']/null_flavour|defining_code")
  private NullFlavour dateClinicallyRecognisedNullFlavourDefiningCode;

  /**
   * Path: diagnosis-demo/Diagnosis/Specific details
   * Description: Details that are additionally required to record as unique attributes of this problem or diagnosis.
   * Comment: May include structured detail about the grading or staging of the diagnosis; diagnostic criteria, classification criteria or formal severity assessments such as Common Terminology Criteria for Adverse Events.
   */
  @Path("/data[at0001]/items[at0043]")
  private List<Cluster> specificDetails;

  /**
   * Path: diagnosis-demo/Diagnosis/Status
   * Description: Structured details for location-, domain-, episode- or workflow-specific aspects of the diagnostic process.
   * Comment: Use status or context qualifiers with care, as they are variably used in practice and interoperability cannot be assured unless usage is clearly defined with the community of use. For example: active status - active, inactive, resolved, in remission; evolution status - initial, interim/working, final; temporal status - current, past; episodicity status - first, new, ongoing; admission status - admission, discharge; or priority status - primary, secondary.
   */
  @Path("/data[at0001]/items[at0046]")
  private List<Cluster> status;

  /**
   * Path: diagnosis-demo/Diagnosis/Extension
   * Description: Additional information required to capture local content or to align with other reference models/formalisms.
   * Comment: For example: local information requirements or additional metadata to align with FHIR or CIMI equivalents.
   */
  @Path("/protocol[at0032]/items[at0071]")
  private List<Cluster> extension;

  /**
   * Path: diagnosis-demo/Diagnosis/subject
   */
  @Path("/subject")
  private PartyProxy subject;

  /**
   * Path: diagnosis-demo/Diagnosis/language
   */
  @Path("/language")
  private Language language;

  /**
   * Path: diagnosis-demo/Diagnosis/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  public void setDiagnosisValue(String diagnosisValue) {
     this.diagnosisValue = diagnosisValue;
  }

  public String getDiagnosisValue() {
     return this.diagnosisValue ;
  }

  public void setDiagnosisNullFlavourDefiningCode(NullFlavour diagnosisNullFlavourDefiningCode) {
     this.diagnosisNullFlavourDefiningCode = diagnosisNullFlavourDefiningCode;
  }

  public NullFlavour getDiagnosisNullFlavourDefiningCode() {
     return this.diagnosisNullFlavourDefiningCode ;
  }

  public void setStructuredBodySite(List<Cluster> structuredBodySite) {
     this.structuredBodySite = structuredBodySite;
  }

  public List<Cluster> getStructuredBodySite() {
     return this.structuredBodySite ;
  }

  public void setDateOfOnsetValue(TemporalAccessor dateOfOnsetValue) {
     this.dateOfOnsetValue = dateOfOnsetValue;
  }

  public TemporalAccessor getDateOfOnsetValue() {
     return this.dateOfOnsetValue ;
  }

  public void setDateOfOnsetNullFlavourDefiningCode(
      NullFlavour dateOfOnsetNullFlavourDefiningCode) {
     this.dateOfOnsetNullFlavourDefiningCode = dateOfOnsetNullFlavourDefiningCode;
  }

  public NullFlavour getDateOfOnsetNullFlavourDefiningCode() {
     return this.dateOfOnsetNullFlavourDefiningCode ;
  }

  public void setDateClinicallyRecognisedValue(TemporalAccessor dateClinicallyRecognisedValue) {
     this.dateClinicallyRecognisedValue = dateClinicallyRecognisedValue;
  }

  public TemporalAccessor getDateClinicallyRecognisedValue() {
     return this.dateClinicallyRecognisedValue ;
  }

  public void setDateClinicallyRecognisedNullFlavourDefiningCode(
      NullFlavour dateClinicallyRecognisedNullFlavourDefiningCode) {
     this.dateClinicallyRecognisedNullFlavourDefiningCode = dateClinicallyRecognisedNullFlavourDefiningCode;
  }

  public NullFlavour getDateClinicallyRecognisedNullFlavourDefiningCode() {
     return this.dateClinicallyRecognisedNullFlavourDefiningCode ;
  }

  public void setSpecificDetails(List<Cluster> specificDetails) {
     this.specificDetails = specificDetails;
  }

  public List<Cluster> getSpecificDetails() {
     return this.specificDetails ;
  }

  public void setStatus(List<Cluster> status) {
     this.status = status;
  }

  public List<Cluster> getStatus() {
     return this.status ;
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
