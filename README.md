# constraint-aware-3D-printer-management
Constraint-aware scheduling and printer management for shared 3D printing environments, currently being adapted for the ICRS lab.

# 3D Printer Scheduling System

A constraint-aware scheduling and printer-management system for shared 3D printing environments.

This project began as a multi-user 3D printer management system developed for a school workshop with six FDM printers. It is now being reworked into a smaller, more practical scheduling layer for use in the Imperial College Robotics Society (ICRS) lab.

> **Status:** active rewrite / prototype  
> The original implementation is being used as a reference while the system is redesigned around the ICRS workflow.

## What the original system did

The original system was designed around a school Design Technology department where staff had to coordinate many student print jobs across six Creality Ender 5 printers.

It included:

- multi-user client/server communication;
- printer and job state tracking;
- constraint-aware job-to-printer matching;
- print scheduling based on duration, remaining filament and printer configuration;
- support for fixed or flexible filament colour/material preferences;
- queue-time-based job priority;
- higher weighting for deadline-sensitive assessed work;
- G-code metadata extraction for:
  - estimated print duration,
  - filament usage,
  - model dimensions,
  - layer height,
  - quality settings,
  - infill density;
- SQLite persistence for users, printers and completed jobs;
- printer control over serial;
- file transfer between clients and server;
- print-completion/error notifications;
- teacher approval and cost/balance tracking.

The scheduling logic maintained a pool of pending jobs, filtered jobs according to printer constraints, and selected suitable work based on the remaining time and filament available on each machine.

## Why it is being rewritten

The ICRS lab already has a much cleaner access-control workflow than the environment the original project targeted.

ICRS currently uses:

- a modified fork of Orca Slicer;
- a custom Imperial card scanner;
- server-side checks for induction status and user permissions;
- a maximum print duration of approximately three hours;
- a self-service workflow where inducted members load filament, start prints and clear beds themselves.

There is also a strict no-coursework rule, so the lab does not need deadline- or coursework-based priority scheduling. Printer access is effectively first-come, first-served.

That means a large part of the original application is unnecessary.

The rewrite therefore focuses on the part that is still useful: **matching jobs to suitable printers while preserving a simple first-come-first-served workflow**.

## Rewrite goals

The current prototype is intended to explore whether a lightweight scheduling layer can reduce clashes and manual coordination without replacing the existing ICRS access-control system.

The initial scope is:

- keep first-come-first-served behaviour;
- track printer availability;
- track printer/material configuration;
- match jobs to compatible printers;
- account for print duration;
- avoid assigning jobs to unsuitable machines;
- provide a clear view of queued jobs and printer state;
- keep filament loading and bed clearing manual;
- remain separate from the existing ICRS production setup during prototyping.

The prototype will only be integrated further if it provides a meaningful improvement over the current workflow.

## What is being removed

The rewrite intentionally drops features that were specific to the school deployment:

- teacher approval queues;
- student/teacher account roles;
- coursework/NEA priority weighting;
- school-day shutdown constraints;
- balance and cost accounting;
- email-based password reset;
- direct responsibility for access control;
- assumptions that a central operator clears beds or changes filament.

This is a redesign around a different operating environment, not a line-for-line refactor of the original coursework.

## Current design direction

The rewritten system is being kept deliberately small.

The core model is expected to consist of:

### `PrintJob`

Stores the information needed for scheduling, such as:

- submission time;
- estimated print duration;
- requested material/filament;
- any printer compatibility constraints;
- current queue state.

Where useful, metadata can be extracted directly from generated G-code.

### `Printer`

Stores the current state of a printer:

- availability;
- material/filament configuration;
- current job;
- compatibility/capability information.

### Scheduler

The scheduler will:

1. consider jobs in first-come-first-served order;
2. determine which printers are compatible;
3. avoid assigning work to unavailable or unsuitable machines;
4. return an assignment or leave the job queued until a suitable printer is available.

The objective is not to create a complex optimisation system for its own sake. The scheduler should only add enough logic to reduce contention while remaining predictable to users.

## Development approach

The original implementation is being treated as a reference implementation rather than a codebase that must be preserved.

Useful domain logic will be carried over where appropriate, but school-specific infrastructure and unnecessary complexity will be removed rather than refactored.

Near-term work:

- [x] Review the original scheduling and printer-management implementation
- [x] Define the ICRS-specific problem and remove school-specific requirements
- [ ] Define the minimal job and printer data models
- [ ] Rewrite the scheduling core
- [ ] Add a lightweight queue/printer-state interface
- [ ] Test with representative multi-printer scenarios
- [ ] Review the prototype against the current ICRS workflow
- [ ] Investigate integration with the existing system if the prototype proves useful

## Background

The original project was developed as an A-Level Computer Science NEA and received full marks.

The current rewrite is focused on turning that academic prototype into a smaller system shaped by a real operational environment: fewer assumptions, less infrastructure, and a clearer boundary between access control, user actions and scheduling.

## Repository note

During the rewrite, legacy code may be retained for reference while new components are introduced separately. The target architecture should be judged against the current ICRS use case rather than the structure of the original implementation.
