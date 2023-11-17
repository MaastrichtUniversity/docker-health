package com.example.restservice.compositions.vitalsignscomposition.definition;

import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.ItemTree;
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
    date = "2023-11-15T13:51:49.015351263+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
public class BodyHeightPointInTimePointEvent implements PointEventEntity {
  /**
   * Path: Vital Signs/Body Height/Point in time/Body Height
   * Description: The length of the body from crown of head to sole of foot.
   */
  @Path("/data[at0003]/items[at0004 and name/value='Body Height']/value|magnitude")
  private Double bodyHeightMagnitude;

  /**
   * Path: Vital Signs/Body Height/Point in time/Body Height
   * Description: The length of the body from crown of head to sole of foot.
   */
  @Path("/data[at0003]/items[at0004 and name/value='Body Height']/value|units")
  private String bodyHeightUnits;

  /**
   * Path: Vital Signs/Body Height/history/Point in time/Simple/Body Height/null_flavour
   */
  @Path("/data[at0003]/items[at0004 and name/value='Body Height']/null_flavour|defining_code")
  private NullFlavour bodyHeightNullFlavourDefiningCode;

  /**
   * Path: Vital Signs/Body Height/Point in time/Tree
   * Description: @ internal @
   */
  @Path("/state[at0013]")
  private ItemTree tree;

  /**
   * Path: Vital Signs/Body Height/Point in time/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  /**
   * Path: Vital Signs/Body Height/Point in time/time
   */
  @Path("/time|value")
  private TemporalAccessor timeValue;

  public void setBodyHeightMagnitude(Double bodyHeightMagnitude) {
     this.bodyHeightMagnitude = bodyHeightMagnitude;
  }

  public Double getBodyHeightMagnitude() {
     return this.bodyHeightMagnitude ;
  }

  public void setBodyHeightUnits(String bodyHeightUnits) {
     this.bodyHeightUnits = bodyHeightUnits;
  }

  public String getBodyHeightUnits() {
     return this.bodyHeightUnits ;
  }

  public void setBodyHeightNullFlavourDefiningCode(NullFlavour bodyHeightNullFlavourDefiningCode) {
     this.bodyHeightNullFlavourDefiningCode = bodyHeightNullFlavourDefiningCode;
  }

  public NullFlavour getBodyHeightNullFlavourDefiningCode() {
     return this.bodyHeightNullFlavourDefiningCode ;
  }

  public void setTree(ItemTree tree) {
     this.tree = tree;
  }

  public ItemTree getTree() {
     return this.tree ;
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
