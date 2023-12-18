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
    date = "2023-11-15T13:51:49.021840058+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
public class BodyWeightPointInTimePointEvent implements PointEventEntity {
  /**
   * Path: Vital Signs/Body weight/Point in time/Weight
   * Description: The weight of the individual.
   */
  @Path("/data[at0001]/items[at0004]/value|magnitude")
  private Double bodyWeightMagnitude;

  /**
   * Path: Vital Signs/Body weight/Point in time/Weight
   * Description: The weight of the individual.
   */
  @Path("/data[at0001]/items[at0004]/value|units")
  private String bodyWeightUnits;

  /**
   * Path: Vital Signs/Body weight/history/Point in time/Simple/Weight/null_flavour
   */
  @Path("/data[at0001]/items[at0004]/null_flavour|defining_code")
  private NullFlavour bodyWeightNullFlavourDefiningCode;

  /**
   * Path: Vital Signs/Body weight/Point in time/state structure
   * Description: @ internal @
   */
  @Path("/state[at0008]")
  private ItemTree stateStructure;

  /**
   * Path: Vital Signs/Body weight/Point in time/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  /**
   * Path: Vital Signs/Body weight/Point in time/time
   */
  @Path("/time|value")
  private TemporalAccessor timeValue;

  public void setBodyWeightMagnitude(Double bodyWeightMagnitude) {
     this.bodyWeightMagnitude = bodyWeightMagnitude;
  }

  public Double getBodyWeightMagnitude() {
     return this.bodyWeightMagnitude ;
  }

  public void setBodyWeightUnits(String bodyWeightUnits) {
     this.bodyWeightUnits = bodyWeightUnits;
  }

  public String getBodyWeightUnits() {
     return this.bodyWeightUnits ;
  }

  public void setBodyWeightNullFlavourDefiningCode(NullFlavour bodyWeightNullFlavourDefiningCode) {
     this.bodyWeightNullFlavourDefiningCode = bodyWeightNullFlavourDefiningCode;
  }

  public NullFlavour getBodyWeightNullFlavourDefiningCode() {
     return this.bodyWeightNullFlavourDefiningCode ;
  }

  public void setStateStructure(ItemTree stateStructure) {
     this.stateStructure = stateStructure;
  }

  public ItemTree getStateStructure() {
     return this.stateStructure ;
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
