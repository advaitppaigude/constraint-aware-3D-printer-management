from datetime import datetime, timedelta

from src.print_job import PrintJob
from src.printer import Printer
from src.scheduler import Scheduler


BASE_TIME = datetime(2026, 10, 2, 12, 0, 0)


test_struct = {
    "printers": [
        {
            "id": "P1",
            "materials": ["PLA", "PETG"],
            "build_volume": [220, 220, 250],
            "filament_remaining_g": 420,
            "available": True,
        },
        {
            "id": "P2",
            "materials": ["PLA"],
            "build_volume": [180, 180, 180],
            "filament_remaining_g": 180,
            "available": True,
        },
        {
            "id": "P3",
            "materials": ["PLA", "ABS"],
            "build_volume": [300, 300, 300],
            "filament_remaining_g": 750,
            "available": True,
        },
        {
            "id": "P4",
            "materials": ["PETG"],
            "build_volume": [150, 150, 150],
            "filament_remaining_g": 90,
            "available": True,
        },
    ],
    "jobs": [
        {
            "id": "J1",
            "material": "PETG",
            "size": [100, 100, 80],
            "duration": 7200,
            "filament_required_g": 120,
            "submitted_at": BASE_TIME,
        },
        {
            "id": "J2",
            "material": "PLA",
            "size": [170, 170, 150],
            "duration": 3600,
            "filament_required_g": 80,
            "submitted_at": BASE_TIME + timedelta(minutes=1),
        },
        {
            "id": "J3",
            "material": "ABS",
            "size": [200, 200, 200],
            "duration": 5400,
            "filament_required_g": 160,
            "submitted_at": BASE_TIME + timedelta(minutes=2),
        },
        {
            "id": "J4",
            "material": "PLA",
            "size": [250, 250, 200],
            "duration": 8000,
            "filament_required_g": 300,
            "submitted_at": BASE_TIME + timedelta(minutes=3),
        },
        {
            "id": "J5",
            "material": "PETG",
            "size": [140, 140, 140],
            "duration": 3000,
            "filament_required_g": 95,
            "submitted_at": BASE_TIME + timedelta(minutes=4),
        },
        {
            "id": "J6",
            "material": "PETG",
            "size": [160, 160, 160],
            "duration": 4500,
            "filament_required_g": 70,
            "submitted_at": BASE_TIME + timedelta(minutes=5),
        },
        {
            "id": "J7",
            "material": "PLA",
            "size": [175, 175, 175],
            "duration": 2500,
            "filament_required_g": 60,
            "submitted_at": BASE_TIME + timedelta(minutes=6),
        },
        {
            "id": "J8",
            "material": "PLA",
            "size": [181, 181, 181],
            "duration": 2500,
            "filament_required_g": 60,
            "submitted_at": BASE_TIME + timedelta(minutes=7),
        },
        {
            "id": "J9",
            "material": "TPU",
            "size": [100, 100, 100],
            "duration": 2000,
            "filament_required_g": 40,
            "submitted_at": BASE_TIME + timedelta(minutes=8),
        },
        {
            "id": "J10",
            "material": "PLA",
            "size": [100, 100, 260],
            "duration": 4000,
            "filament_required_g": 110,
            "submitted_at": BASE_TIME + timedelta(minutes=9),
        },
        {
            "id": "J11",
            "material": "PLA",
            "size": [100, 100, 100],
            "duration": 10801,
            "filament_required_g": 50,
            "submitted_at": BASE_TIME + timedelta(minutes=10),
        },
        {
            "id": "J12",
            "material": "PETG",
            "size": [120, 120, 120],
            "duration": 1800,
            "filament_required_g": 100,
            "submitted_at": BASE_TIME + timedelta(minutes=11),
        },
    ],
}


def make_printers():
    return [
        Printer(
            printer_id=p["id"],
            materials=tuple(p["materials"]),
            build_volume=tuple(p["build_volume"]),
            filament_remaining_g=p["filament_remaining_g"],
            available=p["available"],
        )
        for p in test_struct["printers"]
    ]


def make_jobs():
    return [
        PrintJob(
            job_id=j["id"],
            material=j["material"],
            size=tuple(j["size"]),
            duration=j["duration"],
            filament_required_g=j["filament_required_g"],
            submitted_at=j["submitted_at"],
        )
        for j in test_struct["jobs"]
    ]


def get_job(job_id):
    return next(job for job in make_jobs() if job.job_id == job_id)


def get_printer(printer_id):
    return next(
        printer for printer in make_printers()
        if printer.printer_id == printer_id
    )


def test_material_constraint():
    scheduler = Scheduler()
    assert scheduler.compatible(get_job("J1"), get_printer("P1"))
    assert not scheduler.compatible(get_job("J1"), get_printer("P2"))


def test_build_volume_constraint():
    scheduler = Scheduler()
    assert scheduler.compatible(get_job("J7"), get_printer("P2"))
    assert not scheduler.compatible(get_job("J8"), get_printer("P2"))
    assert not scheduler.compatible(get_job("J10"), get_printer("P1"))
    assert scheduler.compatible(get_job("J10"), get_printer("P3"))


def test_filament_constraint():
    scheduler = Scheduler()
    assert not scheduler.compatible(get_job("J5"), get_printer("P4"))
    assert scheduler.compatible(get_job("J6"), get_printer("P1"))
    assert not scheduler.compatible(get_job("J12"), get_printer("P4"))


def test_unsupported_material():
    scheduler = Scheduler()
    assert not any(
        scheduler.compatible(get_job("J9"), printer)
        for printer in make_printers()
    )


def test_three_hour_limit():
    scheduler = Scheduler()
    assert scheduler.is_job_valid(get_job("J1"))
    assert not scheduler.is_job_valid(get_job("J11"))


def test_unavailable_printer():
    scheduler = Scheduler()
    printer = get_printer("P1")
    printer.available = False
    assert not scheduler.compatible(get_job("J1"), printer)


def test_fcfs_order_is_used():
    scheduler = Scheduler()

    printer = Printer(
        printer_id="P1",
        materials=("PLA",),
        build_volume=(220, 220, 250),
        filament_remaining_g=500,
        available=True,
    )

    earlier = PrintJob(
        job_id="EARLY",
        material="PLA",
        size=(100, 100, 100),
        duration=1200,
        filament_required_g=50,
        submitted_at=BASE_TIME,
    )

    later = PrintJob(
        job_id="LATE",
        material="PLA",
        size=(100, 100, 100),
        duration=1200,
        filament_required_g=50,
        submitted_at=BASE_TIME + timedelta(minutes=1),
    )

    # Deliberately pass them in reverse order.
    assignments, unassigned = scheduler.assign(
        [later, earlier],
        [printer],
    )

    assert assignments[0][0].job_id == "EARLY"
    assert [job.job_id for job in unassigned] == ["LATE"]


def test_assignment_updates_printer_state():
    scheduler = Scheduler()

    printer = Printer(
        printer_id="P1",
        materials=("PLA",),
        build_volume=(220, 220, 250),
        filament_remaining_g=200,
        available=True,
    )

    job = PrintJob(
        job_id="J",
        material="PLA",
        size=(100, 100, 100),
        duration=1200,
        filament_required_g=75,
        submitted_at=BASE_TIME,
    )

    assignments, _ = scheduler.assign([job], [printer])

    assert len(assignments) == 1
    assert printer.available is False
    assert printer.filament_remaining_g == 125
