package com.example.restservice;

import com.example.restservice.diagnosisdemocomposition.DiagnosisDemoComposition;
import com.example.restservice.patientcomposition.PatientComposition;
import com.example.restservice.vitalsignscomposition.VitalSignsComposition;
import com.nedap.archie.rm.composition.Composition;
import jakarta.validation.Valid;
import org.ehrbase.openehr.sdk.serialisation.dto.GeneratedDtoToRmConverter;
import org.ehrbase.openehr.sdk.serialisation.jsonencoding.CanonicalJson;
import org.ehrbase.openehr.sdk.validation.CompositionValidator;
import org.openehr.schemas.v1.OPERATIONALTEMPLATE;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;

import java.net.URISyntaxException;

@org.springframework.web.bind.annotation.RestController
public class RestController {

    @PostMapping("/diagnosis-demo")
    String createNewDiagnosis(@Valid @RequestBody DiagnosisDemoDTO diagnosisDemoDTO) throws URISyntaxException {
        GenerateComposition generateComposition = new GenerateComposition();
        DiagnosisDemoComposition composition = generateComposition.generateDiagnosisComposition(diagnosisDemoDTO);
        TemplateProviderLoader provider = new TemplateProviderLoader();
        GeneratedDtoToRmConverter cut = new GeneratedDtoToRmConverter(provider);
        Composition rmObject = (Composition) cut.toRMObject(composition);
        OPERATIONALTEMPLATE template = provider.find(TemplateProviderLoader.TEMPLATE_NAME_DIAGNOSIS).orElseThrow();

        // Validation
        CompositionValidator compositionValidator = new CompositionValidator();
        var result = compositionValidator.validate(rmObject, template);
        if (result.size() > 0) {
            result.forEach(System.out::println);
        } else {
            System.out.println("Composition validated successfully");
        }

        // Uncomment the following lines to run the interaction
        // This will:
        //  - Post the diagnosis-demo template if not found
        //  - Create an EHR
        //  - Post the composition
        EHRbaseClientDemo ehRbaseClientDemo = new EHRbaseClientDemo();
        ehRbaseClientDemo.interactWithEHRBase(composition, TemplateProviderLoader.TEMPLATE_NAME_DIAGNOSIS);

        CanonicalJson json = new CanonicalJson();
        return json.marshal(rmObject);
    }

    @PostMapping("/patient")
    String createNewPatient(@Valid @RequestBody PatientDTO patientDTO) throws URISyntaxException {
        GenerateComposition generateComposition = new GenerateComposition();
        PatientComposition patientComposition = generateComposition.generatePatientComposition(patientDTO);
        TemplateProviderLoader patientTemplateProvider = new TemplateProviderLoader();
        GeneratedDtoToRmConverter cut = new GeneratedDtoToRmConverter(patientTemplateProvider);
        Composition rmObject = (Composition) cut.toRMObject(patientComposition);
        OPERATIONALTEMPLATE template = patientTemplateProvider.find(TemplateProviderLoader.TEMPLATE_NAME_PATIENT).orElseThrow();
        CompositionValidator compositionValidator = new CompositionValidator();
        var result = compositionValidator.validate(rmObject, template);
        if (result.size() > 0) {
            result.forEach(System.out::println);
        } else {
            System.out.println("Composition validated successfully");
        }

        // Uncomment the following lines to run the interaction
        // This will:
        //  - Post the patient template if not found
        //  - Create an EHR
        //  - Post the composition
        EHRbaseClientDemo ehRbaseClientDemo = new EHRbaseClientDemo();
        ehRbaseClientDemo.interactWithEHRBase(patientComposition, TemplateProviderLoader.TEMPLATE_NAME_PATIENT);

        CanonicalJson json = new CanonicalJson();
        return json.marshal(rmObject);
    }


    @PostMapping("/vital_signs")
    String createNewVitalSigns(@Valid @RequestBody VitalSignsDTO vitalSignsDTO) throws URISyntaxException {
        GenerateComposition generateComposition = new GenerateComposition();
        VitalSignsComposition vitalSignsComposition = generateComposition.generateVitalSignsComposition(vitalSignsDTO);

        TemplateProviderLoader vitalSignsTemplateProvider = new TemplateProviderLoader();
        GeneratedDtoToRmConverter cut = new GeneratedDtoToRmConverter(vitalSignsTemplateProvider);
        OPERATIONALTEMPLATE template = vitalSignsTemplateProvider.find(TemplateProviderLoader.TEMPLATE_NAME_VITAL_SIGNS).orElseThrow();

        CompositionValidator compositionValidator = new CompositionValidator();
        Composition rmObject = (Composition) cut.toRMObject(vitalSignsComposition);
        var result = compositionValidator.validate(rmObject, template);
        if (result.size() > 0) {
            result.forEach(System.out::println);
        } else {
            System.out.println("Composition validated successfully");
        }

        EHRbaseClientDemo ehRbaseClientDemo = new EHRbaseClientDemo();
        ehRbaseClientDemo.interactWithEHRBase(vitalSignsComposition, TemplateProviderLoader.TEMPLATE_NAME_VITAL_SIGNS);

        CanonicalJson json = new CanonicalJson();
        return json.marshal(rmObject);
    }


    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public String handleValidationExceptions(MethodArgumentNotValidException ex) {
         var list = ex.getBindingResult().getFieldErrors().stream().map(err -> err.getDefaultMessage()).collect(java.util.stream.Collectors.joining("\n"));
         return list;
    }
}