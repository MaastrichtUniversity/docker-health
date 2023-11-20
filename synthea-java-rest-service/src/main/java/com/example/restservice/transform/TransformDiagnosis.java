package com.example.restservice.transform;

import com.example.restservice.compositions.diagnosisdemocomposition.DiagnosisDemoComposition;
import com.example.restservice.compositions.diagnosisdemocomposition.definition.DiagnosisEvaluation;
import com.example.restservice.dto.DiagnosisDemoDTO;
import com.nedap.archie.rm.datatypes.CodePhrase;
import com.nedap.archie.rm.datavalues.DvCodedText;
import com.nedap.archie.rm.generic.PartyIdentified;
import com.nedap.archie.rm.generic.PartySelf;
import com.nedap.archie.rm.support.identification.TerminologyId;
import org.ehrbase.openehr.sdk.generator.commons.interfaces.CompositionEntity;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Language;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Setting;
import org.ehrbase.openehr.sdk.generator.commons.shareddefinition.Territory;

import java.util.Collections;

import static com.example.restservice.transform.Formatters.formatToCorrectTime;

public class TransformDiagnosis implements ITransformDto {

    private final DiagnosisDemoDTO diagnosisDemoDTO;
    private final String templateSemVer;

    public TransformDiagnosis(DiagnosisDemoDTO diagnosisDemoDTO) {
        this.diagnosisDemoDTO = diagnosisDemoDTO;
        this.templateSemVer = System.getenv("DIAGNOSIS_SEM_VER");
    }

    @Override
    public CompositionEntity toCompositionEntity() {
        DiagnosisDemoComposition composition = new DiagnosisDemoComposition();
        composition.setSettingDefiningCode(Setting.HOME);
        composition.setLanguage(Language.EN);
        composition.setTerritory(Territory.NL);
        composition.setEndTimeValue(formatToCorrectTime(this.diagnosisDemoDTO.getEndTime()));
        composition.setStartTimeValue(formatToCorrectTime(this.diagnosisDemoDTO.getStartTime()));
        composition.setComposer(new PartyIdentified(null, "DataHub", null));


        // Diagnosis
        DiagnosisEvaluation diagnosisEvaluation = new DiagnosisEvaluation();
        diagnosisEvaluation.setSubject(new PartySelf());
        diagnosisEvaluation.setLanguage(Language.NL);
        diagnosisEvaluation.setDateOfDiagnosisValue(formatToCorrectTime(this.diagnosisDemoDTO.getDateClinicallyRecognised()));


        DvCodedText dvCodedText = new DvCodedText();
        CodePhrase codePhrase = new CodePhrase();
        TerminologyId terminologyId = new TerminologyId();
        terminologyId.setValue("SNOMED-CT");
        codePhrase.setTerminologyId(terminologyId);
        codePhrase.setCodeString(this.diagnosisDemoDTO.getDiagnosisSNOMEDCode());
        dvCodedText.setDefiningCode(codePhrase);
        dvCodedText.setValue(this.diagnosisDemoDTO.getDiagnosisValue());
        diagnosisEvaluation.setDiagnosis(dvCodedText);
        composition.setDiagnosis(Collections.singletonList(diagnosisEvaluation));

        return composition;
    }

    @Override
    public String getTemplateId() {
        return "diagnosis_demo";
    }

    @Override
    public String getTemplateSemVer() {
        return this.templateSemVer;
    }
}
