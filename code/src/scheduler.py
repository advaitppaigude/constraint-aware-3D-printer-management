# scheduler.py

class Scheduler:
    def compatible(self, job, printer):
        if not printer.available:
            return False

        if job.material != printer.material:
            return False

        if job.colour is not None and job.colour != printer.colour:
            return False

        return True

    def assign(self, jobs, printers):
        assignments = []

        for job in jobs:  # preserves FCFS
            for printer in printers:
                if self.compatible(job, printer):
                    assignments.append((job, printer))
                    printer.available = False
                    break

        return assignments
