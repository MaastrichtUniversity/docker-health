package com.example.restservice.patientcomposition.definition;

import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.Cluster;
import com.nedap.archie.rm.generic.PartyProxy;
import java.time.temporal.TemporalAccessor;
import org.ehrbase.openehr.sdk.generator.commons.aql.containment.Containment;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.AqlFieldImp;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.ListAqlFieldImp;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.ListSelectAqlField;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.SelectAqlField;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.NullFlavour;

public class DeathEvaluationContainment extends Containment {
  public SelectAqlField<DeathEvaluation> DEATH_EVALUATION = new AqlFieldImp<DeathEvaluation>(DeathEvaluation.class, "", "DeathEvaluation", DeathEvaluation.class, this);

  public SelectAqlField<TemporalAccessor> DATE_OF_DEATH_VALUE = new AqlFieldImp<TemporalAccessor>(DeathEvaluation.class, "/data[at0001]/items[at0092]/value|value", "dateOfDeathValue", TemporalAccessor.class, this);

  public SelectAqlField<NullFlavour> DATE_OF_DEATH_NULL_FLAVOUR_DEFINING_CODE = new AqlFieldImp<NullFlavour>(DeathEvaluation.class, "/data[at0001]/items[at0092]/null_flavour|defining_code", "dateOfDeathNullFlavourDefiningCode", NullFlavour.class, this);

  public ListSelectAqlField<Cluster> DATE_OF_DEATH_ALTERNATIVES = new ListAqlFieldImp<Cluster>(DeathEvaluation.class, "/data[at0001]/items[at0104]", "dateOfDeathAlternatives", Cluster.class, this);

  public ListSelectAqlField<Cluster> STRUCTURED_PLACE_OF_DEATH = new ListAqlFieldImp<Cluster>(DeathEvaluation.class, "/data[at0001]/items[at0100]", "structuredPlaceOfDeath", Cluster.class, this);

  public ListSelectAqlField<Cluster> ADDITIONAL_DETAILS = new ListAqlFieldImp<Cluster>(DeathEvaluation.class, "/data[at0001]/items[at0042]", "additionalDetails", Cluster.class, this);

  public ListSelectAqlField<Cluster> EXTENSION = new ListAqlFieldImp<Cluster>(DeathEvaluation.class, "/protocol[at0009]/items[at0102]", "extension", Cluster.class, this);

  public SelectAqlField<PartyProxy> SUBJECT = new AqlFieldImp<PartyProxy>(DeathEvaluation.class, "/subject", "subject", PartyProxy.class, this);

  public SelectAqlField<Language> LANGUAGE = new AqlFieldImp<Language>(DeathEvaluation.class, "/language", "language", Language.class, this);

  public SelectAqlField<FeederAudit> FEEDER_AUDIT = new AqlFieldImp<FeederAudit>(DeathEvaluation.class, "/feeder_audit", "feederAudit", FeederAudit.class, this);

  private DeathEvaluationContainment() {
    super("openEHR-EHR-EVALUATION.death_summary.v1");
  }

  public static DeathEvaluationContainment getInstance() {
    return new DeathEvaluationContainment();
  }
}
