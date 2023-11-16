package com.example.restservice.vitalsignscomposition;

import com.example.restservice.vitalsignscomposition.definition.BloodPressureObservation;
import com.example.restservice.vitalsignscomposition.definition.BodyHeightObservation;
import com.example.restservice.vitalsignscomposition.definition.BodyWeightObservation;
import com.example.restservice.vitalsignscomposition.definition.HeartRateObservation;
import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.Cluster;
import com.nedap.archie.rm.generic.Participation;
import com.nedap.archie.rm.generic.PartyIdentified;
import com.nedap.archie.rm.generic.PartyProxy;
import java.lang.String;
import java.time.temporal.TemporalAccessor;
import org.ehrbase.openehr.sdk.generator.commons.aql.containment.Containment;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.AqlFieldImp;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.ListAqlFieldImp;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.ListSelectAqlField;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.SelectAqlField;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Category;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Setting;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Territory;

public class VitalSignsCompositionContainment extends Containment {
  public SelectAqlField<VitalSignsComposition> VITAL_SIGNS_COMPOSITION = new AqlFieldImp<VitalSignsComposition>(VitalSignsComposition.class, "", "VitalSignsComposition", VitalSignsComposition.class, this);

  public SelectAqlField<Category> CATEGORY_DEFINING_CODE = new AqlFieldImp<Category>(VitalSignsComposition.class, "/category|defining_code", "categoryDefiningCode", Category.class, this);

  public ListSelectAqlField<Cluster> EXTENSION = new ListAqlFieldImp<Cluster>(VitalSignsComposition.class, "/context/other_context[at0001]/items[at0002]", "extension", Cluster.class, this);

  public SelectAqlField<TemporalAccessor> START_TIME_VALUE = new AqlFieldImp<TemporalAccessor>(VitalSignsComposition.class, "/context/start_time|value", "startTimeValue", TemporalAccessor.class, this);

  public ListSelectAqlField<Participation> PARTICIPATIONS = new ListAqlFieldImp<Participation>(VitalSignsComposition.class, "/context/participations", "participations", Participation.class, this);

  public SelectAqlField<TemporalAccessor> END_TIME_VALUE = new AqlFieldImp<TemporalAccessor>(VitalSignsComposition.class, "/context/end_time|value", "endTimeValue", TemporalAccessor.class, this);

  public SelectAqlField<String> LOCATION = new AqlFieldImp<String>(VitalSignsComposition.class, "/context/location", "location", String.class, this);

  public SelectAqlField<PartyIdentified> HEALTH_CARE_FACILITY = new AqlFieldImp<PartyIdentified>(VitalSignsComposition.class, "/context/health_care_facility", "healthCareFacility", PartyIdentified.class, this);

  public SelectAqlField<Setting> SETTING_DEFINING_CODE = new AqlFieldImp<Setting>(VitalSignsComposition.class, "/context/setting|defining_code", "settingDefiningCode", Setting.class, this);

  public SelectAqlField<BodyHeightObservation> BODY_HEIGHT = new AqlFieldImp<BodyHeightObservation>(VitalSignsComposition.class, "/content[openEHR-EHR-OBSERVATION.height.v2]", "bodyHeight", BodyHeightObservation.class, this);

  public SelectAqlField<BodyWeightObservation> BODY_WEIGHT = new AqlFieldImp<BodyWeightObservation>(VitalSignsComposition.class, "/content[openEHR-EHR-OBSERVATION.body_weight.v2]", "bodyWeight", BodyWeightObservation.class, this);

  public SelectAqlField<HeartRateObservation> HEART_RATE = new AqlFieldImp<HeartRateObservation>(VitalSignsComposition.class, "/content[openEHR-EHR-OBSERVATION.pulse.v2]", "heartRate", HeartRateObservation.class, this);

  public SelectAqlField<BloodPressureObservation> BLOOD_PRESSURE = new AqlFieldImp<BloodPressureObservation>(VitalSignsComposition.class, "/content[openEHR-EHR-OBSERVATION.blood_pressure.v2]", "bloodPressure", BloodPressureObservation.class, this);

  public SelectAqlField<PartyProxy> COMPOSER = new AqlFieldImp<PartyProxy>(VitalSignsComposition.class, "/composer", "composer", PartyProxy.class, this);

  public SelectAqlField<Language> LANGUAGE = new AqlFieldImp<Language>(VitalSignsComposition.class, "/language", "language", Language.class, this);

  public SelectAqlField<FeederAudit> FEEDER_AUDIT = new AqlFieldImp<FeederAudit>(VitalSignsComposition.class, "/feeder_audit", "feederAudit", FeederAudit.class, this);

  public SelectAqlField<Territory> TERRITORY = new AqlFieldImp<Territory>(VitalSignsComposition.class, "/territory", "territory", Territory.class, this);

  private VitalSignsCompositionContainment() {
    super("openEHR-EHR-COMPOSITION.encounter.v1");
  }

  public static VitalSignsCompositionContainment getInstance() {
    return new VitalSignsCompositionContainment();
  }
}
