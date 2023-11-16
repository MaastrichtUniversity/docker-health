package com.example.restservice.vitalsignscomposition.definition;

import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.Cluster;
import java.lang.Double;
import java.lang.String;
import java.time.temporal.TemporalAccessor;
import java.util.List;
import javax.annotation.processing.Generated;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Entity;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Path;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.PointEventEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.NullFlavour;

@Entity
@Generated(
    value = "org.ehrbase.openehr.sdk.generator.ClassGenerator",
    date = "2023-11-15T13:51:49.024887455+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
public class HeartRatePointInTimePointEvent implements PointEventEntity {
  /**
   * Path: Vital Signs/Heart rate/Point in time/Rate
   * Description: The rate of the pulse or heart beat, measured in beats per minute.
   */
  @Path("/data[at0001]/items[at0004]/value|magnitude")
  private Double rateMagnitude;

  /**
   * Path: Vital Signs/Heart rate/Point in time/Rate
   * Description: The rate of the pulse or heart beat, measured in beats per minute.
   */
  @Path("/data[at0001]/items[at0004]/value|units")
  private String rateUnits;

  /**
   * Path: Vital Signs/Heart rate/history/Point in time/structure/Rate/null_flavour
   */
  @Path("/data[at0001]/items[at0004]/null_flavour|defining_code")
  private NullFlavour rateNullFlavourDefiningCode;

  /**
   * Path: Vital Signs/Heart rate/Point in time/Exertion
   * Description: Details about physical exertion being undertaken during the examination.
   */
  @Path("/state[at0012]/items[at1017]")
  private List<Cluster> exertion;

  /**
   * Path: Vital Signs/Heart rate/Point in time/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  /**
   * Path: Vital Signs/Heart rate/Point in time/time
   */
  @Path("/time|value")
  private TemporalAccessor timeValue;

  public void setRateMagnitude(Double rateMagnitude) {
     this.rateMagnitude = rateMagnitude;
  }

  public Double getRateMagnitude() {
     return this.rateMagnitude ;
  }

  public void setRateUnits(String rateUnits) {
     this.rateUnits = rateUnits;
  }

  public String getRateUnits() {
     return this.rateUnits ;
  }

  public void setRateNullFlavourDefiningCode(NullFlavour rateNullFlavourDefiningCode) {
     this.rateNullFlavourDefiningCode = rateNullFlavourDefiningCode;
  }

  public NullFlavour getRateNullFlavourDefiningCode() {
     return this.rateNullFlavourDefiningCode ;
  }

  public void setExertion(List<Cluster> exertion) {
     this.exertion = exertion;
  }

  public List<Cluster> getExertion() {
     return this.exertion ;
  }

  public void setFeederAudit(FeederAudit feederAudit) {
     this.feederAudit = feederAudit;
  }

  public FeederAudit getFeederAudit() {
     return this.feederAudit ;
  }

  public void setTimeValue(TemporalAccessor timeValue) {
     this.timeValue = timeValue;
  }

  public TemporalAccessor getTimeValue() {
     return this.timeValue ;
  }
}
