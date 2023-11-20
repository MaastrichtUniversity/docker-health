package com.example.restservice.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;

public class PatientDTO {

    @NotBlank(message = "startTime is mandatory field")
    @NotEmpty(message = "startTime cannot be empty")
    private String startTime;
    @NotBlank(message = "sexAssignedAtBirth is mandatory field")
    @NotEmpty(message = "sexAssignedAtBirth cannot be empty")
    private String sexAssignedAtBirth;
    @NotBlank(message = "dateOfBirth is mandatory field")
    @NotEmpty(message = "dateOfBirth cannot be empty")
    private String dateOfBirth;
    private String dateOfDeath = null;

    public String getStartTime() {
        return startTime;
    }

    public String getSexAssignedAtBirth() {
        return sexAssignedAtBirth;
    }

    public String getDateOfBirth() {
        return dateOfBirth;
    }

    public String getDateOfDeath() {
        return dateOfDeath;
    }
}
