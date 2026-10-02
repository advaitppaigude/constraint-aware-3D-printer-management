from dataclasses import dataclass


@dataclass
class Printer:
    """
    Printer state relevant to scheduling.

    This intentionally excludes access control, direct printer control and
    user-management concerns because they are already handled elsewhere
    in the ICRS workflow.
    """

    printer_id: str
    materials: tuple[str, ...]
    build_volume: tuple[int, int, int]
    filament_remaining_g: float
    available: bool = True

    def supports_material(self, material: str) -> bool:
        return material in self.materials

    def has_enough_filament(self, required_g: float) -> bool:
        return self.filament_remaining_g >= required_g
