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
@Archetype("openEHR-EHR-OBSERVATION.body_weight.v2")
@Generated(
    value = "org.ehrbase.openehr.sdk.generator.ClassGenerator",
    date = "2023-11-15T13:51:49.021567882+01:00",
    comments = "https://github.com/ehrbase/openEHR_SDK Version: 2.5.0-SNAPSHOT"
)
public class BodyWeightObservation implements EntryEntity {
  /**
   * Path: Vital Signs/Body weight/Point in time
   * Description: Default, unspecified point in time or interval event which may be explicitly defined in a template or at run-time.
   */
  @Path("/data[at0002]/events[at0003 and name/value='Point in time']")
  private List<BodyWeightPointInTimePointEvent> pointInTime;

  /**
   * Path: Vital Signs/Body weight/origin
   */
  @Path("/data[at0002]/origin|value")
  private TemporalAccessor originValue;

  /**
   * Path: Vital Signs/Body weight/Device
   * Description: Details about the weighing device.
   */
  @Path("/protocol[at0015]/items[at0020]")
  private Cluster device;

  /**
   * Path: Vital Signs/Body weight/Extension
   * Description: Additional information required to capture local content or to align with other reference models/formalisms.
   * Comment: For example: local information requirements or additional metadata to align with FHIR or CIMI equivalents.
   */
  @Path("/protocol[at0015]/items[at0027]")
  private List<Cluster> extension;

  /**
   * Path: Vital Signs/Body weight/subject
   */
  @Path("/subject")
  private PartyProxy subject;

  /**
   * Path: Vital Signs/Body weight/language
   */
  @Path("/language")
  private Language language;

  /**
   * Path: Vital Signs/Body weight/feeder_audit
   */
  @Path("/feeder_audit")
  private FeederAudit feederAudit;

  public void setPointInTime(List<BodyWeightPointInTimePointEvent> pointInTime) {
     this.pointInTime = pointInTime;
  }

  public List<BodyWeightPointInTimePointEvent> getPointInTime() {
     return this.pointInTime ;
  }

  public void setOriginValue(TemporalAccessor originValue) {
     this.originValue = originValue;
  }

  public TemporalAccessor getOriginValue() {
     return this.originValue ;
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
