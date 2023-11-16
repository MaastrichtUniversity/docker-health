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

public class BodyHeightObservationContainment extends Containment {
  public SelectAqlField<BodyHeightObservation> BODY_HEIGHT_OBSERVATION = new AqlFieldImp<BodyHeightObservation>(BodyHeightObservation.class, "", "BodyHeightObservation", BodyHeightObservation.class, this);

  public ListSelectAqlField<BodyHeightPointInTimePointEvent> POINT_IN_TIME = new ListAqlFieldImp<BodyHeightPointInTimePointEvent>(BodyHeightObservation.class, "/data[at0001]/events[at0002]", "pointInTime", BodyHeightPointInTimePointEvent.class, this);

  public SelectAqlField<TemporalAccessor> ORIGIN_VALUE = new AqlFieldImp<TemporalAccessor>(BodyHeightObservation.class, "/data[at0001]/origin|value", "originValue", TemporalAccessor.class, this);

  public SelectAqlField<Cluster> DEVICE = new AqlFieldImp<Cluster>(BodyHeightObservation.class, "/protocol[at0007]/items[at0011]", "device", Cluster.class, this);

  public ListSelectAqlField<Cluster> EXTENSION = new ListAqlFieldImp<Cluster>(BodyHeightObservation.class, "/protocol[at0007]/items[at0022]", "extension", Cluster.class, this);

  public SelectAqlField<PartyProxy> SUBJECT = new AqlFieldImp<PartyProxy>(BodyHeightObservation.class, "/subject", "subject", PartyProxy.class, this);

  public SelectAqlField<Language> LANGUAGE = new AqlFieldImp<Language>(BodyHeightObservation.class, "/language", "language", Language.class, this);

  public SelectAqlField<FeederAudit> FEEDER_AUDIT = new AqlFieldImp<FeederAudit>(BodyHeightObservation.class, "/feeder_audit", "feederAudit", FeederAudit.class, this);

  private BodyHeightObservationContainment() {
    super("openEHR-EHR-OBSERVATION.height.v2");
  }

  public static BodyHeightObservationContainment getInstance() {
    return new BodyHeightObservationContainment();
  }
}
