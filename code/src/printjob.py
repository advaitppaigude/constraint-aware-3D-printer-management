# printjob.py

class PrintJob:
    def __init__(
        self,
        job_id,
        user_id,
        duration,
        material,
        colour=None,
    ):
        self.job_id = job_id
        self.user_id = user_id
        self.duration = duration
        self.material = material
        self.colour = colour
