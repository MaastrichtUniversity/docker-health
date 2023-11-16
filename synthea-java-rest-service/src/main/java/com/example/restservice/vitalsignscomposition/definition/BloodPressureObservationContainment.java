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

public class BloodPressureObservationContainment extends Containment {
  public SelectAqlField<BloodPressureObservation> BLOOD_PRESSURE_OBSERVATION = new AqlFieldImp<BloodPressureObservation>(BloodPressureObservation.class, "", "BloodPressureObservation", BloodPressureObservation.class, this);

  public ListSelectAqlField<BloodPressurePointInTimePointEvent> POINT_IN_TIME = new ListAqlFieldImp<BloodPressurePointInTimePointEvent>(BloodPressureObservation.class, "/data[at0001]/events[at0006]", "pointInTime", BloodPressurePointInTimePointEvent.class, this);

  public SelectAqlField<TemporalAccessor> ORIGIN_VALUE = new AqlFieldImp<TemporalAccessor>(BloodPressureObservation.class, "/data[at0001]/origin|value", "originValue", TemporalAccessor.class, this);

  public ListSelectAqlField<Cluster> STRUCTURED_MEASUREMENT_LOCATION = new ListAqlFieldImp<Cluster>(BloodPressureObservation.class, "/protocol[at0011]/items[at1057]", "structuredMeasurementLocation", Cluster.class, this);

  public SelectAqlField<Cluster> DEVICE = new AqlFieldImp<Cluster>(BloodPressureObservation.class, "/protocol[at0011]/items[at1025]", "device", Cluster.class, this);

  public ListSelectAqlField<Cluster> EXTENSION = new ListAqlFieldImp<Cluster>(BloodPressureObservation.class, "/protocol[at0011]/items[at1058]", "extension", Cluster.class, this);

  public SelectAqlField<PartyProxy> SUBJECT = new AqlFieldImp<PartyProxy>(BloodPressureObservation.class, "/subject", "subject", PartyProxy.class, this);

  public SelectAqlField<Language> LANGUAGE = new AqlFieldImp<Language>(BloodPressureObservation.class, "/language", "language", Language.class, this);

  public SelectAqlField<FeederAudit> FEEDER_AUDIT = new AqlFieldImp<FeederAudit>(BloodPressureObservation.class, "/feeder_audit", "feederAudit", FeederAudit.class, this);

  private BloodPressureObservationContainment() {
    super("openEHR-EHR-OBSERVATION.blood_pressure.v2");
  }

  public static BloodPressureObservationContainment getInstance() {
    return new BloodPressureObservationContainment();
  }
}
