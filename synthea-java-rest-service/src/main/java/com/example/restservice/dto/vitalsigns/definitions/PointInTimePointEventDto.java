package com.example.restservice.dto.vitalsigns.definitions;

public class PointInTimePointEventDto {

    /**
     * Path: Vital Signs/Body Height/Point in time/Body Height
     * Description: The length of the body from crown of head to sole of foot.
     */
    private Double magnitude;


    /**
     * Path: Vital Signs/Body Height/Point in time/Body Height
     * Description: The length of the body from crown of head to sole of foot.
     */
    private String units;

    /**
     * Path: Vital Signs/Body Height/Point in time/time
     */
    private String timeValue;

    /**
     * To deserialize a JSON String to custom object, Jackson need to access a default constructor;
     * (https://www.baeldung.com/jackson-exception#2-the-solution)
     */
    public PointInTimePointEventDto() {
        super();
    }

    public PointInTimePointEventDto(Double magnitude, String units, String timeValue) {
        this.magnitude = magnitude;
        this.units = units;
        this.timeValue = timeValue;
    }
    public Double getMagnitude() {
        return magnitude;
    }
    public String getUnits() {
        return units;
    }

    public String getTimeValue() {
        return timeValue;
    }
}
