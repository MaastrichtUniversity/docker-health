package com.example.restservice.dto.vitalsigns.definitions;

import java.util.List;

public class ObservationDto {
    /**
     * Path: Vital Signs/Body Height/Point in time
     * Description: Default, unspecified point in time or interval event which may be explicitly defined in a template or at run-time.
     */
    private List<PointInTimePointEventDto> pointInTime;

    /**
     * To deserialize a JSON String to custom object, Jackson need to access a default constructor;
     * (https://www.baeldung.com/jackson-exception#2-the-solution)
     */
    public ObservationDto() {
        super();
    }

    public ObservationDto(List<PointInTimePointEventDto> pointInTime) {
        this.pointInTime = pointInTime;
    }

    public List<PointInTimePointEventDto> getPointInTime() {
        return pointInTime;
    }
}
