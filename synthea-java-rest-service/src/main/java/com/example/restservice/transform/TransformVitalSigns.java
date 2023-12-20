package com.example.restservice.transform;

import com.example.restservice.compositions.vitalsignscomposition.VitalSignsComposition;
import com.example.restservice.compositions.vitalsignscomposition.definition.*;
import com.example.restservice.dto.vitalsigns.VitalSignsDTO;
import com.example.restservice.dto.vitalsigns.definitions.PointInTimePointEventDto;
import com.nedap.archie.rm.generic.PartyIdentified;
import com.nedap.archie.rm.generic.PartySelf;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.CompositionEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Setting;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Territory;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import static com.example.restservice.transform.Formatters.formatToCorrectTime;
import static java.util.Objects.nonNull;

public class TransformVitalSigns implements ITransformDto {

    private final VitalSignsDTO vitalSignsDTO;
    private final String templateSemVer;

    private String originTimeValue;

    public TransformVitalSigns(VitalSignsDTO vitalSignsDTO) {
        this.vitalSignsDTO = vitalSignsDTO;
        this.templateSemVer = System.getenv("VITAL_SIGNS_SEM_VER");
    }

    @Override
    public CompositionEntity toCompositionEntity() {
        VitalSignsComposition composition = new VitalSignsComposition();
        composition.setSettingDefiningCode(Setting.HOME);
        composition.setLanguage(Language.EN);
        composition.setTerritory(Territory.NL);
        composition.setComposer(new PartyIdentified(null, "DataHub", null));

        composition.setStartTimeValue(formatToCorrectTime(this.vitalSignsDTO.getStartTime()));

        if (nonNull(this.vitalSignsDTO.getBodyHeightObservation())) {
            composition.setBodyHeight(parseBodyHeight());
        }
        if (nonNull(this.vitalSignsDTO.getBodyWeightObservation())) {
            composition.setBodyWeight(parseBodyWeight());
        }
        if (nonNull(this.vitalSignsDTO.getHeartRateObservation())) {
            composition.setHeartRate(parseHeartRate());
        }
        if (nonNull(this.vitalSignsDTO.getBloodPressureSystolicObservation())) { // and (nonNull(this.vitalSignsDTO.getBloodPressureDiastolicObservation()))
            composition.setBloodPressure(parseBloodPressure());
        }

        return composition;
    }

    public BodyHeightObservation parseBodyHeight() {
        BodyHeightObservation bodyHeightObservation = new BodyHeightObservation();

        bodyHeightObservation.setLanguage(Language.EN);
        bodyHeightObservation.setSubject(new PartySelf());
        bodyHeightObservation.setPointInTime(parseBodyHeightPointInTimeEvents());
        // TODO Check why this timestamp is needed
        bodyHeightObservation.setOriginValue(formatToCorrectTime(this.originTimeValue));

        return bodyHeightObservation;
    }

    public List<BodyHeightPointInTimePointEvent> parseBodyHeightPointInTimeEvents(){
        List<BodyHeightPointInTimePointEvent> bodyHeightPointInTimePointEvents = new ArrayList<>();
        for (PointInTimePointEventDto pointEvent : this.vitalSignsDTO.getBodyHeightObservation().getPointInTime()) {
            BodyHeightPointInTimePointEvent bodyHeightPointInTimePointEvent = new BodyHeightPointInTimePointEvent();

            Double magnitude = pointEvent.getMagnitude();
            String unit = pointEvent.getUnits();
            String time = pointEvent.getTimeValue();

            this.originTimeValue = time;

            bodyHeightPointInTimePointEvent.setBodyHeightMagnitude(magnitude);
            bodyHeightPointInTimePointEvent.setBodyHeightUnits(unit);
            bodyHeightPointInTimePointEvent.setTimeValue(formatToCorrectTime(time));

            bodyHeightPointInTimePointEvents.add(bodyHeightPointInTimePointEvent);
        }

        return bodyHeightPointInTimePointEvents;
    }

    public BodyWeightObservation parseBodyWeight() {
        BodyWeightObservation bodyWeightObservation = new BodyWeightObservation();

        bodyWeightObservation.setLanguage(Language.EN);
        bodyWeightObservation.setSubject(new PartySelf());
        bodyWeightObservation.setPointInTime(parseBodyWeightPointInTimeEvents());
        // TODO Check why this timestamp is needed
        bodyWeightObservation.setOriginValue(formatToCorrectTime(this.originTimeValue));

        return bodyWeightObservation;
    }
    public List<BodyWeightPointInTimePointEvent> parseBodyWeightPointInTimeEvents(){
        List<BodyWeightPointInTimePointEvent> bodyWeightPointInTimePointEvents = new ArrayList<>();
        for (PointInTimePointEventDto pointEvent : this.vitalSignsDTO.getBodyWeightObservation().getPointInTime()) {
            BodyWeightPointInTimePointEvent bodyWeightPointInTimePointEvent = new BodyWeightPointInTimePointEvent();

            Double magnitude = pointEvent.getMagnitude();
            String unit = pointEvent.getUnits();
            String time = pointEvent.getTimeValue();

            this.originTimeValue = time;

            bodyWeightPointInTimePointEvent.setBodyWeightMagnitude(magnitude);
            bodyWeightPointInTimePointEvent.setBodyWeightUnits(unit);
            bodyWeightPointInTimePointEvent.setTimeValue(formatToCorrectTime(time));

            bodyWeightPointInTimePointEvents.add(bodyWeightPointInTimePointEvent);
        }

        return bodyWeightPointInTimePointEvents;
    }

