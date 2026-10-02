from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class PrintJob:
    """
    Minimal scheduling model for the ICRS rewrite:

    - Jobs are ordered by submission time to preserve first-come-first-served
    behaviour
    
    - Duration is stored in seconds and dimensions in millimetres
    """

    job_id: str
    material: str
    size: tuple[int, int, int]
    duration: int
    filament_required_g: float
    submitted_at: datetime

    def fits_within(self, build_volume: tuple[int, int, int]) -> bool:
        return all(
            job_dimension <= printer_dimension
            for job_dimension, printer_dimension in zip(self.size, build_volume)
        )
