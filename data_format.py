# Example simplified data
UFS = {
    "UF1": {
        "code": "TC1028",
        "type": "materia",
        "periods": ["PMT1", "PMT2"],
        "UdC": 2,
        "modules": {1: 40},
        "semester": 1
    },
    "UF2": {
        "code": "TC3002B",
        "type": "bloque",
        "periods": ["PMT2", "PMT3"],
        "UdC": 3,
        "modules": {1: 20, 2: 20},
        "semester": 2
    },
    "UF3": {
        "code": "TC1001A",
        "type": "semana Tec",
        "periods": ["PMT1", "PMT2", "PMT3"],
        "UdC": 1,
        "modules": {1: 20},
        "semester": 1
    }
}

professors = {
    "Professor1": {
        "type": "planta",
        "availability": {
            "Monday": ["9-11", "13-15"],
            "Tuesday": ["9-11"],
            "Wednesday": ["13-15"],
            "Thursday": ["9-11", "13-15"],
            "Friday": ["9-11"]
        },
        "modules": {1, 2},
        "min_workload": 2,
        "max_workload": 5
    },
    "Professor2": {
        "type": "cátedra",
        "availability": {
            "Monday": ["9-11", "13-15"],
            "Tuesday": ["9-11"],
            "Wednesday": ["13-15"],
            "Thursday": ["9-11", "13-15"],
            "Friday": ["9-11"]
        },
        "modules": {1},
        "min_workload": 1,
        "max_workload": 3
    },
    "Professor3": {
        "type": "planta",
        "availability": {
            "Monday": ["9-11", "13-15"],
            "Tuesday": ["9-11"],
            "Wednesday": ["13-15"],
            "Thursday": ["9-11", "13-15"],
            "Friday": ["9-11"]
        },
        "modules": {1, 2},
        "min_workload": 2,
        "max_workload": 5
    }
}