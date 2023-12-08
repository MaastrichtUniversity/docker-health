package com.example.restservice.transform;

import com.example.restservice.compositions.patientcomposition.PatientComposition;
import com.example.restservice.compositions.patientcomposition.definition.BirthEvaluation;
import com.example.restservice.compositions.patientcomposition.definition.DeathEvaluation;
import com.example.restservice.compositions.patientcomposition.definition.GenderEvaluation;
import com.example.restservice.compositions.patientcomposition.definition.SexAssignedAtBirthDefiningCode;
import com.example.restservice.dto.PatientDTO;
import com.nedap.archie.rm.generic.PartyIdentified;
import com.nedap.archie.rm.generic.PartySelf;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.CompositionEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.NullFlavour;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Setting;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Territory;

import java.util.Objects;

import static com.example.restservice.transform.Formatters.formatToCorrectTime;
import static java.util.Objects.nonNull;

public class TransformPatient implements ITransformDto {

    private final PatientDTO patientDTO;
    private final String templateSemVer;

    public TransformPatient(PatientDTO patientDTO) {
        this.patientDTO = patientDTO;
        this.templateSemVer = System.getenv("PATIENT_SEM_VER");
    }

    @Override
    public CompositionEntity toCompositionEntity() {
        PatientComposition composition = new PatientComposition();
        composition.setSettingDefiningCode(Setting.HOME);
        composition.setLanguage(Language.EN);
        composition.setTerritory(Territory.NL);
        composition.setComposer(new PartyIdentified(null, "DataHub", null));
        composition.setStartTimeValue(formatToCorrectTime(this.patientDTO.getStartTime()));

        // Date of Birth
        BirthEvaluation birthEvaluation = new BirthEvaluation();
        birthEvaluation.setSubject(new PartySelf());
        birthEvaluation.setLanguage(Language.EN);
        birthEvaluation.setDateOfBirthValue(formatToCorrectTime(this.patientDTO.getDateOfBirth()));
        composition.setBirth(birthEvaluation);

        //Date of Death
        DeathEvaluation deathEvaluation = new DeathEvaluation();
        if (nonNull(patientDTO.getDateOfDeath())) {
            deathEvaluation.setDateOfDeathValue(formatToCorrectTime(this.patientDTO.getDateOfDeath()));
        } else {
            deathEvaluation.setDateOfDeathNullFlavourDefiningCode(NullFlavour.NOT_APPLICABLE);
        }
        deathEvaluation.setSubject(new PartySelf());
        deathEvaluation.setLanguage(Language.EN);
        composition.setDeath(deathEvaluation);

        // Gender at birth
        GenderEvaluation genderEvaluation = new GenderEvaluation();
        if (Objects.equals(this.patientDTO.getSexAssignedAtBirth(), "Male")) {
            genderEvaluation.setSexAssignedAtBirthDefiningCode(SexAssignedAtBirthDefiningCode.MALE);
        } else if (Objects.equals(this.patientDTO.getSexAssignedAtBirth(), "Female")) {
            genderEvaluation.setSexAssignedAtBirthDefiningCode(SexAssignedAtBirthDefiningCode.FEMALE);
        } else if (Objects.equals(this.patientDTO.getSexAssignedAtBirth(), "Intersex")) {
            genderEvaluation.setSexAssignedAtBirthDefiningCode(SexAssignedAtBirthDefiningCode.INTERSEX);
        } else {
            genderEvaluation.setSexAssignedAtBirthNullFlavourDefiningCode(NullFlavour.UNKNOWN);
        }
        genderEvaluation.setSubject(new PartySelf());
        genderEvaluation.setLanguage(Language.EN);
        composition.setGender(genderEvaluation);

        return composition;

    }

    @Override
    public String getTemplateId() {
        return "patient";
    }

    @Override
    public String getTemplateSemVer() {
        return this.templateSemVer;
    }
}
