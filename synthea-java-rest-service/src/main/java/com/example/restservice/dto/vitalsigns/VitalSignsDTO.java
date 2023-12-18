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
    private ObservationDto heartRateObservation;

    public VitalSignsDTO(String startTime, ObservationDto bodyHeightObservation, ObservationDto bodyWeightObservation, ObservationDto heartRateObservation) {
        this.startTime = startTime;
        this.bodyHeightObservation = bodyHeightObservation;
        this.bodyWeightObservation = bodyWeightObservation;
        this.heartRateObservation = heartRateObservation;
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
    public ObservationDto getHeartRateObservation() { return heartRateObservation; }
}
