package com.example.restservice.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;

public class DiagnosisDemoDTO {

    @NotBlank(message = "startTime is mandatory field")
    @NotEmpty(message = "startTime cannot be empty")
    private String startTime;
    private String dateOfResolutionValue = null;
    @NotBlank(message = "dateOfDiagnosisValue is mandatory field")
    @NotEmpty(message = "dateOfDiagnosisValue cannot be empty")
    private String dateOfDiagnosisValue;
    @NotBlank(message = "diagnosisValue is mandatory field")
    @NotEmpty(message = "diagnosisValue cannot be empty")
    private String diagnosisValue;
    @NotBlank(message = "diagnosisSNOMEDCode is mandatory field")
    @NotEmpty(message = "diagnosisSNOMEDCode cannot be empty")
    private String diagnosisSNOMEDCode;

    public DiagnosisDemoDTO(String startTime, String dateOfResolutionValue, String dateOfDiagnosisValue, String diagnosisValue, String getDiagnosisSNOMEDCode, String genderSNOMEDCode, String genderValue) {
        this.startTime = startTime;
        this.dateOfResolutionValue = dateOfResolutionValue;
        this.dateOfDiagnosisValue = dateOfDiagnosisValue;
        this.diagnosisValue = diagnosisValue;
        this.diagnosisSNOMEDCode = getDiagnosisSNOMEDCode;
    }

    public String getStartTime() {
        return startTime;
    }

    public String getDateOfResolutionValue() {
        return dateOfResolutionValue;
    }

    public String getDateOfDiagnosisValue() {
        return dateOfDiagnosisValue;
    }

    public String getDiagnosisValue() {
        return diagnosisValue;
    }

    public String getDiagnosisSNOMEDCode() {
        return diagnosisSNOMEDCode;
    }
}
