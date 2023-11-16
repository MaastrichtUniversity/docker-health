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

public class HeartRateObservationContainment extends Containment {
  public SelectAqlField<HeartRateObservation> HEART_RATE_OBSERVATION = new AqlFieldImp<HeartRateObservation>(HeartRateObservation.class, "", "HeartRateObservation", HeartRateObservation.class, this);

  public ListSelectAqlField<HeartRatePointInTimePointEvent> POINT_IN_TIME = new ListAqlFieldImp<HeartRatePointInTimePointEvent>(HeartRateObservation.class, "/data[at0002]/events[at0003]", "pointInTime", HeartRatePointInTimePointEvent.class, this);

  public SelectAqlField<TemporalAccessor> ORIGIN_VALUE = new AqlFieldImp<TemporalAccessor>(HeartRateObservation.class, "/data[at0002]/origin|value", "originValue", TemporalAccessor.class, this);

  public SelectAqlField<Cluster> DEVICE = new AqlFieldImp<Cluster>(HeartRateObservation.class, "/protocol[at0010]/items[at1013]", "device", Cluster.class, this);

  public ListSelectAqlField<Cluster> EXTENSION = new ListAqlFieldImp<Cluster>(HeartRateObservation.class, "/protocol[at0010]/items[at1056]", "extension", Cluster.class, this);

  public SelectAqlField<PartyProxy> SUBJECT = new AqlFieldImp<PartyProxy>(HeartRateObservation.class, "/subject", "subject", PartyProxy.class, this);

  public SelectAqlField<Language> LANGUAGE = new AqlFieldImp<Language>(HeartRateObservation.class, "/language", "language", Language.class, this);

  public SelectAqlField<FeederAudit> FEEDER_AUDIT = new AqlFieldImp<FeederAudit>(HeartRateObservation.class, "/feeder_audit", "feederAudit", FeederAudit.class, this);

  private HeartRateObservationContainment() {
    super("openEHR-EHR-OBSERVATION.pulse.v2");
  }

  public static HeartRateObservationContainment getInstance() {
    return new HeartRateObservationContainment();
  }
}
