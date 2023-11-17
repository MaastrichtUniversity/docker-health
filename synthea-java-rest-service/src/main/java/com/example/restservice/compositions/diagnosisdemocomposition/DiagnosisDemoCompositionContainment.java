package com.example.restservice.compositions.diagnosisdemocomposition;

import com.example.restservice.compositions.diagnosisdemocomposition.definition.DiagnosisEvaluation;
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

public class DiagnosisDemoCompositionContainment extends Containment {
  public SelectAqlField<DiagnosisDemoComposition> DIAGNOSIS_DEMO_COMPOSITION = new AqlFieldImp<DiagnosisDemoComposition>(DiagnosisDemoComposition.class, "", "DiagnosisDemoComposition", DiagnosisDemoComposition.class, this);

  public SelectAqlField<Category> CATEGORY_DEFINING_CODE = new AqlFieldImp<Category>(DiagnosisDemoComposition.class, "/category|defining_code", "categoryDefiningCode", Category.class, this);

  public ListSelectAqlField<Cluster> EXTENSION = new ListAqlFieldImp<Cluster>(DiagnosisDemoComposition.class, "/context/other_context[at0006]/items[at0008]", "extension", Cluster.class, this);

  public SelectAqlField<TemporalAccessor> START_TIME_VALUE = new AqlFieldImp<TemporalAccessor>(DiagnosisDemoComposition.class, "/context/start_time|value", "startTimeValue", TemporalAccessor.class, this);

  public ListSelectAqlField<Participation> PARTICIPATIONS = new ListAqlFieldImp<Participation>(DiagnosisDemoComposition.class, "/context/participations", "participations", Participation.class, this);

  public SelectAqlField<TemporalAccessor> END_TIME_VALUE = new AqlFieldImp<TemporalAccessor>(DiagnosisDemoComposition.class, "/context/end_time|value", "endTimeValue", TemporalAccessor.class, this);

  public SelectAqlField<String> LOCATION = new AqlFieldImp<String>(DiagnosisDemoComposition.class, "/context/location", "location", String.class, this);

  public SelectAqlField<PartyIdentified> HEALTH_CARE_FACILITY = new AqlFieldImp<PartyIdentified>(DiagnosisDemoComposition.class, "/context/health_care_facility", "healthCareFacility", PartyIdentified.class, this);

  public SelectAqlField<Setting> SETTING_DEFINING_CODE = new AqlFieldImp<Setting>(DiagnosisDemoComposition.class, "/context/setting|defining_code", "settingDefiningCode", Setting.class, this);

  public ListSelectAqlField<DiagnosisEvaluation> DIAGNOSIS = new ListAqlFieldImp<DiagnosisEvaluation>(DiagnosisDemoComposition.class, "/content[openEHR-EHR-EVALUATION.problem_diagnosis.v1]", "diagnosis", DiagnosisEvaluation.class, this);

  public SelectAqlField<PartyProxy> COMPOSER = new AqlFieldImp<PartyProxy>(DiagnosisDemoComposition.class, "/composer", "composer", PartyProxy.class, this);

  public SelectAqlField<Language> LANGUAGE = new AqlFieldImp<Language>(DiagnosisDemoComposition.class, "/language", "language", Language.class, this);

  public SelectAqlField<FeederAudit> FEEDER_AUDIT = new AqlFieldImp<FeederAudit>(DiagnosisDemoComposition.class, "/feeder_audit", "feederAudit", FeederAudit.class, this);

  public SelectAqlField<Territory> TERRITORY = new AqlFieldImp<Territory>(DiagnosisDemoComposition.class, "/territory", "territory", Territory.class, this);

  private DiagnosisDemoCompositionContainment() {
    super("openEHR-EHR-COMPOSITION.problem_list.v2");
  }

  public static DiagnosisDemoCompositionContainment getInstance() {
    return new DiagnosisDemoCompositionContainment();
  }
}
