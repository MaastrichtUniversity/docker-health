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

public class BirthEvaluationContainment extends Containment {
  public SelectAqlField<BirthEvaluation> BIRTH_EVALUATION = new AqlFieldImp<BirthEvaluation>(BirthEvaluation.class, "", "BirthEvaluation", BirthEvaluation.class, this);

  public SelectAqlField<TemporalAccessor> DATE_OF_BIRTH_VALUE = new AqlFieldImp<TemporalAccessor>(BirthEvaluation.class, "/data[at0001]/items[at0004]/value|value", "dateOfBirthValue", TemporalAccessor.class, this);

  public SelectAqlField<NullFlavour> DATE_OF_BIRTH_NULL_FLAVOUR_DEFINING_CODE = new AqlFieldImp<NullFlavour>(BirthEvaluation.class, "/data[at0001]/items[at0004]/null_flavour|defining_code", "dateOfBirthNullFlavourDefiningCode", NullFlavour.class, this);

  public ListSelectAqlField<Cluster> DOB_ALTERNATIVES = new ListAqlFieldImp<Cluster>(BirthEvaluation.class, "/data[at0001]/items[at0003]", "dobAlternatives", Cluster.class, this);

  public ListSelectAqlField<Cluster> STRUCTURED_PLACE_OF_BIRTH = new ListAqlFieldImp<Cluster>(BirthEvaluation.class, "/data[at0001]/items[at0005]", "structuredPlaceOfBirth", Cluster.class, this);

  public ListSelectAqlField<Cluster> BIRTH_DETAILS = new ListAqlFieldImp<Cluster>(BirthEvaluation.class, "/data[at0001]/items[at0008]", "birthDetails", Cluster.class, this);

  public ListSelectAqlField<Cluster> ADDITIONAL_DETAILS = new ListAqlFieldImp<Cluster>(BirthEvaluation.class, "/data[at0001]/items[at0013]", "additionalDetails", Cluster.class, this);

  public ListSelectAqlField<Cluster> EXTENSION = new ListAqlFieldImp<Cluster>(BirthEvaluation.class, "/protocol[at0009]/items[at0011]", "extension", Cluster.class, this);

  public SelectAqlField<PartyProxy> SUBJECT = new AqlFieldImp<PartyProxy>(BirthEvaluation.class, "/subject", "subject", PartyProxy.class, this);

  public SelectAqlField<Language> LANGUAGE = new AqlFieldImp<Language>(BirthEvaluation.class, "/language", "language", Language.class, this);

  public SelectAqlField<FeederAudit> FEEDER_AUDIT = new AqlFieldImp<FeederAudit>(BirthEvaluation.class, "/feeder_audit", "feederAudit", FeederAudit.class, this);

  private BirthEvaluationContainment() {
    super("openEHR-EHR-EVALUATION.birth_summary.v0");
  }

  public static BirthEvaluationContainment getInstance() {
    return new BirthEvaluationContainment();
  }
}
