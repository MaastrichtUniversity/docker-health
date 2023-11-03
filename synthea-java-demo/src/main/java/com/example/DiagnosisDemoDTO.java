package com.example;

public class DiagnosisDemoDTO {

    private String startTime;
    private String endTime;
    private String dateClinicallyRecognised;

    private String diagnosisValue;
    private String diagnosisSNOMEDCode;
    private String genderSNOMEDCode;
    private String genderValue;

    public DiagnosisDemoDTO(String startTime, String endTime, String dateClinicallyRecognised, String diagnosisValue, String getDiagnosisSNOMEDCode, String genderSNOMEDCode, String genderValue) {
        this.startTime = startTime;
        this.endTime = endTime;
        this.dateClinicallyRecognised = dateClinicallyRecognised;
        this.diagnosisValue = diagnosisValue;
        this.diagnosisSNOMEDCode = getDiagnosisSNOMEDCode;
        this.genderSNOMEDCode = genderSNOMEDCode;
        this.genderValue = genderValue;
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

    public String getGenderSNOMEDCode() {
        return genderSNOMEDCode;
    }

    public void setGenderSNOMEDCode(String genderSNOMEDCode) {
        this.genderSNOMEDCode = genderSNOMEDCode;
    }

    public String getGenderValue() {
        return genderValue;
    }

    public void setGenderValue(String genderValue) {
        this.genderValue = genderValue;
    }


}
