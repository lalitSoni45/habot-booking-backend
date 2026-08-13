HabotConnect - LSA Service Booking Backend

Position: Python Backend Developer Hiring Project
Candidate: Lalit Soni
Technology: Python, Django, Django REST Framework, PostgreSQL

1. Project Overview

This project is a backend prototype for an LSA (Learning Support
Assistant) Service Booking platform.

The platform connects parents with Learning Support Assistants (LSAs)
and provides backend APIs for:

Parent management

LSA profile management

Booking requests

LSA search and availability

Double-booking prevention

Payment webhook processing

Automated testing

Continuous Integration using GitHub Actions

The backend is built using Python, Django, Django REST Framework, and
PostgreSQL.

2. Problem Statement

The system needs to reliably manage booking requests between parents and
Learning Support Assistants.

The main backend challenges are:

Store booking information using a relational database.

Maintain relationships between parents, LSAs, bookings, and
payments.

Prevent overlapping bookings for the same LSA.

Search LSAs efficiently using skills and availability.

Avoid unnecessary database queries and the N+1 query problem.

Process payment success and failure events.

Update booking state based on payment events.

Validate API input and return meaningful HTTP status codes.

Automatically test the backend after code changes.

3. Features

Booking Management

Create a new booking.

Validate booking data.

Check LSA availability.

Prevent overlapping sessions.

Return appropriate HTTP status codes.

Store valid bookings in PostgreSQL.

LSA Search

Search LSAs using skills.

Filter active LSAs.

Check availability.

Use Django ORM for database operations.

Avoid unnecessary repeated database queries.

Payment Webhook

Receive payment events.

Accept transaction information.

Process payment success and failure.

Update the related booking state according to the payment result.

Automated Testing

The project contains automated tests covering the main backend
workflows:

Successful booking

Invalid booking data

Double booking

LSA search

Payment webhook

Continuous Integration

GitHub Actions automatically runs the Django test suite when code is
pushed to the repository.

4. Technology Stack

Technology              Purpose

Python                  Backend programming language
Django                  Web framework
Django REST Framework   REST API development
PostgreSQL              Relational database
Requests                External service integration
Django TestCase         Automated testing
Git                     Version control
GitHub Actions          Continuous Integration

5. Project Architecture

The project follows Django's MVT (Model-View-Template) architecture with
Django REST Framework for REST API development.

Client
   |
   | HTTP Request
   v
URL Configuration
   |
   v
Django View / DRF API View
   |
   v
Serializer / Validation
   |
   v
Business Logic
   |
   v
Django ORM
   |
   v
PostgreSQL
   |
   v
HTTP Response

Request Flow

POST /api/v1/bookings/
        |
        v
Validate request data
        |
        v
Check Parent and LSA
        |
        v
Check overlapping booking
        |
   +----+----+
   |         |
Overlap    Available
   |         |
   v         v
HTTP 409   Create Booking
             |
             v
         HTTP 201

6. MVC vs MVT Design Choice

Django MVT

Django uses the MVT (Model-View-Template) pattern.

Model: Represents database entities and relationships.

View: Handles requests, business logic, and responses.

Template: Generates HTML for traditional Django pages.

This project mainly exposes REST APIs, so Django REST Framework is used
to return JSON responses instead of traditional HTML pages.

Why Django + DRF?

Django and Django REST Framework were selected because they provide:

Built-in ORM

Database migrations

Request and response handling

Serializer validation

HTTP status code support

Structured application architecture

Good support for automated testing

7. Database Design

The project uses PostgreSQL as the relational database.

Parent

Field        Purpose

id           Primary key
name         Parent name
email        Parent email
phone        Parent phone
created_at   Creation timestamp

LSAProfile

Field         Purpose

id            Primary key
name          LSA name
email         LSA email
skills        Skills provided by the LSA
hourly_rate   LSA hourly rate
is_active     Whether the LSA is active
created_at    Creation timestamp

BookingRequest

Field        Purpose

id           Primary key
parent       Foreign key to Parent
lsa          Foreign key to LSAProfile
start_time   Session start time
end_time     Session end time
status       Current booking status
created_at   Creation timestamp

Payment

Field            Purpose

id               Primary key
booking          Related BookingRequest
transaction_id   External payment transaction ID
amount           Payment amount
status           Payment status
created_at       Creation timestamp

Relationships

Parent
   |
   | 1 : Many
   v
BookingRequest
   ^
   |
   | Many : 1
   |
LSAProfile

BookingRequest
   |
   | 1 : 1
   v
Payment

8. API Documentation

Base URL:

http://127.0.0.1:8000

8.1 Create Booking

Method: POST

Endpoint:

/api/v1/bookings/

Request:

{
    "parent": 1,
    "lsa": 1,
    "start_time": "2026-08-13T14:00:00Z",
    "end_time": "2026-08-13T15:00:00Z"
}

Success: HTTP 201 Created

{
    "id": 1,
    "parent": 1,
    "lsa": 1,
    "start_time": "2026-08-13T14:00:00Z",
    "end_time": "2026-08-13T15:00:00Z",
    "status": "PENDING",
    "created_at": "2026-08-13T..."
}

Invalid or missing required fields return HTTP 400 Bad Request.

If the LSA is already booked during an overlapping time:

HTTP 409 Conflict

{
    "error": "LSA is already booked during this time."
}

