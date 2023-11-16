package com.example.restservice.vitalsignscomposition.definition;

import com.nedap.archie.rm.archetyped.FeederAudit;
import com.nedap.archie.rm.datastructures.Cluster;
import com.nedap.archie.rm.generic.PartyProxy;
import java.time.temporal.TemporalAccessor;
import java.util.List;
import javax.annotation.processing.Generated;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Archetype;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Entity;
import org.ehrbase.openehr.sdk.generator.commons.annotations.Path;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.EntryEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;

@Entity
@Archetype("openEHR-EHR-OBSERVATION.blood_pressure.v2")
@Generated(
    value = "org.ehrbase.openehr.sdk.generator.ClassGenerator",
    date = "2023-11-15T13:51:49.027874548+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
public class BloodPressureObservation implements EntryEntity {
  /**
   * Path: Vital Signs/Blood pressure/Point in time
   * Description: Default, unspecified point in time or interval event which may be explicitly defined in a template or at run-time.
   */
  @Path("/data[at0001]/events[at0006 and name/value='Point in time']")
  private List<BloodPressurePointInTimePointEvent> pointInTime;

  /**
   * Path: Vital Signs/Blood pressure/origin
   */
  @Path("/data[at0001]/origin|value")
  private TemporalAccessor originValue;

  /**
   * Path: Vital Signs/Blood pressure/Structured measurement location
   * Description: Structured anatomical location of where the measurement was taken.
   */
  @Path("/protocol[at0011]/items[at1057]")
  private List<Cluster> structuredMeasurementLocation;

  /**
   * Path: Vital Signs/Blood pressure/Device
   * Description: Details about sphygmomanometer or other device used to measure the blood pressure.
   */
  @Path("/protocol[at0011]/items[at1025]")
  private Cluster device;

  /**
   * Path: Vital Signs/Blood pressure/Extension
   * Description: Additional information required to capture local context or to align with other reference models/formalisms.
   * Comment: For example: Local hospital departmental infomation or additional metadata to align with FHIR or CIMI equivalents.
   */
  @Path("/protocol[at0011]/items[at1058]")
  private List<Cluster> extension;

  /**
   * Path: Vital Signs/Blood pressure/subject
   */
  @Path("/subject")
  private PartyProxy subject;

  /**
   * Path: Vital Signs/Blood pressure/language
   */
  @Path("/language")
  private Language language;

  /**
   * Path: Vital Signs/Blood pressure/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  public void setPointInTime(List<BloodPressurePointInTimePointEvent> pointInTime) {
     this.pointInTime = pointInTime;
  }

  public List<BloodPressurePointInTimePointEvent> getPointInTime() {
     return this.pointInTime ;
  }

  public void setOriginValue(TemporalAccessor originValue) {
     this.originValue = originValue;
  }

  public TemporalAccessor getOriginValue() {
     return this.originValue ;
  }

  public void setStructuredMeasurementLocation(List<Cluster> structuredMeasurementLocation) {
     this.structuredMeasurementLocation = structuredMeasurementLocation;
  }

  public List<Cluster> getStructuredMeasurementLocation() {
     return this.structuredMeasurementLocation ;
  }

  public void setDevice(Cluster device) {
     this.device = device;
  }

  public Cluster getDevice() {
     return this.device ;
  }

  public void setExtension(List<Cluster> extension) {
     this.extension = extension;
  }

  public List<Cluster> getExtension() {
     return this.extension ;
  }

  public void setSubject(PartyProxy subject) {
     this.subject = subject;
  }

  public PartyProxy getSubject() {
     return this.subject ;
  }

  public void setLanguage(Language language) {
     this.language = language;
  }

  public Language getLanguage() {
     return this.language ;
  }

  public void setFeederAudit(FeederAudit feederAudit) {
     this.feederAudit = feederAudit;
  }

  public FeederAudit getFeederAudit() {
     return this.feederAudit ;
  }
}
