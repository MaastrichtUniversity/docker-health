package com.example.restservice.vitalsignscomposition.definition;

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

public class BodyWeightObservationContainment extends Containment {
  public SelectAqlField<BodyWeightObservation> BODY_WEIGHT_OBSERVATION = new AqlFieldImp<BodyWeightObservation>(BodyWeightObservation.class, "", "BodyWeightObservation", BodyWeightObservation.class, this);

  public ListSelectAqlField<BodyWeightPointInTimePointEvent> POINT_IN_TIME = new ListAqlFieldImp<BodyWeightPointInTimePointEvent>(BodyWeightObservation.class, "/data[at0002]/events[at0003]", "pointInTime", BodyWeightPointInTimePointEvent.class, this);

  public SelectAqlField<TemporalAccessor> ORIGIN_VALUE = new AqlFieldImp<TemporalAccessor>(BodyWeightObservation.class, "/data[at0002]/origin|value", "originValue", TemporalAccessor.class, this);

  public SelectAqlField<Cluster> DEVICE = new AqlFieldImp<Cluster>(BodyWeightObservation.class, "/protocol[at0015]/items[at0020]", "device", Cluster.class, this);

  public ListSelectAqlField<Cluster> EXTENSION = new ListAqlFieldImp<Cluster>(BodyWeightObservation.class, "/protocol[at0015]/items[at0027]", "extension", Cluster.class, this);

  public SelectAqlField<PartyProxy> SUBJECT = new AqlFieldImp<PartyProxy>(BodyWeightObservation.class, "/subject", "subject", PartyProxy.class, this);

  public SelectAqlField<Language> LANGUAGE = new AqlFieldImp<Language>(BodyWeightObservation.class, "/language", "language", Language.class, this);

  public SelectAqlField<FeederAudit> FEEDER_AUDIT = new AqlFieldImp<FeederAudit>(BodyWeightObservation.class, "/feeder_audit", "feederAudit", FeederAudit.class, this);

  private BodyWeightObservationContainment() {
    super("openEHR-EHR-OBSERVATION.body_weight.v2");
  }

  public static BodyWeightObservationContainment getInstance() {
    return new BodyWeightObservationContainment();
  }
}
