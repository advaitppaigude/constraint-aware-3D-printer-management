# Constraint-Aware 3D Printer Management

A constraint-aware scheduling and printer-management system for shared 3D printing environments.

This project began as a multi-user 3D printer management system developed for a school workshop with six FDM printers. It is now being reworked into a smaller scheduling layer for potential use in the Imperial College Robotics Society (ICRS) lab.

> **Status:** active rewrite / prototype  
> The original implementation is retained as a legacy reference while the scheduling core is redesigned around the ICRS workflow.

## Original system

The original system was built for a school Design Technology department where staff had to coordinate many student print jobs across six Creality Ender 5 printers.

It included:

- multi-user client/server communication;
- printer and job state tracking;
- constraint-aware job-to-printer matching;
- scheduling based on printer availability, print duration, filament requirements and printer configuration;
- fixed or flexible filament colour/material preferences;
- G-code metadata extraction for:
  - estimated print duration,
  - filament usage,
  - model dimensions,
  - layer height,
  - quality settings,
  - infill density;
- SQLite persistence for users, printers and completed jobs;
- direct printer control over serial;
- file transfer between clients and server;
- print-completion and error notifications;
- teacher approval and cost/balance tracking;
- queue-time and coursework-specific priority rules.

Those features were useful for the original environment, but many do not map cleanly onto ICRS.

## ICRS context

ICRS already has an established access-control workflow based around:

- a modified fork of Orca Slicer;
- a custom Imperial card scanner;
- server-side induction and permission checks;
- a maximum print duration of approximately three hours;
- a self-service workflow where inducted members load filament, start prints and clear beds themselves.

ICRS also operates on a first-come-first-served basis, with a strict no-coursework rule.

Because of this, the rewrite does **not** attempt to replace authentication, user priority levels, induction checks or printer access control. It focuses only on the scheduling problem that may still be useful on top of the existing setup.

## Rewrite goals

The current prototype is intended to test whether a lightweight scheduling layer can reduce clashes and manual coordination while preserving the existing ICRS workflow.

The current scheduling model considers:

- first-come-first-served submission order;
- printer availability;
- supported filament/material types;
- printer build volume;
- job dimensions;
- remaining filament on each printer;
- filament required by each job;
- the three-hour ICRS print-duration limit.

A job is only considered compatible with a printer if all relevant constraints are satisfied.

The prototype is deliberately separate from the current ICRS production setup. Further integration only makes sense if the scheduling layer provides a meaningful improvement over the existing workflow.

## Current data model

### `PrintJob`

Each print job currently stores:

- `job_id`
- required `material`
- model `size` as `(x, y, z)` dimensions in millimetres
- estimated `duration` in seconds
- `filament_required_g`
- `submitted_at`

`submitted_at` is used to preserve first-come-first-served ordering. There is no priority score in the ICRS rewrite.

### `Printer`

Each printer currently stores:

- `printer_id`
- supported `materials`
- `build_volume`
- `filament_remaining_g`
- current `available` state

This is intentionally limited to state that affects scheduling.

### `Scheduler`

The scheduler currently:

1. orders jobs by submission time;
2. rejects jobs that exceed the three-hour duration limit;
3. checks printer availability;
4. checks material compatibility;
5. checks that the job fits within the printer build volume;
6. checks that sufficient filament remains;
7. assigns the earliest compatible job to an available printer;
8. marks that printer unavailable and deducts the job's filament requirement.

This provides a simple, predictable FCFS scheduler while still respecting real printer constraints.

## Repository structure

```text
code/
├── legacy/
│   ├── printjob.py
│   ├── printer.py
│   ├── scheduler.py
│   └── optimiser.py
├── src/
│   ├── __init__.py
│   ├── print_job.py
│   ├── printer.py
│   └── scheduler.py
└── tests/
    ├── __init__.py
    └── test_scheduler.py
```

### `code/legacy/`

Contains the minimum scheduling-relevant portion of the original A-Level implementation.

It is retained for reference only and is not the basis of the new architecture.

### `code/src/`

Contains the current ICRS-oriented rewrite.

### `code/tests/`

Contains representative multi-printer test scenarios covering:

- material compatibility;
- build-volume constraints;
- insufficient filament;
- unsupported materials;
- unavailable printers;
- the three-hour duration limit;
- first-come-first-served ordering;
- printer-state updates after assignment.

## What is being removed

The rewrite intentionally drops features that were specific to the school deployment:

- teacher approval queues;
- student/teacher account roles;
- coursework/NEA priority weighting;
- school-day shutdown rules;
- balance and cost accounting;
- email-based password reset;
- direct responsibility for access control;
- assumptions that a central operator clears beds or changes filament.

This is a redesign around a different operating environment, not a line-for-line refactor of the original coursework.

## Development approach

The original implementation is being treated as a reference implementation rather than a codebase that must be preserved.

Useful scheduling concepts are being carried over where appropriate, while school-specific infrastructure is removed.

Near-term work:

- [x] Review the original scheduling and printer-management implementation
- [x] Define the ICRS-specific problem
- [x] Remove priority-based scheduling
- [x] Define the minimal job and printer data models
- [x] Implement initial FCFS constraint checking
- [x] Add representative scheduler tests
- [ ] Refine printer selection when several compatible printers are available
- [ ] Decide how filament state should be updated in the real ICRS workflow
- [ ] Add G-code metadata extraction where useful
- [ ] Add a lightweight queue/printer-state interface
- [ ] Review the prototype against the current ICRS workflow
- [ ] Investigate integration with the existing system if the prototype proves useful

## Background

The original project was developed as an A-Level Computer Science NEA and received full marks.

The current rewrite is focused on turning that academic prototype into a smaller system shaped by a real operational environment: fewer assumptions, less infrastructure, and a clearer separation between access control, user actions and scheduling.
