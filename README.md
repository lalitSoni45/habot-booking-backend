# HabotConnect - LSA Service Booking Backend

**Position:** Python Backend Developer Hiring Project

**Candidate:** Lalit Soni

**Technology:** Python, Django, Django REST Framework, PostgreSQL

---

## 1. Project Overview

This project is a backend prototype for an LSA Service Booking platform.

The platform connects parents with Learning Support Assistants (LSAs) and provides backend APIs for:

- Parent management
- LSA profiles
- Booking requests
- LSA availability search
- Double-booking prevention
- Payment webhook processing
- Automated testing
- Continuous Integration using GitHub Actions

The backend is built using Python, Django, Django REST Framework, and PostgreSQL.

---

## 2. Problem Statement

The system needs to reliably manage booking requests between parents and Learning Support Assistants.

The main backend challenges are:

1. Store booking information using a relational database.
2. Prevent overlapping bookings for the same LSA.
3. Search available LSAs efficiently.
4. Avoid N+1 database queries.
5. Process payment success/failure events.
6. Automatically update booking status after payment.
7. Validate API input.
8. Automatically test the backend after code changes.

---

## 3. Features

### Booking Management

- Create a new booking.
- Validate booking data.
- Prevent overlapping sessions.
- Return appropriate HTTP status codes.

### LSA Search

- Search LSAs using skills.
- Filter active LSAs.
- Use optimized ORM queries.

### Payment Webhook

- Receive payment events.
- Accept transaction information.
- Process payment success/failure.
- Update booking status automatically.

### Automated Testing

The project contains automated tests covering:

- Successful booking
- Invalid booking data
- Double booking
- LSA search
- Payment webhook

### Continuous Integration

GitHub Actions automatically runs the Django test suite when code is pushed to the repository.

---

## 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming language |
| Django | Web framework |
| Django REST Framework | REST API development |
| PostgreSQL | Relational database |
| Requests | External service integration |
| Django TestCase | Automated testing |
| Git | Version control |
| GitHub Actions | Continuous Integration |

---

## 5. Project Architecture

The project follows Django's MVT architecture.

```text
Client
  |
  | HTTP Request
  ↓
URL Configuration
  |
  ↓
Django View
  |
  ↓
Serializer / Validation
  |
  ↓
Django ORM
  |
  ↓
PostgreSQL
  |
  ↓
HTTP Response