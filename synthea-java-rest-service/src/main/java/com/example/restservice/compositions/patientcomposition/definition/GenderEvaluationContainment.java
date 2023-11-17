package com.example.restservice.compositions.patientcomposition.definition;

import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.Cluster;
import com.nedap.archie.rm.generic.PartyProxy;
import org.ehrbase.openehr.sdk.generator.commons.aql.containment.Containment;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.AqlFieldImp;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.ListAqlFieldImp;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.ListSelectAqlField;
import org.ehrbase.openehr.sdk.generator.commons.aql.field.SelectAqlField;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.NullFlavour;

public class GenderEvaluationContainment extends Containment {
  public SelectAqlField<GenderEvaluation> GENDER_EVALUATION = new AqlFieldImp<GenderEvaluation>(GenderEvaluation.class, "", "GenderEvaluation", GenderEvaluation.class, this);

  public SelectAqlField<SexAssignedAtBirthDefiningCode> SEX_ASSIGNED_AT_BIRTH_DEFINING_CODE = new AqlFieldImp<SexAssignedAtBirthDefiningCode>(GenderEvaluation.class, "/data[at0002]/items[at0019]/value|defining_code", "sexAssignedAtBirthDefiningCode", SexAssignedAtBirthDefiningCode.class, this);

  public SelectAqlField<NullFlavour> SEX_ASSIGNED_AT_BIRTH_NULL_FLAVOUR_DEFINING_CODE = new AqlFieldImp<NullFlavour>(GenderEvaluation.class, "/data[at0002]/items[at0019]/null_flavour|defining_code", "sexAssignedAtBirthNullFlavourDefiningCode", NullFlavour.class, this);

  public ListSelectAqlField<Cluster> ADDITIONAL_DETAILS = new ListAqlFieldImp<Cluster>(GenderEvaluation.class, "/data[at0002]/items[at0023]", "additionalDetails", Cluster.class, this);

  public ListSelectAqlField<Cluster> EXTENSION = new ListAqlFieldImp<Cluster>(GenderEvaluation.class, "/protocol[at0003]/items[at0005]", "extension", Cluster.class, this);

  public SelectAqlField<PartyProxy> SUBJECT = new AqlFieldImp<PartyProxy>(GenderEvaluation.class, "/subject", "subject", PartyProxy.class, this);

  public SelectAqlField<Language> LANGUAGE = new AqlFieldImp<Language>(GenderEvaluation.class, "/language", "language", Language.class, this);

  public SelectAqlField<FeederAudit> FEEDER_AUDIT = new AqlFieldImp<FeederAudit>(GenderEvaluation.class, "/feeder_audit", "feederAudit", FeederAudit.class, this);

  private GenderEvaluationContainment() {
    super("openEHR-EHR-EVALUATION.gender.v1");
  }

  public static GenderEvaluationContainment getInstance() {
    return new GenderEvaluationContainment();
  }
}
