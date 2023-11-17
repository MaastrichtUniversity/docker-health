package com.example.restservice;

import com.example.restservice.diagnosisdemocomposition.DiagnosisDemoComposition;
import com.example.restservice.diagnosisdemocomposition.definition.DiagnosisEvaluation;
import com.example.restservice.patientcomposition.PatientComposition;
import com.example.restservice.patientcomposition.definition.BirthEvaluation;
import com.example.restservice.patientcomposition.definition.DeathEvaluation;
import com.example.restservice.patientcomposition.definition.GenderEvaluation;
import com.example.restservice.patientcomposition.definition.SexAssignedAtBirthDefiningCode;
import com.example.restservice.vitalsignscomposition.VitalSignsComposition;
import com.nedap.archie.rm.datatypes.CodePhrase;
import com.nedap.archie.rm.datavalues.DvCodedText;
import com.nedap.archie.rm.generic.PartyIdentified;
import com.nedap.archie.rm.generic.PartySelf;
import com.nedap.archie.rm.support.identification.TerminologyId;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.NullFlavour;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Setting;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Territory;

import java.text.ParsePosition;
import java.time.format.DateTimeFormatter;
import java.time.temporal.TemporalAccessor;
import java.util.Collections;
import java.util.Objects;

import static java.util.Objects.nonNull;

public class GenerateComposition {

    public static TemporalAccessor formatToCorrectTime(String time){
        DateTimeFormatter formatter = DateTimeFormatter.ISO_DATE_TIME;
        ParsePosition pp = new ParsePosition(0);
        return formatter.parseUnresolved(time, pp);
    }


    public DiagnosisDemoComposition generateDiagnosisComposition(DiagnosisDemoDTO diagnosisDemoDTO){
        DiagnosisDemoComposition composition = new DiagnosisDemoComposition();
        composition.setSettingDefiningCode(Setting.HOME);
        composition.setLanguage(Language.EN);
        composition.setTerritory(Territory.NL);
        composition.setEndTimeValue(formatToCorrectTime(diagnosisDemoDTO.getEndTime()));
        composition.setStartTimeValue(formatToCorrectTime(diagnosisDemoDTO.getStartTime()));
        composition.setComposer(new PartyIdentified(null, "DataHub", null));


        // Diagnosis
        DiagnosisEvaluation diagnosisEvaluation = new DiagnosisEvaluation();
        diagnosisEvaluation.setSubject(new PartySelf());
        diagnosisEvaluation.setLanguage(Language.NL);
        diagnosisEvaluation.setDateOfDiagnosisValue(formatToCorrectTime(diagnosisDemoDTO.getDateClinicallyRecognised()));


        DvCodedText dvCodedText = new DvCodedText();
        CodePhrase codePhrase = new CodePhrase();
        TerminologyId terminologyId = new TerminologyId();
        terminologyId.setValue("SNOMED-CT");
        codePhrase.setTerminologyId(terminologyId);
        codePhrase.setCodeString(diagnosisDemoDTO.getDiagnosisSNOMEDCode());
        dvCodedText.setDefiningCode(codePhrase);
        dvCodedText.setValue(diagnosisDemoDTO.getDiagnosisValue());
        diagnosisEvaluation.setDiagnosis(dvCodedText);
        composition.setDiagnosis(Collections.singletonList(diagnosisEvaluation));

         return composition;
    }

    public PatientComposition generatePatientComposition(PatientDTO patientDTO){
        PatientComposition composition = new PatientComposition();
        composition.setSettingDefiningCode(Setting.HOME);
        composition.setLanguage(Language.EN);
        composition.setTerritory(Territory.NL);
        composition.setComposer(new PartyIdentified(null, "DataHub", null));
        composition.setStartTimeValue(formatToCorrectTime(patientDTO.getStartTime()));

        // Date of Birth
        BirthEvaluation birthEvaluation = new BirthEvaluation();
        birthEvaluation.setSubject(new PartySelf());
        birthEvaluation.setLanguage(Language.EN);
        birthEvaluation.setDateOfBirthValue(formatToCorrectTime(patientDTO.getDateOfBirth()));
        composition.setBirth(birthEvaluation);

        //Date of Death
        DeathEvaluation deathEvaluation = new DeathEvaluation();
        if(nonNull(patientDTO.getDateOfDeath())){
                deathEvaluation.setDateOfDeathValue(formatToCorrectTime(patientDTO.getDateOfDeath()));
        }
        else{
                deathEvaluation.setDateOfDeathNullFlavourDefiningCode(NullFlavour.NOT_APPLICABLE);
        }
        deathEvaluation.setSubject(new PartySelf());
        deathEvaluation.setLanguage(Language.EN);
        composition.setDeath(deathEvaluation);

        // Gender at birth
        GenderEvaluation genderEvaluation = new GenderEvaluation();
        if (Objects.equals(patientDTO.getSexAssignedAtBirth(), "Male")){
            genderEvaluation.setSexAssignedAtBirthDefiningCode(SexAssignedAtBirthDefiningCode.MALE);
        }
        else if (Objects.equals(patientDTO.getSexAssignedAtBirth(), "Female")){
            genderEvaluation.setSexAssignedAtBirthDefiningCode(SexAssignedAtBirthDefiningCode.FEMALE);
        }
        else if (Objects.equals(patientDTO.getSexAssignedAtBirth(), "Intersex")){
            genderEvaluation.setSexAssignedAtBirthDefiningCode(SexAssignedAtBirthDefiningCode.INTERSEX);
        }
        else{
            genderEvaluation.setSexAssignedAtBirthNullFlavourDefiningCode(NullFlavour.UNKNOWN);
        }
        genderEvaluation.setSubject(new PartySelf());
        genderEvaluation.setLanguage(Language.EN);
        composition.setGender(genderEvaluation);

        return composition;
    }

    public VitalSignsComposition generateVitalSignsComposition(VitalSignsDTO vitalSignsDTO){
        VitalSignsComposition composition = new VitalSignsComposition();
        composition.setSettingDefiningCode(Setting.HOME);
        composition.setLanguage(Language.EN);
        composition.setTerritory(Territory.NL);
        composition.setEndTimeValue(formatToCorrectTime(vitalSignsDTO.getEndTime()));
        composition.setStartTimeValue(formatToCorrectTime(vitalSignsDTO.getStartTime()));
        composition.setComposer(new PartyIdentified(null, "DataHub", null));

        return composition;
    }


}