8.2 LSA Search

Method: GET

Endpoint:

/api/v1/lsas/search/

Example:

GET /api/v1/lsas/search/?skill=Mathematics

The endpoint searches active LSAs using the requested skill and
availability conditions.

Successful requests return HTTP 200 OK.

8.3 Payment Webhook

Method: POST

Endpoint:

/api/v1/payments/webhook/

Example:

{
    "booking_id": 1,
    "transaction_id": "TXN_10001",
    "status": "SUCCESS",
    "amount": "500.00"
}

The webhook processes the payment event and updates the related booking
state according to the payment result.

9. Double-Booking Prevention

The booking API checks whether the selected LSA already has an
overlapping booking.

The overlap condition is:

Existing start time < New end time
AND
Existing end time > New start time

Example:

Existing booking: 14:00 - 15:00
New booking:      14:30 - 15:30

Result: Overlap

The API rejects the request with HTTP 409 Conflict.

This protects data integrity and prevents two parents from receiving the
same LSA during overlapping sessions.

10. Query Optimization and N+1 Problem

What is the N+1 Problem?

The N+1 problem happens when an application first retrieves a list of
records and then performs another database query for each record.

1 query -> fetch N LSAs
N queries -> fetch related booking data
Total = N + 1 queries

This becomes inefficient as the number of LSAs increases.

Optimization Approach

The LSA search implementation uses Django ORM filtering and related-data
handling to keep database access efficient.

The main goals are:

Filter data at the database level.

Avoid querying related booking information repeatedly inside Python
loops.

Reduce unnecessary database round trips.

Keep the search endpoint scalable.

11. Payment Integration

The project includes integration with an external/mock payment
verification service using Python's requests library.

The integration is designed to:

Send a request to the external service.

Receive the payment verification result.

Handle successful and failed responses.

Handle request exceptions.

Log errors when external communication fails.

Update the booking/payment state based on the result.

Example:

Transaction ID: TXN_10001
Amount: 500.00
Status: SUCCESS

12. Automated Testing

The project contains automated tests for the main API and business
rules.

Test scenarios include:

Successful booking creation.

Invalid booking request.

Double-booking prevention.

LSA search.

Payment webhook processing.

Run tests with:

python manage.py test

The test suite helps detect regressions when backend code changes.

13. Continuous Integration

GitHub Actions is configured to run the test suite automatically when
code is pushed to the repository.

Workflow directory:

.github/workflows/

Typical workflow:

Developer pushes code
        |
        v
GitHub Actions starts
        |
        v
Checkout repository
        |
        v
Install dependencies
        |
        v
Run migrations / setup
        |
        v
Run automated tests
        |
        v
Pass / Fail result

14. Setup Instructions

Prerequisites

Python 3.13 or compatible Python version

PostgreSQL

Git

Step 1: Clone Repository

git clone https://github.com/lalitSoni45/habot-booking-backend.git
cd habot-booking-backend

Step 2: Create Virtual Environment

python -m venv venv

Step 3: Activate Virtual Environment

Windows PowerShell:

venv\Scripts\Activate.ps1

Step 4: Install Dependencies

pip install -r requirements.txt

Step 5: Configure PostgreSQL

Create the PostgreSQL database used by the project and configure the
database credentials in Django settings.

Example:

Database: habot_db
Host: localhost
Port: 5432
User: postgres

Do not commit database passwords or secret keys to Git.

Step 6: Run Migrations

python manage.py makemigrations
python manage.py migrate

Step 7: Run Development Server

python manage.py runserver

The development server will normally be available at:

http://127.0.0.1:8000/

15. Example Testing Flow

Step 1 --- Create Booking

POST /api/v1/bookings/

Expected:

HTTP 201 Created

Step 2 --- Try an Overlapping Booking

Send another booking for the same LSA with an overlapping time.

Expected:

HTTP 409 Conflict

Step 3 --- Search LSAs

GET /api/v1/lsas/search/

Expected:

HTTP 200 OK

Step 4 --- Send Payment Webhook

POST /api/v1/payments/webhook/

The payment event is processed and the related booking state is updated
according to the payment result.

16. Project Structure

habot-booking-backend/
|
+-- .github/
|   +-- workflows/
|
+-- booking/
|   +-- migrations/
|   +-- models.py
|   +-- serializers.py
|   +-- views.py
|   +-- urls.py
|   +-- tests.py
|
+-- config/
|   +-- settings.py
|   +-- urls.py
|
+-- .gitignore
+-- manage.py
+-- requirements.txt
+-- README.md

17. Security and Data Integrity

The project follows basic backend security practices:

Database credentials should not be committed to Git.

.env is excluded through .gitignore.

Virtual environment files are excluded from Git.

Invalid API input is rejected.

Booking conflicts are rejected.

Database relationships use foreign keys.

External service failures are handled.

Sensitive configuration should be provided through environment
variables in a production deployment.

18. Repository

GitHub Repository:

https://github.com/lalitSoni45/habot-booking-backend

19. Conclusion

This project demonstrates a Django-based backend for an LSA Service
Booking platform with:

Relational database design

Django ORM

RESTful APIs

Request validation

Double-booking prevention

LSA search

Payment webhook processing

External service integration

Automated testing

GitHub Actions Continuous Integration

The design focuses on reliability, maintainability, data integrity, and
efficient database access.
