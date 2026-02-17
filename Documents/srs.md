---
title: Software Requirement Specification (SRS)
subtitle: Airplane E‑Ticketing System
author: >
  Team:<br>
  Lakshya Saini - 24001001069<br>
  Lakshya Upreti - 24001001070<br>
  Lavnish - 24001001071<br>
date:
---

1. Introduction

1.1 Purpose of the Software

The purpose of this document is to describe the functional and non‑functional requirements of the Airplane E‑Ticketing System.
This Software Requirement Specification (SRS) provides a clear understanding of system behavior, constraints, and expected functionality for developers, testers, and evaluators before system design and implementation.


---

1.2 Scope of the Software

The Airplane E‑Ticketing System is a web‑based application that allows passengers to search flights, book seats, make payments, receive electronic tickets, and cancel bookings.

The system also enables administrators to manage aircraft, airports, routes, flights, and reports within a single‑airline environment.

The project is developed using the Iterative and Incremental Software Development Model to ensure structured growth, modular implementation, and continuous validation.


---

1.3 Definitions, Acronyms, and Abbreviations

Term	Meaning

SRS	Software Requirement Specification
UI	User Interface
DB	Database
FK	Foreign Key
PNR	Passenger Name Record
E‑Ticket	Electronic flight ticket issued after booking
Admin	System administrator



---

2. Overall Description

2.1 Product Perspective

The system follows a client–server architecture with layered separation between:

Presentation layer (frontend user interface)

Application layer (backend APIs and business logic)

Data layer (MySQL for core data and MongoDB for logs)


This structure ensures security, scalability, and maintainability.


---

2.2 User Types

User Type	Description

Passenger	Searches flights, books tickets, makes payments, and cancels bookings
Admin	Manages aircraft, routes, flights, and system reports



---

2.3 Operating Environment

Web‑based system accessible through modern browsers

Backend server running API services

Relational database for transactional data

Document database for logs and audit trails



---

3. Functional Requirements

FR1 – User Registration and Login

The system shall allow users to register and log in securely.

Passwords shall be stored in encrypted form.


FR2 – Aircraft and Cabin Management

The admin shall define aircraft, seating capacity, and cabin classes.


FR3 – Airport and Route Management

The admin shall manage airports and define routes between them.


FR4 – Flight Scheduling

The admin shall create flights with assigned aircraft, routes, departure time, and arrival time.


FR5 – Flight Search

Users shall search flights using source airport, destination airport, and date.


FR6 – Seat Availability

The system shall display real‑time seat availability for each flight and cabin class.


FR7 – Booking Creation

Users shall book available seats on selected flights.

Each booking shall generate a unique booking record.


FR8 – Payment Processing

The system shall validate payment details using a simulated payment mechanism.

Booking confirmation shall occur only after successful payment.


FR9 – Ticket Generation

The system shall generate an electronic ticket linked to the booking.


FR10 – Ticket Cancellation

Users shall cancel bookings based on defined rules.

Seat availability shall update automatically after cancellation.


FR11 – Logging and Audit

The system shall record user activity, booking events, payment events, and system errors.


FR12 – Admin Reporting

The admin shall view booking statistics, payment summaries, and system usage reports.


FR13 - Airline Management

Admin shall create and manage multiple airlines.

Each flight shall belong to one airline.

Users shall be able to view and compare flights from different airlines on the same route



---

4. Non‑Functional Requirements

4.1 Performance

System response time shall generally be within 2–3 seconds.

Concurrent bookings shall not corrupt seat availability.


4.2 Security

Encrypted password storage.

Token‑based authentication.

Role‑based access for admin functions.


4.3 Reliability

Booking and payment data shall remain consistent.

System shall handle invalid operations gracefully.


4.4 Maintainability

Modular architecture shall support future enhancements.

Database design shall remain normalized and extensible.



---

5. System Requirements

5.1 Hardware Requirements

Desktop or laptop computer

Minimum Intel i3 processor

Minimum 4 GB RAM

Stable internet connection



---

5.2 Software Requirements

Frontend

HTML, CSS, JavaScript

Modern web framework (e.g., React)


Backend

Python‑based web framework

RESTful API architecture


Database

MySQL for core transactional data

MongoDB for logs and audit trails


Development Tools

Code editor

Version control system

API server runtime



---

6. Development Methodology

The project follows the Iterative and Incremental Model, where the system is developed in small functional modules such as authentication, flight management, booking, and payment.
Each iteration refines functionality and ensures early validation of requirements.


---

7. Future Scope

Integration with real payment gateways

Online check‑in and boarding pass generation

Multi‑airline aggregation support

Mobile application deployment

Dynamic fare pricing
