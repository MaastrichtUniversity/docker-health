package com.example.restservice.compositions.patientcomposition;

import com.example.restservice.compositions.patientcomposition.definition.BirthEvaluation;
import com.example.restservice.compositions.patientcomposition.definition.DeathEvaluation;
import com.example.restservice.compositions.patientcomposition.definition.GenderEvaluation;
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

public class PatientCompositionContainment extends Containment {
  public SelectAqlField<PatientComposition> PATIENT_COMPOSITION = new AqlFieldImp<PatientComposition>(PatientComposition.class, "", "PatientComposition", PatientComposition.class, this);

  public SelectAqlField<Category> CATEGORY_DEFINING_CODE = new AqlFieldImp<Category>(PatientComposition.class, "/category|defining_code", "categoryDefiningCode", Category.class, this);

  public ListSelectAqlField<Cluster> EXTENSION = new ListAqlFieldImp<Cluster>(PatientComposition.class, "/context/other_context[at0001]/items[at0002]", "extension", Cluster.class, this);

  public SelectAqlField<TemporalAccessor> START_TIME_VALUE = new AqlFieldImp<TemporalAccessor>(PatientComposition.class, "/context/start_time|value", "startTimeValue", TemporalAccessor.class, this);

  public ListSelectAqlField<Participation> PARTICIPATIONS = new ListAqlFieldImp<Participation>(PatientComposition.class, "/context/participations", "participations", Participation.class, this);

  public SelectAqlField<TemporalAccessor> END_TIME_VALUE = new AqlFieldImp<TemporalAccessor>(PatientComposition.class, "/context/end_time|value", "endTimeValue", TemporalAccessor.class, this);

  public SelectAqlField<String> LOCATION = new AqlFieldImp<String>(PatientComposition.class, "/context/location", "location", String.class, this);

  public SelectAqlField<PartyIdentified> HEALTH_CARE_FACILITY = new AqlFieldImp<PartyIdentified>(PatientComposition.class, "/context/health_care_facility", "healthCareFacility", PartyIdentified.class, this);

  public SelectAqlField<Setting> SETTING_DEFINING_CODE = new AqlFieldImp<Setting>(PatientComposition.class, "/context/setting|defining_code", "settingDefiningCode", Setting.class, this);

  public SelectAqlField<GenderEvaluation> GENDER = new AqlFieldImp<GenderEvaluation>(PatientComposition.class, "/content[openEHR-EHR-EVALUATION.gender.v1]", "gender", GenderEvaluation.class, this);

  public SelectAqlField<BirthEvaluation> BIRTH = new AqlFieldImp<BirthEvaluation>(PatientComposition.class, "/content[openEHR-EHR-EVALUATION.birth_summary.v0]", "birth", BirthEvaluation.class, this);

  public SelectAqlField<DeathEvaluation> DEATH = new AqlFieldImp<DeathEvaluation>(PatientComposition.class, "/content[openEHR-EHR-EVALUATION.death_summary.v1]", "death", DeathEvaluation.class, this);

  public SelectAqlField<PartyProxy> COMPOSER = new AqlFieldImp<PartyProxy>(PatientComposition.class, "/composer", "composer", PartyProxy.class, this);

  public SelectAqlField<Language> LANGUAGE = new AqlFieldImp<Language>(PatientComposition.class, "/language", "language", Language.class, this);

  public SelectAqlField<FeederAudit> FEEDER_AUDIT = new AqlFieldImp<FeederAudit>(PatientComposition.class, "/feeder_audit", "feederAudit", FeederAudit.class, this);

  public SelectAqlField<Territory> TERRITORY = new AqlFieldImp<Territory>(PatientComposition.class, "/territory", "territory", Territory.class, this);

  private PatientCompositionContainment() {
    super("openEHR-EHR-COMPOSITION.encounter.v1");
  }

  public static PatientCompositionContainment getInstance() {
    return new PatientCompositionContainment();
  }
}
