package com.example.restservice.compositions.diagnosisdemocomposition;

import com.example.restservice.compositions.diagnosisdemocomposition.definition.DiagnosisEvaluation;
import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.Cluster;
import com.nedap.archie.rm.generic.Participation;
import com.nedap.archie.rm.generic.PartyIdentified;
import com.nedap.archie.rm.generic.PartyProxy;
import com.nedap.archie.rm.support.identification.ObjectVersionId;
import java.lang.String;
import java.time.temporal.TemporalAccessor;
import java.util.List;
import javax.annotation.processing.Generated;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Archetype;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Entity;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Id;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Path;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Template;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.CompositionEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Category;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Setting;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Territory;

@Entity
@Archetype("openEHR-EHR-COMPOSITION.problem_list.v2")
@Generated(
    value = "org.ehrbase.openehr.sdk.generator.ClassGenerator",
    date = "2023-11-15T13:51:24.812247259+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
@Template("diagnosis_demo")
public class DiagnosisDemoComposition implements CompositionEntity {
  /**
   * Path: Diagnosis/category
   */
  @Path("/category|defining_code")
  private Category categoryDefiningCode;

  /**
   * Path: Diagnosis/context/Extension
   * Description: Additional information required to capture local context or to align with other reference models/formalisms.
   * Comment: For example: Local hospital departmental infomation or additional metadata to align with FHIR or CIMI equivalents.
   */
  @Path("/context/other_context[at0006]/items[at0008]")
  private List<Cluster> extension;

  /**
   * Path: Diagnosis/context/start_time
   */
  @Path("/context/start_time|value")
  private TemporalAccessor startTimeValue;

  /**
   * Path: Diagnosis/context/participations
   */
  @Path("/context/participations")
  private List<Participation> participations;

  /**
   * Path: Diagnosis/context/end_time
   */
  @Path("/context/end_time|value")
  private TemporalAccessor endTimeValue;

  /**
   * Path: Diagnosis/context/location
   */
  @Path("/context/location")
  private String location;

  /**
   * Path: Diagnosis/context/health_care_facility
   */
  @Path("/context/health_care_facility")
  private PartyIdentified healthCareFacility;

  /**
   * Path: Diagnosis/context/setting
   */
  @Path("/context/setting|defining_code")
  private Setting settingDefiningCode;

  /**
   * Path: Diagnosis/Diagnosis
   * Description: Details about a single identified health condition, injury, disability or any other issue which impacts on the physical, mental and/or social well-being of an individual.
   * Comment: Clear delineation between the scope of a problem versus a diagnosis is not easy to achieve in practice. For the purposes of clinical documentation with this archetype, problem and diagnosis are regarded as a continuum, with increasing levels of detail and supportive evidence usually providing weight towards the label of 'diagnosis'.
   */
  @Path("/content[openEHR-EHR-EVALUATION.problem_diagnosis.v1 and name/value='Diagnosis']")
  private List<DiagnosisEvaluation> diagnosis;

  /**
   * Path: Diagnosis/composer
   */
  @Path("/composer")
  private PartyProxy composer;

  /**
   * Path: Diagnosis/language
   */
  @Path("/language")
  private Language language;

  /**
   * Path: Diagnosis/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  /**
   * Path: Diagnosis/territory
   */
  @Path("/territory")
  private Territory territory;

  @Id
  private ObjectVersionId versionUid;

  public void setCategoryDefiningCode(Category categoryDefiningCode) {
     this.categoryDefiningCode = categoryDefiningCode;
  }

  public Category getCategoryDefiningCode() {
     return this.categoryDefiningCode ;
  }

  public void setExtension(List<Cluster> extension) {
     this.extension = extension;
  }

  public List<Cluster> getExtension() {
     return this.extension ;
  }

  public void setStartTimeValue(TemporalAccessor startTimeValue) {
     this.startTimeValue = startTimeValue;
  }

  public TemporalAccessor getStartTimeValue() {
     return this.startTimeValue ;
  }

  public void setParticipations(List<Participation> participations) {
     this.participations = participations;
  }

  public List<Participation> getParticipations() {
     return this.participations ;
  }

  public void setEndTimeValue(TemporalAccessor endTimeValue) {
     this.endTimeValue = endTimeValue;
  }

  public TemporalAccessor getEndTimeValue() {
     return this.endTimeValue ;
  }

  public void setLocation(String location) {
     this.location = location;
  }

  public String getLocation() {
     return this.location ;
  }

  public void setHealthCareFacility(PartyIdentified healthCareFacility) {
     this.healthCareFacility = healthCareFacility;
  }

  public PartyIdentified getHealthCareFacility() {
     return this.healthCareFacility ;
  }

  public void setSettingDefiningCode(Setting settingDefiningCode) {
     this.settingDefiningCode = settingDefiningCode;
  }

  public Setting getSettingDefiningCode() {
     return this.settingDefiningCode ;
  }

  public void setDiagnosis(List<DiagnosisEvaluation> diagnosis) {
     this.diagnosis = diagnosis;
  }

  public List<DiagnosisEvaluation> getDiagnosis() {
     return this.diagnosis ;
  }

  public void setComposer(PartyProxy composer) {
     this.composer = composer;
  }

  public PartyProxy getComposer() {
     return this.composer ;
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

  public void setTerritory(Territory territory) {
     this.territory = territory;
  }

  public Territory getTerritory() {
     return this.territory ;
  }

  public ObjectVersionId getVersionUid() {
     return this.versionUid ;
  }

  public void setVersionUid(ObjectVersionId versionUid) {
     this.versionUid = versionUid;
  }
}
