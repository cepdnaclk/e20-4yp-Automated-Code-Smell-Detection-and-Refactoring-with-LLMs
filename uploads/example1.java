/**
 * Employee Management System - Test File for Code Smell Detection
 * This file intentionally contains multiple code smells for testing purposes
 */

import java.util.*;
import java.util.Date;
import java.io.*;
import java.sql.*;

// CODE SMELL 1: God Class - Too many responsibilities
public class example1 {
    
    // CODE SMELL 2: Magic Numbers
    private static final int MAX_SIZE = 100;
    private List<Employee> employees = new ArrayList<>();
    private Connection dbConnection;
    
    // CODE SMELL 3: Long Parameter List
    public void addEmployee(String name, int age, String address, String phone, 
                           String email, double salary, String department, 
                           String position, Date hireDate, String manager) {
        Employee emp = new Employee();
        emp.name = name;
        emp.age = age;
        emp.address = address;
        emp.phone = phone;
        emp.email = email;
        emp.salary = salary;
        emp.department = department;
        emp.position = position;
        emp.hireDate = hireDate;
        emp.manager = manager;
        employees.add(emp);
    }
    
    // CODE SMELL 4: Long Method with multiple responsibilities
    public void processEmployeeData(Employee emp) throws Exception {
        // Validation
        if (emp.name == null || emp.name.equals("")) {
            throw new Exception("Name is required");
        }
        if (emp.age < 18) {
            throw new Exception("Age must be at least 18");
        }
        if (emp.salary < 0) {
            throw new Exception("Salary cannot be negative");
        }
        
        // Calculate benefits
        double benefits = 0;
        if (emp.salary < 30000) {
            benefits = emp.salary * 0.05;
        } else if (emp.salary >= 30000 && emp.salary < 50000) {
            benefits = emp.salary * 0.10;
        } else if (emp.salary >= 50000 && emp.salary < 80000) {
            benefits = emp.salary * 0.15;
        } else {
            benefits = emp.salary * 0.20;
        }
        emp.benefits = benefits;
        
        // Database operation
        String sql = "INSERT INTO employees VALUES ('" + emp.name + "', " + 
                     emp.age + ", '" + emp.address + "', " + emp.salary + ")";
        Statement stmt = dbConnection.createStatement();
        stmt.executeUpdate(sql);
        
        // Logging
        System.out.println("Employee added: " + emp.name);
        FileWriter fw = new FileWriter("log.txt", true);
        fw.write("Employee added: " + emp.name + "\n");
        fw.close();
        
        // Send notification
        sendEmail(emp.email, "Welcome to the company!");
    }
    
    // CODE SMELL 5: Duplicate Code
    public double calculateYearlyBonus(Employee emp) {
        double bonus = 0;
        if (emp.salary < 30000) {
            bonus = emp.salary * 0.05;
        } else if (emp.salary >= 30000 && emp.salary < 50000) {
            bonus = emp.salary * 0.10;
        } else if (emp.salary >= 50000 && emp.salary < 80000) {
            bonus = emp.salary * 0.15;
        } else {
            bonus = emp.salary * 0.20;
        }
        return bonus;
    }
    
    // CODE SMELL 6: Feature Envy - method uses more of another class's data
    public String getEmployeeInfo(Employee emp) {
        return emp.name + " - " + emp.department + " - " + emp.position + 
               " - $" + emp.salary + " - " + emp.email + " - " + emp.phone;
    }
    
    // CODE SMELL 7: Inappropriate Intimacy - accessing internals of another class
    public void promoteEmployee(Employee emp, String newPosition, double raise) {
        emp.position = newPosition;
        emp.salary = emp.salary + raise;
        emp.promotionHistory.add(new Date() + ": " + newPosition);
    }
    
    // CODE SMELL 8: Dead Code
    private void oldCalculationMethod() {
        // This method is never called
        int x = 10;
        int y = 20;
        int z = x + y;
    }
    
    // CODE SMELL 9: Speculative Generality
    public abstract class FutureFeature {
        // Planned for future use but not currently needed
        public abstract void doSomething();
    }
    
    // CODE SMELL 10: Primitive Obsession
    public void updateAddress(Employee emp, String street, String city, 
                             String state, String zip, String country) {
        emp.address = street + ", " + city + ", " + state + " " + zip + ", " + country;
    }
    
    // CODE SMELL 11: Data Clumps
    public void createEmployee(String street, String city, String state, String zip) {
        // These parameters always appear together
    }
    
    public void updateEmployeeAddress(String street, String city, String state, String zip) {
        // Same group of parameters
    }
    
