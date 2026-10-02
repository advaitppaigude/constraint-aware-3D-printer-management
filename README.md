# Legacy minimum extract

This folder contains the minimum scheduling-relevant code reconstructed from
the final code listing in the uploaded A-Level NEA report.

Included:
- PrintJob metadata parsing and legacy priority state
- Printer scheduling state
- waitingRoom / printer job-pool filtering
- legacy optimiser

Intentionally omitted:
- GUI
- sockets / client-server request handling
- authentication and accounts
- teacher approval
- email
- database code
- cost/balance tracking
- file transfer
- serial printer control
- printer notifications
- shutdown/economical controls except where the old scheduler directly
  depended on the 16:00 school-day constraint

Important:
The PDF preserves the code text but not reliable source indentation. These
files therefore reconstruct indentation and a few obvious line wraps. They
should be treated as a reference extract, not a byte-for-byte copy of the
original source files.
