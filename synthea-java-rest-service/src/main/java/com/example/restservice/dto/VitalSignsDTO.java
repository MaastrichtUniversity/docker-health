package com.example.restservice.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;

public class VitalSignsDTO {

    @NotBlank(message = "startTime is mandatory field")
    @NotEmpty(message = "startTime cannot be empty")
    private String startTime;
    @NotBlank(message = "endTime is mandatory field")
    @NotEmpty(message = "endTime cannot be empty")
    private String endTime;

    public VitalSignsDTO(String startTime, String endTime) {
        this.startTime = startTime;
        this.endTime = endTime;
    }

    public String getEndTime() {
        return endTime;
    }

    public void setEndTime(String endTime) {
        this.endTime = endTime;
    }

    public String getStartTime() {
        return startTime;
    }

    public void setStartTime(String startTime) {
        this.startTime = startTime;
    }
}
