package com.example.restservice.compositions.vitalsignscomposition;

import com.example.restservice.compositions.vitalsignscomposition.definition.BloodPressureObservation;
import com.example.restservice.compositions.vitalsignscomposition.definition.HeartRateObservation;
import com.example.restservice.compositions.vitalsignscomposition.definition.BodyHeightObservation;
import com.example.restservice.compositions.vitalsignscomposition.definition.BodyWeightObservation;
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
    date = "2023-11-15T13:51:49.002355619+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
@Template("vital_signs")
public class VitalSignsComposition implements CompositionEntity {
  /**
   * Path: Vital Signs/category
   */
  @Path("/category|defining_code")
  private Category categoryDefiningCode;

  /**
   * Path: Vital Signs/context/Extension
   * Description: Additional information required to capture local context or to align with other reference models/formalisms.
   * Comment: e.g. Local hospital departmental infomation or additional metadata to align with FHIR or CIMI equivalents.
   */
  @Path("/context/other_context[at0001]/items[at0002]")
  private List<Cluster> extension;

  /**
   * Path: Vital Signs/context/start_time
   */
  @Path("/context/start_time|value")
  private TemporalAccessor startTimeValue;

  /**
   * Path: Vital Signs/context/participations
   */
  @Path("/context/participations")
  private List<Participation> participations;

  /**
   * Path: Vital Signs/context/end_time
   */
  @Path("/context/end_time|value")
  private TemporalAccessor endTimeValue;

  /**
   * Path: Vital Signs/context/location
   */
  @Path("/context/location")
  private String location;

  /**
   * Path: Vital Signs/context/health_care_facility
   */
  @Path("/context/health_care_facility")
  private PartyIdentified healthCareFacility;

  /**
   * Path: Vital Signs/context/setting
   */
  @Path("/context/setting|defining_code")
  private Setting settingDefiningCode;

  /**
   * Path: Vital Signs/Body Height
   * Description: Height, or body length, is measured from crown of head to sole of foot.
   * Comment: Height is measured with the individual in a standing position and body length in a recumbent position.
   */
  @Path("/content[openEHR-EHR-OBSERVATION.height.v2 and name/value='Body Height']")
  private BodyHeightObservation bodyHeight;

  /**
   * Path: Vital Signs/Body weight
   * Description: Measurement of the body weight of an individual.
   */
  @Path("/content[openEHR-EHR-OBSERVATION.body_weight.v2]")
  private BodyWeightObservation bodyWeight;

  /**
   * Path: Vital Signs/Heart rate
   * Description: The rate and associated attributes for a pulse or heart beat.
   */
  @Path("/content[openEHR-EHR-OBSERVATION.pulse.v2 and name/value='Heart rate']")
  private HeartRateObservation heartRate;

  /**
   * Path: Vital Signs/Blood pressure
   * Description: The local measurement of arterial blood pressure which is a surrogate for arterial pressure in the systemic circulation.
   * Comment: Most commonly, use of the term 'blood pressure' refers to measurement of brachial artery pressure in the upper arm.
   */
  @Path("/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]")
  private BloodPressureObservation bloodPressure;

  /**
   * Path: Vital Signs/composer
   */
  @Path("/composer")
  private PartyProxy composer;

  /**
   * Path: Vital Signs/language
   */
  @Path("/language")
  private Language language;

  /**
   * Path: Vital Signs/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  /**
   * Path: Vital Signs/territory
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

  public void setBodyHeight(BodyHeightObservation bodyHeight) {
     this.bodyHeight = bodyHeight;
  }

  public BodyHeightObservation getBodyHeight() {
     return this.bodyHeight ;
  }

  public void setBodyWeight(BodyWeightObservation bodyWeight) {
     this.bodyWeight = bodyWeight;
  }

  public BodyWeightObservation getBodyWeight() {
     return this.bodyWeight ;
  }

  public void setHeartRate(HeartRateObservation heartRate) {
     this.heartRate = heartRate;
  }

  public HeartRateObservation getHeartRate() {
     return this.heartRate ;
  }

  public void setBloodPressure(BloodPressureObservation bloodPressure) {
     this.bloodPressure = bloodPressure;
  }

  public BloodPressureObservation getBloodPressure() {
     return this.bloodPressure ;
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
