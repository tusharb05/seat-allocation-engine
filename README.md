# Seat Allocation Engine

**Stack:** Redis (advisory locks (leases)), PostgreSQL (truth), FastAPI (API), Docker Compose (deployment)  
**Focus:** Concurrency correctness, idempotency, atomic multi-seat booking, load-tested under race conditions.

This project is intentionally backend-heavy. There is no UI, no auth, and no payments.  
The goal is to solve **seat allocation under concurrency** correctly and prove it with load tests.

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Core Design Principles](#core-design-principles)
- [Data Model & Constraints](#data-model--constraints)
- [Booking Flow](#booking-flow)
- [Deployment](#deployment)
- [Load Testing Strategy](#load-testing-strategy)
- [Locust Tests Summary](#locust-tests-summary)
- [Database Verification](#database-verification)
- [Key Engineering Takeaways](#key-engineering-takeaways)
- [Resume Highlights](#resume-highlights)

---

## Architecture Overview

The system is split into **coordination** and **truth** layers:

- **Redis** is used only for *advisory locking* with TTL.
- **PostgreSQL** is the *single source of truth*.
- **FastAPI** exposes HTTP endpoints.
- **Docker Compose** runs everything locally in isolated containers.

Redis helps reduce contention.  
Postgres enforces correctness.

If Redis lies, Postgres corrects it.

---

## Core Design Principles

1. **Redis is advisory, not authoritative**
2. **Postgres enforces invariants**
3. **All booking commits are transactional**
4. **Idempotency is explicit and enforced at DB level**
5. **High rejection rate under load is expected and correct**
6. **No partial state is ever committed**

---


### Why this works

- Redis handles fast, distributed coordination.
- PostgreSQL guarantees atomicity and consistency.
- Row-level locks (`SELECT ... FOR UPDATE`) prevent double booking.
- TTL prevents deadlocks if clients crash.

---

## Data Model & Constraints

### seats

| column   | type    |
|---------|---------|
| id      | varchar |
| show_id | varchar |
| status  | enum (`AVAILABLE`, `BOOKED`) |

### bookings

| column      | type    |
|------------|---------|
| id         | uuid    |
| show_id    | varchar |
| seat_id    | varchar |
| user_id    | uuid    |
| request_id | uuid    |

### Constraints 

```sql
ALTER TABLE bookings
ADD CONSTRAINT uq_booking_request_seat
UNIQUE (request_id, seat_id);
```

This allows:

- One request_id → multiple seats
- Safe retries
- No duplicate seat booking


---


## Booking Flow


### 1. Seat Lock (Redis)

```
POST /seat-lock
{
  show_id,
  seat_ids,
  user_id
}
```

- Redis keys: lock:{show_id}:{seat_id}
- TTL-based
- Failure returns 409

### 2. Confirm Booking (Postgres)

```
POST /booking/confirm
{
  show_id,
  seat_ids,
  user_id,
  request_id
}
```

#### Inside one DB transaction:

- Verify Redis locks

- SELECT seats FOR UPDATE

- Idempotency check

- Invariant check (all seats AVAILABLE)

- Mark seats BOOKED

- Insert bookings

- Commit

#### Guarantees:

- Atomic multi-seat booking

- No partial commits

- No double booking

---


## Load Testing Strategy

All load tests were done using Locust.

#### Key points:

- High concurrency

- Short TTLs

- Aggressive ramp-up

- Focus on correctness, not throughput

A high failure rate is expected and desired.


---


## Locust Test Summary

## Locust Tests Summary



| # | Test Name                     | What It Validates          | Seats | Users    | Ramp-up | Runtime | TTL   | Screenshot             |
|---|------------------------------|----------------------------|-------|----------|---------|---------|-------|-------------------------|
| 1 | Lock Contention              | Mutual exclusion           | A1    | 50       | 1/sec   | 2m      | 120s  | assets/test1.png        |
| 2 | Lock TTL Expiry              | Lock auto-release          | A1    | 50       | 1/sec   | 1m      | 5s    | assets/test2.png        |
| 3 | High Ramp-up Lock Race       | Atomic locking             | A1    | 50       | 10/sec  | 1m      | 5s    | assets/test3.png        |
| 4 | Confirm Race (Single Seat)   | DB truth beats Redis       | A1    | 20       | 5/sec   | 1m      | 1s    | assets/test4.png        |
| 5 | Confirm Race (Multi-seat)    | Atomic commit              | A2,A3 | 20       | 5/sec   | 1m      | 1s    | assets/test5.png        |


---

## Key Engineering Takeaways

- Redis is not trusted with correctness

- DB constraints are non-negotiable

- Idempotency must be designed, not assumed

- Returning from inside DB transactions is dangerous

- Load testing reveals bugs unit tests never will

- High failure rate ≠ broken system