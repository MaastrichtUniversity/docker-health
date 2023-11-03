package com.example.restservice;

import com.example.restservice.diagnosisdemocomposition.DiagnosisDemoComposition;
import com.example.restservice.diagnosisdemocomposition.definition.DiagnosisEvaluation;
import com.example.restservice.diagnosisdemocomposition.definition.GenderEvaluation;
import com.nedap.archie.rm.datatypes.CodePhrase;
import com.nedap.archie.rm.datavalues.DvCodedText;
import com.nedap.archie.rm.generic.PartyIdentified;
import com.nedap.archie.rm.generic.PartySelf;
import com.nedap.archie.rm.support.identification.TerminologyId;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Setting;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Territory;

import java.text.ParsePosition;
import java.time.format.DateTimeFormatter;
import java.time.temporal.TemporalAccessor;
import java.util.Collections;

public class GenerateComposition {

    public static TemporalAccessor formatToCorrectTime(String time){
        DateTimeFormatter formatter = DateTimeFormatter.ISO_DATE_TIME;
        ParsePosition pp = new ParsePosition(0);
        return formatter.parseUnresolved(time, pp);
    }


    public DiagnosisDemoComposition generateComposition(DiagnosisDemoDTO diagnosisDemoDTO){
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
        diagnosisEvaluation.setDateClinicallyRecognisedValue(formatToCorrectTime(diagnosisDemoDTO.getDateClinicallyRecognised()));


        DvCodedText dvCodedText = new DvCodedText();
        CodePhrase codePhrase = new CodePhrase();
        TerminologyId terminologyId = new TerminologyId();
        terminologyId.setValue("SNOMED-CT");
        codePhrase.setTerminologyId(terminologyId);
        codePhrase.setCodeString(diagnosisDemoDTO.getDiagnosisSNOMEDCode());
        dvCodedText.setDefiningCode(codePhrase);
        dvCodedText.setValue(diagnosisDemoDTO.getDiagnosisValue());
        // This loses all my nice code setting
        //diagnosisEvaluation.setDiagnosisValue(dvCodedText.getValue());
        diagnosisEvaluation.setDiagnosisValue(dvCodedText.toString());
        composition.setDiagnosis(Collections.singletonList(diagnosisEvaluation));

        // Gender
        GenderEvaluation genderEvaluation = new GenderEvaluation();
        genderEvaluation.setSubject(new PartySelf());
        genderEvaluation.setLanguage(Language.NL);

        DvCodedText codedGender = new DvCodedText();
        CodePhrase genderCcodePhrase = new CodePhrase();
        TerminologyId genderTerminologyId = new TerminologyId();
        genderTerminologyId.setValue("SNOMED-CT");
        genderCcodePhrase.setTerminologyId(terminologyId);
        genderCcodePhrase.setCodeString(diagnosisDemoDTO.getGenderSNOMEDCode());
        codedGender.setDefiningCode(codePhrase);
        codedGender.setValue(diagnosisDemoDTO.getGenderValue());
        genderEvaluation.setSexAssignedAtBirth(codedGender);
        composition.setGender(genderEvaluation);

        return composition;
    }
}
