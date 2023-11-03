package com.example.diagnosisdemocomposition.definition;

import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.Cluster;
import com.nedap.archie.rm.generic.PartyProxy;
import java.lang.String;
import java.time.temporal.TemporalAccessor;
import org.ehrbase.openehr.sdk.generator.commons.aql.containment.Containment;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.AqlFieldImp;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.ListAqlFieldImp;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.ListSelectAqlField;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.SelectAqlField;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.NullFlavour;

public class DiagnosisEvaluationContainment extends Containment {
  public SelectAqlField<DiagnosisEvaluation> DIAGNOSIS_EVALUATION = new AqlFieldImp<DiagnosisEvaluation>(DiagnosisEvaluation.class, "", "DiagnosisEvaluation", DiagnosisEvaluation.class, this);

  public SelectAqlField<String> DIAGNOSIS_VALUE = new AqlFieldImp<String>(DiagnosisEvaluation.class, "/data[at0001]/items[at0002]/value|value", "diagnosisValue", String.class, this);

  public SelectAqlField<NullFlavour> DIAGNOSIS_NULL_FLAVOUR_DEFINING_CODE = new AqlFieldImp<NullFlavour>(DiagnosisEvaluation.class, "/data[at0001]/items[at0002]/null_flavour|defining_code", "diagnosisNullFlavourDefiningCode", NullFlavour.class, this);

  public ListSelectAqlField<Cluster> STRUCTURED_BODY_SITE = new ListAqlFieldImp<Cluster>(DiagnosisEvaluation.class, "/data[at0001]/items[at0039]", "structuredBodySite", Cluster.class, this);

  public SelectAqlField<TemporalAccessor> DATE_OF_ONSET_VALUE = new AqlFieldImp<TemporalAccessor>(DiagnosisEvaluation.class, "/data[at0001]/items[at0077]/value|value", "dateOfOnsetValue", TemporalAccessor.class, this);

  public SelectAqlField<NullFlavour> DATE_OF_ONSET_NULL_FLAVOUR_DEFINING_CODE = new AqlFieldImp<NullFlavour>(DiagnosisEvaluation.class, "/data[at0001]/items[at0077]/null_flavour|defining_code", "dateOfOnsetNullFlavourDefiningCode", NullFlavour.class, this);

  public SelectAqlField<TemporalAccessor> DATE_CLINICALLY_RECOGNISED_VALUE = new AqlFieldImp<TemporalAccessor>(DiagnosisEvaluation.class, "/data[at0001]/items[at0003]/value|value", "dateClinicallyRecognisedValue", TemporalAccessor.class, this);

  public SelectAqlField<NullFlavour> DATE_CLINICALLY_RECOGNISED_NULL_FLAVOUR_DEFINING_CODE = new AqlFieldImp<NullFlavour>(DiagnosisEvaluation.class, "/data[at0001]/items[at0003]/null_flavour|defining_code", "dateClinicallyRecognisedNullFlavourDefiningCode", NullFlavour.class, this);

  public ListSelectAqlField<Cluster> SPECIFIC_DETAILS = new ListAqlFieldImp<Cluster>(DiagnosisEvaluation.class, "/data[at0001]/items[at0043]", "specificDetails", Cluster.class, this);

  public ListSelectAqlField<Cluster> STATUS = new ListAqlFieldImp<Cluster>(DiagnosisEvaluation.class, "/data[at0001]/items[at0046]", "status", Cluster.class, this);

  public ListSelectAqlField<Cluster> EXTENSION = new ListAqlFieldImp<Cluster>(DiagnosisEvaluation.class, "/protocol[at0032]/items[at0071]", "extension", Cluster.class, this);

  public SelectAqlField<PartyProxy> SUBJECT = new AqlFieldImp<PartyProxy>(DiagnosisEvaluation.class, "/subject", "subject", PartyProxy.class, this);

  public SelectAqlField<Language> LANGUAGE = new AqlFieldImp<Language>(DiagnosisEvaluation.class, "/language", "language", Language.class, this);

  public SelectAqlField<FeederAudit> FEEDER_AUDIT = new AqlFieldImp<FeederAudit>(DiagnosisEvaluation.class, "/feeder_audit", "feederAudit", FeederAudit.class, this);

  private DiagnosisEvaluationContainment() {
    super("openEHR-EHR-EVALUATION.problem_diagnosis.v1");
  }

  public static DiagnosisEvaluationContainment getInstance() {
    return new DiagnosisEvaluationContainment();
  }
}
