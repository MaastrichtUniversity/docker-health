package com.example.restservice.dto.vitalsigns;

import com.example.restservice.dto.vitalsigns.definitions.ObservationDto;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;

public class VitalSignsDTO {

    @NotBlank(message = "startTime is mandatory field")
    @NotEmpty(message = "startTime cannot be empty")
    private String startTime;

    private ObservationDto bodyHeightObservation;

    public VitalSignsDTO(String startTime, ObservationDto bodyHeightObservation) {
        this.startTime = startTime;
        this.bodyHeightObservation = bodyHeightObservation;
    }

    public String getStartTime() {
        return startTime;
    }

    public ObservationDto getBodyHeightObservation() {
        return bodyHeightObservation;
    }
}
