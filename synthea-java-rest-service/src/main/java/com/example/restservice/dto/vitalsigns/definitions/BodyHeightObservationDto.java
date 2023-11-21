package com.example.restservice.dto.vitalsigns.definitions;

import java.util.List;

public class BodyHeightObservationDto {
    /**
     * Path: Vital Signs/Body Height/Point in time
     * Description: Default, unspecified point in time or interval event which may be explicitly defined in a template or at run-time.
     */
    private List<BodyHeightPointInTimePointEventDto> pointInTime;

    /**
     * To deserialize a JSON String to custom object, Jackson need to access a default constructor;
     * (https://www.baeldung.com/jackson-exception#2-the-solution)
     */
    public BodyHeightObservationDto() {
        super();
    }

    public BodyHeightObservationDto(List<BodyHeightPointInTimePointEventDto> pointInTime) {
        this.pointInTime = pointInTime;
    }

    public List<BodyHeightPointInTimePointEventDto> getPointInTime() {
        return pointInTime;
    }
}
