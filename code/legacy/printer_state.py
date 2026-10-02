class Printer:
    """
    Scheduling-relevant state extracted from the original Printer class.

    Serial control, email notifications, database access, economical settings,
    and direct printer execution have intentionally been omitted.
    """

    def __init__(self, printerNumber):
        self.printerNumber = printerNumber
        self.jobPool = []
        self.status = "Free"
        self.colour = ""
        self.type = ""
        self.remainingLength = 0.0
        self.currentJob = None
