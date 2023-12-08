package com.example.restservice.compositions.vitalsignscomposition.definition;

import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.Cluster;
import java.lang.Double;
import java.lang.String;
import java.time.temporal.TemporalAccessor;
import javax.annotation.processing.Generated;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Entity;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Path;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.PointEventEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.NullFlavour;

@Entity
@Generated(
    value = "org.ehrbase.openehr.sdk.generator.ClassGenerator",
    date = "2023-11-15T13:51:49.028091613+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
public class BloodPressurePointInTimePointEvent implements PointEventEntity {
  /**
   * Path: Vital Signs/Blood pressure/Point in time/Systolic
   * Description: Peak systemic arterial blood pressure  - measured in systolic or contraction phase of the heart cycle.
   */
  @Path("/data[at0003]/items[at0004]/value|magnitude")
  private Double systolicMagnitude;

  /**
   * Path: Vital Signs/Blood pressure/Point in time/Systolic
   * Description: Peak systemic arterial blood pressure  - measured in systolic or contraction phase of the heart cycle.
   */
  @Path("/data[at0003]/items[at0004]/value|units")
  private String systolicUnits;

  /**
   * Path: Vital Signs/Blood pressure/History/Point in time/blood pressure/Systolic/null_flavour
   */
  @Path("/data[at0003]/items[at0004]/null_flavour|defining_code")
  private NullFlavour systolicNullFlavourDefiningCode;

  /**
   * Path: Vital Signs/Blood pressure/Point in time/Diastolic
   * Description: Minimum systemic arterial blood pressure - measured in the diastolic or relaxation phase of the heart cycle.
   */
  @Path("/data[at0003]/items[at0005]/value|magnitude")
  private Double diastolicMagnitude;

  /**
   * Path: Vital Signs/Blood pressure/Point in time/Diastolic
   * Description: Minimum systemic arterial blood pressure - measured in the diastolic or relaxation phase of the heart cycle.
   */
  @Path("/data[at0003]/items[at0005]/value|units")
  private String diastolicUnits;

  /**
   * Path: Vital Signs/Blood pressure/History/Point in time/blood pressure/Diastolic/null_flavour
   */
  @Path("/data[at0003]/items[at0005]/null_flavour|defining_code")
  private NullFlavour diastolicNullFlavourDefiningCode;

  /**
   * Path: Vital Signs/Blood pressure/Point in time/Exertion
   * Description: Details about physical activity undertaken at the time of blood pressure measurement.
   */
  @Path("/state[at0007]/items[at1030]")
  private Cluster exertion;

  /**
   * Path: Vital Signs/Blood pressure/Point in time/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  /**
   * Path: Vital Signs/Blood pressure/Point in time/time
   */
  @Path("/time|value")
  private TemporalAccessor timeValue;

  public void setSystolicMagnitude(Double systolicMagnitude) {
     this.systolicMagnitude = systolicMagnitude;
  }

  public Double getSystolicMagnitude() {
     return this.systolicMagnitude ;
  }

  public void setSystolicUnits(String systolicUnits) {
     this.systolicUnits = systolicUnits;
  }

  public String getSystolicUnits() {
     return this.systolicUnits ;
  }

  public void setSystolicNullFlavourDefiningCode(NullFlavour systolicNullFlavourDefiningCode) {
     this.systolicNullFlavourDefiningCode = systolicNullFlavourDefiningCode;
  }

  public NullFlavour getSystolicNullFlavourDefiningCode() {
     return this.systolicNullFlavourDefiningCode ;
  }

  public void setDiastolicMagnitude(Double diastolicMagnitude) {
     this.diastolicMagnitude = diastolicMagnitude;
  }

  public Double getDiastolicMagnitude() {
     return this.diastolicMagnitude ;
  }

  public void setDiastolicUnits(String diastolicUnits) {
     this.diastolicUnits = diastolicUnits;
  }

  public String getDiastolicUnits() {
     return this.diastolicUnits ;
  }

  public void setDiastolicNullFlavourDefiningCode(NullFlavour diastolicNullFlavourDefiningCode) {
     this.diastolicNullFlavourDefiningCode = diastolicNullFlavourDefiningCode;
  }

  public NullFlavour getDiastolicNullFlavourDefiningCode() {
     return this.diastolicNullFlavourDefiningCode ;
  }

  public void setExertion(Cluster exertion) {
     this.exertion = exertion;
  }

  public Cluster getExertion() {
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
