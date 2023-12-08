package com.example.restservice.transform;

import com.example.restservice.compositions.vitalsignscomposition.VitalSignsComposition;
import com.example.restservice.compositions.vitalsignscomposition.definition.BodyHeightObservation;
import com.example.restservice.compositions.vitalsignscomposition.definition.BodyHeightPointInTimePointEvent;
import com.example.restservice.dto.vitalsigns.VitalSignsDTO;
import com.example.restservice.dto.vitalsigns.definitions.BodyHeightPointInTimePointEventDto;
import com.nedap.archie.rm.generic.PartyIdentified;
import com.nedap.archie.rm.generic.PartySelf;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.CompositionEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Setting;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Territory;

import java.util.ArrayList;
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
        for (BodyHeightPointInTimePointEventDto pointEvent : this.vitalSignsDTO.getBodyHeightObservation().getPointInTime()) {
            BodyHeightPointInTimePointEvent bodyHeightPointInTimePointEvent = new BodyHeightPointInTimePointEvent();

            Double magnitude = pointEvent.getBodyHeightMagnitude();
            String unit = pointEvent.getBodyHeightUnits();
            String time = pointEvent.getTimeValue();

            this.originTimeValue = time;

            bodyHeightPointInTimePointEvent.setBodyHeightMagnitude(magnitude);
            bodyHeightPointInTimePointEvent.setBodyHeightUnits(unit);
            bodyHeightPointInTimePointEvent.setTimeValue(formatToCorrectTime(time));

            bodyHeightPointInTimePointEvents.add(bodyHeightPointInTimePointEvent);
        }

        return bodyHeightPointInTimePointEvents;
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