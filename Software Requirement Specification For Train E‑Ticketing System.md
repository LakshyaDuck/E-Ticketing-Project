## **1. Introduction**

### **1.1 Purpose of the Software**

The purpose of this document is to describe the functional and non‑functional requirements of the **Train E‑Ticketing System**.  
This SRS provides a clear understanding of system behavior, constraints, and requirements for developers, testers, and evaluators before design and implementation.

---

### **1.2 Scope of the Software**

The **Train E‑Ticketing System** is a web‑based application that enables users to search, book, and cancel train tickets between selected cities across different states.

The system supports:

- Train and compartment design
    
- Route and schedule management
    
- Seat availability tracking
    
- Ticket booking and cancellation
    
- Payment validation (simulated)
    
- Administrative control
    

The project is developed using the **Iterative and Incremental Model**.

---

### **1.3 Definitions, Acronyms, and Abbreviations**

|Term|Meaning|
|---|---|
|SRS|Software Requirement Specification|
|UI|User Interface|
|DB|Database|
|API|Application Programming Interface|
|ORM|Object Relational Mapping|

---

## **2. Overall Description**

### **2.1 Product Perspective**

The system follows a **client–server architecture** and is designed using a **layered approach**.

- Frontend handles user interaction
    
- Backend handles business logic and workflows
    
- Database stores persistent data
    

The backend is implemented using **FastAPI**, with **SQLAlchemy** for relational data and **MongoEngine** for logging and audit data.

---

### **2.2 User Types**

|User Type|Description|
|---|---|
|Passenger|Searches, books, and cancels tickets|
|Admin|Manages trains, routes, schedules, and reports|

---

### **2.3 Operating Environment**

- Web‑based system accessible via browser
    
- Backend server running FastAPI
    
- Relational database for transactional data
    
- Document database for logs and system events
    

---

## **3. Functional Requirements**

### **FR1: User Registration and Login**

- The system shall allow users to register and login securely.
    

### **FR2: Train and Compartment Management**

- The system shall allow admin to define trains, number of coaches, and seat layouts.
    

### **FR3: Route and Schedule Management**

- The system shall allow admin to define states, cities, routes, and train schedules.
    

### **FR4: Ticket Search**

- The system shall allow users to search trains using source, destination, and date.
    

### **FR5: Seat Availability Check**

- The system shall display real‑time seat availability for selected trains.
    

### **FR6: Ticket Booking**

- The system shall allow users to book available seats.
    

### **FR7: Payment Processing**

- The system shall validate payment details using a sthird‑party credit card checker.
    

### **FR8: Ticket Cancellation**

- The system shall allow users to cancel booked tickets based on defined rules.
    

### **FR9: Booking State Management**

- The system shall manage ticket states such as _Booked_, _Cancelled_, and _Completed_.
    

### **FR10: Admin Reports**

- The system shall generate booking and cancellation reports for admin users.
    

---

## **4. Non‑Functional Requirements**

### **4.1 Performance Requirements**

- The system should respond to user requests within 2–3 seconds.
    
- Concurrent users should not affect booking consistency.
    

### **4.2 Security Requirements**

- Passwords must be stored in encrypted form.
    
- Token‑based authentication must be used.
    
- Admin functions must be access‑restricted.
    

### **4.3 Reliability Requirements**

- Seat allocation must remain consistent during booking and cancellation.
    
- System should handle invalid operations gracefully.
    

---

## **5. System Requirements**

### **5.1 Hardware Requirements**

- Device: Desktop or Laptop
    
- Processor: Intel i3 or higher
    
- RAM: Minimum 4 GB
    
- Storage: Minimum 20 GB free space
    
- Network: Internet connection
    

---

### **5.2 Software Requirements**

- Operating System: Windows 10/11 or Linux
    
- Web Browser: Google Chrome
    
- Frontend: React.js, HTML, Tailwind, JavaScript
    
- Backend: Python (FastAPI)
    
- Database:
    
    - MySQL (Relational data)
        
    - MongoDB (Logs and audit data)
        
- ORM / ODM:
    
    - SQLAlchemy
        
    - MongoEngine
        
- Tools:
    
    - VS Code
        
    - Git
        
    - Uvicorn
        

---