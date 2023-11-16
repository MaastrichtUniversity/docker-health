package com.example.restservice;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;

public class DiagnosisDemoDTO {

    @NotBlank(message = "startTime is mandatory field")
    @NotEmpty(message = "startTime cannot be empty")
    private String startTime;
    @NotBlank(message = "endTime is mandatory field")
    @NotEmpty(message = "endTime cannot be empty")
    private String endTime;
    @NotBlank(message = "dateClinicallyRecognised is mandatory field")
    @NotEmpty(message = "dateClinicallyRecognised cannot be empty")
    private String dateClinicallyRecognised;
    @NotBlank(message = "diagnosisValue is mandatory field")
    @NotEmpty(message = "diagnosisValue cannot be empty")
    private String diagnosisValue;
    @NotBlank(message = "diagnosisSNOMEDCode is mandatory field")
    @NotEmpty(message = "diagnosisSNOMEDCode cannot be empty")
    private String diagnosisSNOMEDCode;

    public DiagnosisDemoDTO(String startTime, String endTime, String dateClinicallyRecognised, String diagnosisValue, String getDiagnosisSNOMEDCode, String genderSNOMEDCode, String genderValue) {
        this.startTime = startTime;
        this.endTime = endTime;
        this.dateClinicallyRecognised = dateClinicallyRecognised;
        this.diagnosisValue = diagnosisValue;
        this.diagnosisSNOMEDCode = getDiagnosisSNOMEDCode;
    }

    public String getStartTime() {
        return startTime;
    }

    public void setStartTime(String startTime) {
        this.startTime = startTime;
    }

    public String getEndTime() {
        return endTime;
    }

    public void setEndTime(String endTime) {
        this.endTime = endTime;
    }

    public String getDateClinicallyRecognised() {
        return dateClinicallyRecognised;
    }

    public void setDateClinicallyRecognised(String dateClinicallyRecognised) {
        this.dateClinicallyRecognised = dateClinicallyRecognised;
    }

    public String getDiagnosisValue() {
        return diagnosisValue;
    }

    public void setDiagnosisValue(String diagnosisValue) {
        this.diagnosisValue = diagnosisValue;
    }

    public String getDiagnosisSNOMEDCode() {
        return diagnosisSNOMEDCode;
    }

    public void setDiagnosisSNOMEDCode(String diagnosisSNOMEDCode) {
        this.diagnosisSNOMEDCode = diagnosisSNOMEDCode;
    }


}
