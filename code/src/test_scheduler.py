# test_scheduler.py

compatibility_tests = [
    ("J1", "P1", True),
    ("J1", "P2", False),
    ("J3", "P3", True),
    ("J3", "P1", False),
    ("J6", "P4", False),
    ("J7", "P2", True),
    ("J8", "P2", False),
    ("J9", "P1", False),
    ("J10", "P1", False),
    ("J10", "P3", True),
]

test_struct = {
    "printers": [
        {
            "id": "P1",
            "materials": ["PLA", "PETG"],
            "volume": [220, 220, 250]
        },
        {
            "id": "P2",
            "materials": ["PLA"],
            "volume": [180, 180, 180]
        },
        {
            "id": "P3",
            "materials": ["PLA", "ABS"],
            "volume": [300, 300, 300]
        },
        {
            "id": "P4",
            "materials": ["PETG"],
            "volume": [150, 150, 150]
        }
    ],

    "jobs": [
        {
            "id": "J1",
            "material": "PETG",
            "size": [100, 100, 80],
            "duration": 7200,
            "priority": 3
        },
        {
            "id": "J2",
            "material": "PLA",
            "size": [170, 170, 150],
            "duration": 3600,
            "priority": 1
        },
        {
            "id": "J3",
            "material": "ABS",
            "size": [200, 200, 200],
            "duration": 5400,
            "priority": 2
        },
        {
            "id": "J4",
            "material": "PLA",
            "size": [250, 250, 200],
            "duration": 8000,
            "priority": 4
        },
        {
            "id": "J5",
            "material": "PETG",
            "size": [140, 140, 140],
            "duration": 3000,
            "priority": 2
        },
        {
            "id": "J6",
            "material": "PETG",
            "size": [160, 160, 160],
            "duration": 4500,
            "priority": 1
        },
        {
            "id": "J7",
            "material": "PLA",
            "size": [175, 175, 175],
            "duration": 2500,
            "priority": 1
        },
        {
            "id": "J8",
            "material": "PLA",
            "size": [181, 181, 181],
            "duration": 2500,
            "priority": 1
        },
        {
            "id": "J9",
            "material": "TPU",
            "size": [100, 100, 100],
            "duration": 2000,
            "priority": 1
        },
        {
            "id": "J10",
            "material": "PLA",
            "size": [100, 100, 260],
            "duration": 4000,
            "priority": 2
        }
    ]
}


