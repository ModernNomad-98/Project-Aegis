# Product specification — Clinic Appointment Tracker (v1)

This is the accepted v1 product specification referenced by the Scenario A
evidence fixtures (Decision `PS-006`). It is an immutable acceptance artifact:
the user accepts THIS content, and its SHA-256 is the anchor recorded in the
decision log. The Scenario A harness recomputes the digest and fails if it does
not match the pinned value, so the acceptance can be verified, not merely
asserted.

## Problem

A small physiotherapy clinic books appointments on paper. Slots get
double-booked, the front desk cannot see the whole day at a glance, and patients
forget appointments because there is no reminder.

## Users

- **Front-desk receptionist (internal)** — books, reschedules, and checks in
  patients.
- **Patient (external)** — receives a reminder with a link to their appointment
  time; does not log in.

## In scope for v1

1. **Book a 30-minute slot without double-booking.** A slot that is already
   taken cannot be booked again; the attempt is refused with a clear message.
2. **See the day and step to another.** The receptionist sees one day's slots at
   a glance and can move to the previous or next day.
3. **Mark arrived or no-show.** Each appointment can be marked "arrived" or
   "no-show" at check-in time.
4. **A reminder link that stops working after the appointment.** The patient
   reminder contains a link that shows the appointment time and stops working
   once the appointment time has passed.

## Explicitly out of scope for v1

- Online self-booking by patients, payments/billing, insurance, clinician
  scheduling optimization, and a mobile app.

## Acceptance criteria

- Booking an already-taken 30-minute slot is refused; no two appointments share
  one slot.
- The day view lists that day's appointments in time order and supports moving to
  the adjacent day.
- An appointment can be set to exactly one of: booked, arrived, no-show.
- A reminder link resolves to the appointment time before the appointment and
  returns "no longer available" afterwards.

## Done enough to ship (MVP)

A receptionist can book a non-conflicting 30-minute slot, view and navigate the
day, mark arrived/no-show, and the patient's reminder link works up to the
appointment time and then expires.
