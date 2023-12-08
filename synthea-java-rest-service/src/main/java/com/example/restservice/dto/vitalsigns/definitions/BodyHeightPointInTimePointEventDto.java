package com.example.restservice.dto.vitalsigns.definitions;

import jakarta.validation.constraints.PositiveOrZero;

public class BodyHeightPointInTimePointEventDto {
    /**
     * Path: Vital Signs/Body Height/Point in time/Body Height
     * Description: The length of the body from crown of head to sole of foot.
     */
    private Double bodyHeightMagnitude;

    /**
     * Path: Vital Signs/Body Height/Point in time/Body Height
     * Description: The length of the body from crown of head to sole of foot.
     */
    private String bodyHeightUnits;

    /**
     * Path: Vital Signs/Body Height/Point in time/time
     */
    private String timeValue;

    /**
     * To deserialize a JSON String to custom object, Jackson need to access a default constructor;
     * (https://www.baeldung.com/jackson-exception#2-the-solution)
     */
    public BodyHeightPointInTimePointEventDto() {
        super();
    }

    public BodyHeightPointInTimePointEventDto(Double bodyHeightMagnitude, String bodyHeightUnits, String timeValue) {
        this.bodyHeightMagnitude = bodyHeightMagnitude;
        this.bodyHeightUnits = bodyHeightUnits;
        this.timeValue = timeValue;
    }

    public Double getBodyHeightMagnitude() {
        return bodyHeightMagnitude;
    }

    public String getBodyHeightUnits() {
        return bodyHeightUnits;
    }

    public String getTimeValue() {
        return timeValue;
    }
}
