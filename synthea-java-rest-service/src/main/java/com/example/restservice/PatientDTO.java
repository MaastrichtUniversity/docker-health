package com.example.restservice;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;

import java.time.temporal.TemporalAccessor;
import java.util.Optional;

public class PatientDTO {

    @NotBlank(message = "startTime is mandatory field")
    @NotEmpty(message = "startTime cannot be empty")
    private String startTime;
    @NotBlank(message = "sexAssignedAtBirth is mandatory field")
    @NotEmpty(message = "sexAssignedAtBirth cannot be empty")
    private String sexAssignedAtBirth ;
    @NotBlank(message = "dateOfBirth is mandatory field")
    @NotEmpty(message = "dateOfBirth cannot be empty")
    private String dateOfBirth;
    private String dateOfDeath  = null;

    public String getStartTime() {
        return startTime;
    }

    public void setStartTime(String startTime) {
        this.startTime = startTime;
    }

    public String getSexAssignedAtBirth() {
        return sexAssignedAtBirth;
    }

    public void setSexAssignedAtBirth(String sexAssignedAtBirth) {
        this.sexAssignedAtBirth = sexAssignedAtBirth;
    }

    public String getDateOfBirth() {
        return dateOfBirth;
    }

    public void setDateOfBirth(String dateOfBirth) {
        this.dateOfBirth = dateOfBirth;
    }

    public String getDateOfDeath() {
        return dateOfDeath;
    }

    public void setDateOfDeath(String dateOfDeath) {
        this.dateOfDeath = dateOfDeath;
    }
}
