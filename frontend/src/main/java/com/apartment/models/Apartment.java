package com.apartment.models;

import java.math.BigDecimal;

public class Apartment {
    private Long id;
    private String apartmentNumber;
    private int floor;
    private String building;
    private double area;
    private int bedrooms;
    private int bathrooms;
    private String status;
    private BigDecimal monthlyRent;
    
    // Constructors
    public Apartment() {
    }
    
    public Apartment(Long id, String apartmentNumber, int floor, String building, 
                    double area, int bedrooms, int bathrooms, String status, 
                    BigDecimal monthlyRent) {
        this.id = id;
        this.apartmentNumber = apartmentNumber;
        this.floor = floor;
        this.building = building;
        this.area = area;
        this.bedrooms = bedrooms;
        this.bathrooms = bathrooms;
        this.status = status;
        this.monthlyRent = monthlyRent;
    }
    
    // Getters and Setters
    public Long getId() {
        return id;
    }
    
    public void setId(Long id) {
        this.id = id;
    }
    
    public String getApartmentNumber() {
        return apartmentNumber;
    }
    
    public void setApartmentNumber(String apartmentNumber) {
        this.apartmentNumber = apartmentNumber;
    }
    
    public int getFloor() {
        return floor;
    }
    
    public void setFloor(int floor) {
        this.floor = floor;
    }
    
    public String getBuilding() {
        return building;
    }
    
    public void setBuilding(String building) {
        this.building = building;
    }
    
    public double getArea() {
        return area;
    }
    
    public void setArea(double area) {
        this.area = area;
    }
    
    public int getBedrooms() {
        return bedrooms;
    }
    
    public void setBedrooms(int bedrooms) {
        this.bedrooms = bedrooms;
    }
    
    public int getBathrooms() {
        return bathrooms;
    }
    
    public void setBathrooms(int bathrooms) {
        this.bathrooms = bathrooms;
    }
    
    public String getStatus() {
        return status;
    }
    
    public void setStatus(String status) {
        this.status = status;
    }
    
    public BigDecimal getMonthlyRent() {
        return monthlyRent;
    }
    
    public void setMonthlyRent(BigDecimal monthlyRent) {
        this.monthlyRent = monthlyRent;
    }
    
    @Override
    public String toString() {
        return "Căn hộ " + apartmentNumber + " (Tòa " + building + ", Tầng " + floor + ")";
    }
}