    // CODE SMELL 12: Switch Statement that should be polymorphism
    public double calculatePay(Employee emp) {
        double pay = 0;
        switch (emp.type) {
            case 1: // Full time
                pay = emp.salary / 12;
                break;
            case 2: // Part time
                pay = emp.hourlyRate * emp.hoursWorked;
                break;
            case 3: // Contractor
                pay = emp.contractAmount;
                break;
            case 4: // Intern
                pay = 1000;
                break;
            default:
                pay = 0;
        }
        return pay;
    }
    
    // CODE SMELL 13: Temporary Field
    private double tempCalculation;
    private String tempResult;
    
    public void complexCalculation(Employee emp) {
        tempCalculation = emp.salary * 1.5;
        tempResult = "Calculated: " + tempCalculation;
        // These fields are only used in this method
    }
    
    // CODE SMELL 14: Message Chain
    public String getDepartmentManagerEmail(Employee emp) {
        return emp.getDepartment().getManager().getContact().getEmail();
    }
    
    // CODE SMELL 15: Middle Man - class that delegates most of its work
    public String getEmployeeName(Employee emp) {
        return emp.getName();
    }
    
    public String getEmployeeDepartment(Employee emp) {
        return emp.getDepartment().getName();
    }
    
    // CODE SMELL 16: Refused Bequest - inherits but doesn't use parent methods
    class ContractEmployee extends Employee {
        @Override
        public double calculateBenefits() {
            throw new UnsupportedOperationException("Contractors don't get benefits");
        }
        
        @Override
        public void trackVacationDays() {
            throw new UnsupportedOperationException("Contractors don't get vacation");
        }
    }
    
    // CODE SMELL 17: Comments instead of clear code
    public void processPayroll() {
        // Loop through all employees
        for (int i = 0; i < employees.size(); i++) {
            Employee e = employees.get(i);
            // Check if employee is active
            if (e.status == 1) {
                // Calculate the pay
                double p = 0;
                // Check employee type
                if (e.type == 1) {
                    // Full time calculation
                    p = e.salary / 12;
                } else {
                    // Part time calculation
                    p = e.hourlyRate * e.hoursWorked;
                }
                // Add to payroll
                e.pay = p;
            }
        }
    }
    
    // CODE SMELL 18: Large Class with too many fields
    private String companyName;
    private String companyAddress;
    private String companyPhone;
    private String companyEmail;
    private String companyWebsite;
    private String ceoName;
    private String cfoName;
    private String hrDirector;
    private int totalEmployees;
    private double totalPayroll;
    private double averageSalary;
    
    // CODE SMELL 19: Lazy Class - does too little
    class EmployeeId {
        private int id;
        public int getId() { return id; }
        public void setId(int id) { this.id = id; }
    }
    
    // CODE SMELL 20: Divergent Change - class changed for different reasons
    public void addDatabaseSupport() {
        // Database code
    }
    
    public void addReportingFeature() {
        // Reporting code
    }
    
    public void addEmailNotifications() {
        // Email code
    }
    
    // CODE SMELL 21: Shotgun Surgery - single change requires changes in many places
    public void changeEmployeeIdFormat() {
        // Would need to change in multiple places across the codebase
    }
    
    // CODE SMELL 22: Parallel Inheritance Hierarchies
    // (Related to smell in another class structure)
    
    // CODE SMELL 23: Exception Handling Anti-pattern
    public void riskyOperation() {
        try {
            // Some risky code
            dbConnection.close();
        } catch (Exception e) {
            // Swallowing exception
            e.printStackTrace();
        }
    }
    
    // CODE SMELL 24: Boolean Parameter
    public void displayEmployee(Employee emp, boolean detailed, boolean withPhoto, 
                               boolean includeHistory, boolean showSalary) {
        // Multiple boolean flags make it unclear what the method does
    }
    
    // CODE SMELL 25: Null Check everywhere
    public void processEmployee(Employee emp) {
        if (emp != null) {
            if (emp.name != null) {
                if (emp.department != null) {
                    if (emp.manager != null) {
                        // Do something
                    }
                }
            }
        }
    }
    
    // Helper method - also has code smells
    private void sendEmail(String to, String message) {
        // Implementation
    }
}

// CODE SMELL 26: Data Class - only getters and setters
class Employee {
    public String name;
    public int age;
    public String address;
    public String phone;
    public String email;
    public double salary;
    public String department;
    public String position;
    public Date hireDate;
    public String manager;
    public double benefits;
    public int type;
    public double hourlyRate;
    public int hoursWorked;
    public double contractAmount;
    public int status;
    public double pay;
    public List<String> promotionHistory = new ArrayList<>();
    
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    // ... many more getters and setters
    
    public Department getDepartment() { 
        return null; // Stub for example
    }
    
    public double calculateBenefits() {
        return 0;
    }
    
    public void trackVacationDays() {
        // Implementation
    }
}

class Department {
    public Manager getManager() { return null; }
    public String getName() { return ""; }
}

class Manager {
    public Contact getContact() { return null; }
}

class Contact {
    public String getEmail() { return ""; }
}