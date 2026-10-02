# test_scheduler.py


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
    }
  ]
}



