from print_job import PrintJob
from printer import Printer


MAX_PRINT_DURATION_SECONDS = 3 * 60 * 60


class Scheduler:
    """
    FCFS constraint-aware printer assignment.

    A printer is feasible for a job only if:
    - the job is within the ICRS three-hour limit
    - the printer is available
    - the printer supports the required material
    - the job fits within the printer's build volume
    - enough filament remains for the job

    The scheduler then assigns the earliest submitted job to the first
    compatible available printer
    """

    def is_job_valid(self, job: PrintJob) -> bool:
        return 0 < job.duration <= MAX_PRINT_DURATION_SECONDS

    def compatible(self, job: PrintJob, printer: Printer) -> bool:
        return (
            self.is_job_valid(job)
            and printer.available
            and printer.supports_material(job.material)
            and job.fits_within(printer.build_volume)
            and printer.has_enough_filament(job.filament_required_g)
        )

    def assign(self, jobs: list[PrintJob], printers: list[Printer]):
        assignments: list[tuple[PrintJob, Printer]] = []
        unassigned: list[PrintJob] = []

        # submission time is the source of ordering - no longer priority weighting
        ordered_jobs = sorted(jobs, key=lambda job: job.submitted_at)

        for job in ordered_jobs:
            assigned_printer = None

            for printer in printers:
                if self.compatible(job, printer):
                    assigned_printer = printer
                    break

            if assigned_printer is None:
                unassigned.append(job)
                continue

            assignments.append((job, assigned_printer))
            assigned_printer.available = False
            assigned_printer.filament_remaining_g -= job.filament_required_g

        return assignments, unassigned