    public HeartRateObservation parseHeartRate() {
        HeartRateObservation heartRateObservation = new HeartRateObservation();

        heartRateObservation.setLanguage(Language.EN);
        heartRateObservation.setSubject(new PartySelf());
        heartRateObservation.setPointInTime(parseHeartRatePointInTimeEvents());
        // TODO Check why this timestamp is needed
        heartRateObservation.setOriginValue(formatToCorrectTime(this.originTimeValue));

        return heartRateObservation;
    }

    public List<HeartRatePointInTimePointEvent> parseHeartRatePointInTimeEvents(){
        List<HeartRatePointInTimePointEvent> heartRatePointInTimePointEvents = new ArrayList<>();
        for (PointInTimePointEventDto pointEvent : this.vitalSignsDTO.getHeartRateObservation().getPointInTime()) {
            HeartRatePointInTimePointEvent heartRatePointInTimePointEvent = new HeartRatePointInTimePointEvent();

            Double magnitude = pointEvent.getMagnitude();
            String unit = pointEvent.getUnits();
            String time = pointEvent.getTimeValue();

            this.originTimeValue = time;

            heartRatePointInTimePointEvent.setHeartRateMagnitude(magnitude);
            heartRatePointInTimePointEvent.setHeartRateUnits(unit);
            heartRatePointInTimePointEvent.setTimeValue(formatToCorrectTime(time));

            heartRatePointInTimePointEvents.add(heartRatePointInTimePointEvent);
        }

        return heartRatePointInTimePointEvents;
    }

    public BloodPressureObservation parseBloodPressure() {
        BloodPressureObservation bloodPressureObservation = new BloodPressureObservation();

        bloodPressureObservation.setLanguage(Language.EN);
        bloodPressureObservation.setSubject(new PartySelf());
        bloodPressureObservation.setPointInTime(parseBloodPressurePointInTimeEvents());
        // TODO Check why this timestamp is needed
        bloodPressureObservation.setOriginValue(formatToCorrectTime(this.originTimeValue));

        return bloodPressureObservation;
    }

    public List<BloodPressurePointInTimePointEvent> parseBloodPressurePointInTimeEvents(){
        List<BloodPressurePointInTimePointEvent> bloodPressurePointInTimePointEvents = new ArrayList<>();

        Iterator<PointInTimePointEventDto> bloodPressureSystolicPointInTimePointEvents = this.vitalSignsDTO.getBloodPressureSystolicObservation().getPointInTime().iterator();
        Iterator<PointInTimePointEventDto> bloodPressureDiastolicPointInTimePointEvents = this.vitalSignsDTO.getBloodPressureDiastolicObservation().getPointInTime().iterator();

        while (bloodPressureSystolicPointInTimePointEvents.hasNext() && bloodPressureDiastolicPointInTimePointEvents.hasNext()) {
            PointInTimePointEventDto pointEventSystolic = bloodPressureSystolicPointInTimePointEvents.next();
            PointInTimePointEventDto pointEventDiastolic = bloodPressureDiastolicPointInTimePointEvents.next();

            BloodPressurePointInTimePointEvent bloodPressurePointInTimePointEvent = new BloodPressurePointInTimePointEvent();

            Double magnitudeSystolic = pointEventSystolic.getMagnitude();
            String unitSystolic = pointEventSystolic.getUnits();
            String timeSystolic = pointEventSystolic.getTimeValue();
            bloodPressurePointInTimePointEvent.setSystolicMagnitude(magnitudeSystolic);
            bloodPressurePointInTimePointEvent.setSystolicUnits(unitSystolic);
            bloodPressurePointInTimePointEvent.setTimeValue(formatToCorrectTime(timeSystolic));

            Double magnitudeDiastolic = pointEventDiastolic.getMagnitude();
            String unitDiastolic = pointEventDiastolic.getUnits();
            String timeDiastolic = pointEventDiastolic.getTimeValue();
            bloodPressurePointInTimePointEvent.setDiastolicMagnitude(magnitudeDiastolic);
            bloodPressurePointInTimePointEvent.setDiastolicUnits(unitDiastolic);
            bloodPressurePointInTimePointEvent.setTimeValue(formatToCorrectTime(timeDiastolic));
            // timeSystolic should be equal to timeDiastolic
            this.originTimeValue = timeSystolic;

            bloodPressurePointInTimePointEvents.add(bloodPressurePointInTimePointEvent);
        }

        return bloodPressurePointInTimePointEvents;
    }

    @Override
    public String getTemplateId() {
        return "vital_signs";
    }

    @Override
    public String getTemplateSemVer() {
        return this.templateSemVer;
    }
}
