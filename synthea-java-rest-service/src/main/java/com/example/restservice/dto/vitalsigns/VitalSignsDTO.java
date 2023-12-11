package com.example.restservice.dto.vitalsigns;

import com.example.restservice.dto.vitalsigns.definitions.ObservationDto;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotEmpty;

public class VitalSignsDTO {

    @NotBlank(message = "startTime is mandatory field")
    @NotEmpty(message = "startTime cannot be empty")
    private String startTime;

    private ObservationDto bodyHeightObservation;
    private ObservationDto bodyWeightObservation;

    public VitalSignsDTO(String startTime, ObservationDto bodyHeightObservation, ObservationDto bodyWeightObservation) {
        this.startTime = startTime;
        this.bodyHeightObservation = bodyHeightObservation;
        this.bodyWeightObservation = bodyWeightObservation;
    }

    public String getStartTime() {
        return startTime;
    }

    public ObservationDto getBodyHeightObservation() {
        return bodyHeightObservation;
    }
    public ObservationDto getBodyWeightObservation() {
        return bodyWeightObservation;
    }
}
