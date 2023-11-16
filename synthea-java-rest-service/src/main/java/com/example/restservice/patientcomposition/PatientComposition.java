package com.example.restservice.patientcomposition;

import com.example.restservice.patientcomposition.definition.BirthEvaluation;
import com.example.restservice.patientcomposition.definition.DeathEvaluation;
import com.example.restservice.patientcomposition.definition.GenderEvaluation;
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
@Archetype("openEHR-EHR-COMPOSITION.encounter.v1")
@Generated(
    value = "org.ehrbase.openehr.sdk.generator.ClassGenerator",
    date = "2023-11-15T13:51:36.016399622+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
@Template("patient")
public class PatientComposition implements CompositionEntity {
  /**
   * Path: Patient/category
   */
  @Path("/category|defining_code")
  private Category categoryDefiningCode;

  /**
   * Path: Patient/context/Extension
   * Description: Additional information required to capture local context or to align with other reference models/formalisms.
   * Comment: e.g. Local hospital departmental infomation or additional metadata to align with FHIR or CIMI equivalents.
   */
  @Path("/context/other_context[at0001]/items[at0002]")
  private List<Cluster> extension;

  /**
   * Path: Patient/context/start_time
   */
  @Path("/context/start_time|value")
  private TemporalAccessor startTimeValue;

  /**
   * Path: Patient/context/participations
   */
  @Path("/context/participations")
  private List<Participation> participations;

  /**
   * Path: Patient/context/end_time
   */
  @Path("/context/end_time|value")
  private TemporalAccessor endTimeValue;

  /**
   * Path: Patient/context/location
   */
  @Path("/context/location")
  private String location;

  /**
   * Path: Patient/context/health_care_facility
   */
  @Path("/context/health_care_facility")
  private PartyIdentified healthCareFacility;

  /**
   * Path: Patient/context/setting
   */
  @Path("/context/setting|defining_code")
  private Setting settingDefiningCode;

  /**
   * Path: Patient/Gender
   * Description: Details about the gender of an individual.
   */
  @Path("/content[openEHR-EHR-EVALUATION.gender.v1]")
  private GenderEvaluation gender;

  /**
   * Path: Patient/Birth
   * Description: Overview or summary record of the pregnancy and birth of an individual.
   */
  @Path("/content[openEHR-EHR-EVALUATION.birth_summary.v0 and name/value='Birth']")
  private BirthEvaluation birth;

  /**
   * Path: Patient/Death
   * Description: Summary information about the circumstances and context of the death of an individual, excluding the cause(s) of death.
   */
  @Path("/content[openEHR-EHR-EVALUATION.death_summary.v1 and name/value='Death']")
  private DeathEvaluation death;

  /**
   * Path: Patient/composer
   */
  @Path("/composer")
  private PartyProxy composer;

  /**
   * Path: Patient/language
   */
  @Path("/language")
  private Language language;

  /**
   * Path: Patient/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  /**
   * Path: Patient/territory
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

  public void setGender(GenderEvaluation gender) {
     this.gender = gender;
  }

  public GenderEvaluation getGender() {
     return this.gender ;
  }

  public void setBirth(BirthEvaluation birth) {
     this.birth = birth;
  }

  public BirthEvaluation getBirth() {
     return this.birth ;
  }

  public void setDeath(DeathEvaluation death) {
     this.death = death;
  }

  public DeathEvaluation getDeath() {
     return this.death ;
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
