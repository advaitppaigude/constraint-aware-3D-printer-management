# printer.py

class Printer:
    def __init__(
        self,
        printer_id,
        material,
        colour=None,
        available=True,
    ):
        self.printer_id = printer_id
        self.material = material
        self.colour = colour
        self.available = available
