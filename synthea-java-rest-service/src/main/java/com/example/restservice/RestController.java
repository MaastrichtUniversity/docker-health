package com.example.restservice;

import com.example.restservice.dto.DiagnosisDemoDTO;
import com.example.restservice.dto.PatientDTO;
import com.example.restservice.dto.VitalSignsDTO;
import com.example.restservice.transform.TransformDiagnosis;
import com.example.restservice.transform.TransformPatient;
import com.example.restservice.transform.TransformService;
import com.example.restservice.transform.TransformVitalSigns;
import jakarta.validation.Valid;
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
        TransformService transformService = new TransformService(new TransformDiagnosis(diagnosisDemoDTO));
        transformService.transform();

        String jsonComposition = transformService.convertToJson();

        transformService.load();

        return jsonComposition;
    }

    @PostMapping("/patient")
    String createNewPatient(@Valid @RequestBody PatientDTO patientDTO) throws URISyntaxException {
        TransformService transformService = new TransformService(new TransformPatient(patientDTO));
        transformService.transform();

        String jsonComposition = transformService.convertToJson();

        transformService.load();

        return jsonComposition;
    }


    @PostMapping("/vital_signs")
    String createNewVitalSigns(@Valid @RequestBody VitalSignsDTO vitalSignsDTO) throws URISyntaxException {
        TransformService transformService = new TransformService(new TransformVitalSigns(vitalSignsDTO));
        transformService.transform();

        String jsonComposition = transformService.convertToJson();

        transformService.load();

        return jsonComposition;
    }


    @ResponseStatus(HttpStatus.BAD_REQUEST)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public String handleValidationExceptions(MethodArgumentNotValidException ex) {
         var list = ex.getBindingResult().getFieldErrors().stream().map(err -> err.getDefaultMessage()).collect(java.util.stream.Collectors.joining("\n"));
         return list;
    }
}