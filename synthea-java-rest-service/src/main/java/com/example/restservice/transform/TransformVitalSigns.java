package com.example.restservice.transform;

import com.example.restservice.compositions.vitalsignscomposition.VitalSignsComposition;
import com.example.restservice.dto.VitalSignsDTO;
import com.nedap.archie.rm.generic.PartyIdentified;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.CompositionEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Setting;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Territory;

import static com.example.restservice.transform.Formatters.formatToCorrectTime;

public class TransformVitalSigns implements ITransformDto {

    VitalSignsDTO vitalSignsDTO;
    final String templateId = "vital_signs";

    public TransformVitalSigns(VitalSignsDTO vitalSignsDTO) {
        this.vitalSignsDTO = vitalSignsDTO;
    }

    @Override
    public CompositionEntity transform() {
        VitalSignsComposition composition = new VitalSignsComposition();
        composition.setSettingDefiningCode(Setting.HOME);
        composition.setLanguage(Language.EN);
        composition.setTerritory(Territory.NL);
        composition.setEndTimeValue(formatToCorrectTime(this.vitalSignsDTO.getEndTime()));
        composition.setStartTimeValue(formatToCorrectTime(this.vitalSignsDTO.getStartTime()));
        composition.setComposer(new PartyIdentified(null, "DataHub", null));

        return composition;
    }

    @Override
    public String getTemplateId() {
        return templateId;
    }
}
