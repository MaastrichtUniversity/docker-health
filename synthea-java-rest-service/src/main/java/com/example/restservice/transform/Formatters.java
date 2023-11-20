package com.example.restservice.transform;

import java.text.ParsePosition;
import java.time.format.DateTimeFormatter;
import java.time.temporal.TemporalAccessor;

public class Formatters {

    public static TemporalAccessor formatToCorrectTime(String time) {
        DateTimeFormatter formatter = DateTimeFormatter.ISO_DATE_TIME;
        ParsePosition pp = new ParsePosition(0);
        return formatter.parseUnresolved(time, pp);
    }
}
