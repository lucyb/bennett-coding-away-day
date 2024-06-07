import csv
import itertools
import random
from datetime import datetime, timedelta

N_PATIENTS = 3000


# Generate N patients with uniform sex distribution, age, and 10% dead


def generate_patient(patient_id):
    patient = {"patient_id": patient_id}
    patient["sex"] = random.choice(["male", "female"])

    year_of_birth = random.randint(1920, 2020)
    month_of_birth = str(random.randint(1, 12)).zfill(2)
    day_of_birth = str(random.randint(1, 28)).zfill(2)
    patient["date_of_birth"] = f"{year_of_birth}-{month_of_birth}-{day_of_birth}"

    year_of_death = random.randint(year_of_birth + 1, 2023)
    month_of_death = str(random.randint(1, 12)).zfill(2)
    day_of_death = str(random.randint(1, 28)).zfill(2)
    patient["date_of_death"] = random.choice(
        [
            f"{year_of_death}-{month_of_death}-{day_of_death}",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]
    )
    return patient


patients = [generate_patient(patient_id) for patient_id in range(1, N_PATIENTS + 1)]

# Give every patient a practice registration lasting their whole life

nuts1 = [
    "North East",
    "North West",
    "Yorkshire and The Humber",
    "East Midlands",
    "West Midlands",
    "East",
    "London",
    "South East",
    "South West",
]


def generate_practice_registration(patient):
    practice_registration = {"patient_id": patient["patient_id"]}
    practice_registration["start_date"] = patient["date_of_birth"]
    practice_registration["end_date"] = patient["date_of_death"]
    practice_registration["practice_stp"] = (
        f"E54{str(random.randint(1, 999999)).zfill(6)}"
    )
    practice_registration["practice_nuts1_region_name"] = random.choice(nuts1)
    return practice_registration


practice_registrations = [
    generate_practice_registration(patient) for patient in patients
]


def clinical_event_date(patient):
    year_of_birth = int(patient["date_of_birth"][:4])
    year_of_death = (
        int(patient["date_of_death"][:4]) if patient["date_of_death"] else 2023
    )
    month_of_death = (
        int(patient["date_of_death"][5:7]) if patient["date_of_death"] else 12
    )
    day_of_death = (
        int(patient["date_of_death"][-2:]) if patient["date_of_death"] else 28
    )
    year = random.randint(year_of_birth + 1, year_of_death)
    month = str(random.randint(1, month_of_death)).zfill(2)
    day = str(random.randint(1, day_of_death)).zfill(2)
    return f"{year}-{month}-{day}"


def clinical_event(patient, snomedct_code):
    clinical_event = {"patient_id": patient["patient_id"]}
    clinical_event["date"] = clinical_event_date(patient)
    clinical_event["snomedct_code"] = snomedct_code
    clinical_event["ctv3_code"] = None
    clinical_event["numeric_value"] = None
    return clinical_event


# add clinical events

clinical_events = []


def vampire_bite(victim):
    human_bite_of_neck = 283695002
    if victim["date_of_death"]:
        if victim["date_of_birth"][:4] == victim["date_of_death"][:4]:
            halloween_year = victim["date_of_birth"]
        elif (
            int(victim["date_of_birth"][:4]) + 1 == int(victim["date_of_death"][:4]) - 1
        ):
            halloween_year = victim["date_of_birth"]
        else:
            halloween_year = random.randint(
                int(victim["date_of_birth"][:4]) + 1,
                int(victim["date_of_death"][:4]) - 1,
            )
    else:
        halloween_year = random.randint(
            int(victim["date_of_birth"][:4]) + 1,
            2022,
        )

    halloween = f"{halloween_year}-{10}-{31}"

    clinical_event = {"patient_id": victim["patient_id"]}
    dates = list(itertools.repeat(halloween, 11)) + [clinical_event_date(victim)]
    clinical_event["date"] = random.choice(dates)
    clinical_event["snomedct_code"] = human_bite_of_neck
    clinical_event["ctv3_code"] = None
    clinical_event["numeric_value"] = None
    return clinical_event


vampire_victims = random.choices(patients, k=N_PATIENTS // 10)
clinical_events.extend([vampire_bite(victim) for victim in vampire_victims])

# everyone gets bitten in Whitby
for victim in vampire_victims:
    i = victim["patient_id"] - 1
    practice_reg = practice_registrations[i]
    practice_reg["practice_nuts1_region_name"] = "Yorkshire and The Humber"
    practice_registrations[i] = practice_reg


# Jon gets bitten by ferrets
ferret = 242612006
# pick a random patient
while True:
    patient = random.choice(patients)
    if patient["patient_id"] in [v["patient_id"] for v in vampire_victims]:
        continue
    i = patient["patient_id"] - 1
    patient["date_of_birth"] = "1986-06-02"
    patient["sex"] = "male"
    patient["date_of_death"] = None
    patients[i] = patient

    practice_registration = practice_registrations[i]
    practice_registration["start_date"] = patient["date_of_birth"]
    practice_registration["end_date"] = patient["date_of_death"]
    practice_registration["practice_nuts1_region_name"] = "South West"

    for i in range(0, 100):
        clinical_events.append(clinical_event(patient, ferret))
    break


# some other bites
other_bitten = random.choices(patients, k=N_PATIENTS // 10)
with open("codelists/user-jon_massey-bites.csv", "r") as f:
    reader = csv.DictReader(f)
    bites = list(reader)
    bites = [b["code"] for b in bites]
for patient in other_bitten:
    clinical_events.append(clinical_event(patient, random.choice(bites)))


# cake and parachuting
medications = []

with open("codelists/user-jon_massey-cake-dmd.csv", "r") as f:
    reader = csv.DictReader(f)
    cakes = [c["code"] for c in list(reader)]
with open("codelists/user-jon_massey-extreme-sports.csv") as f:
    reader = csv.DictReader(f)
    sports = [c["code"] for c in list(reader)]
with open("codelists/user-jon_massey-parachuting.csv") as f:
    reader = csv.DictReader(f)
    parachuting = [c["code"] for c in list(reader)]

cake_eaters = random.choices(patients, k=N_PATIENTS // 3)
for patient in cake_eaters:
    medication = {"patient_id": patient["patient_id"]}
    medication["date"] = clinical_event_date(patient)
    medication["dmd_code"] = random.choice(cakes)
    medications.append(medication)

parachutists = random.choices(cake_eaters, k=len(cake_eaters) // 2)
for patient in parachutists:
    date = [m for m in medications if m["patient_id"] == patient["patient_id"]][0][
        "date"
    ]
    date = datetime.strptime(date, "%Y-%m-%d")
    date = date + timedelta(days=random.randint(1, 7))
    date = date.strftime("%Y-%m-%d")
    i = patient["patient_id"] - 1
    if random.randint(0, 1) == 0:
        patient["date_of_death"] = date
    patients[i] = patient
    ce = clinical_event(patient, random.choice(parachuting))
    ce["date"] = date
    clinical_events.append(ce)

other_sports = list(set(sports) - set(parachuting))
sporty_folk = random.choices(patients, k=N_PATIENTS // 3)
parachutist_ids = [p["patient_id"] for p in parachutists]
for patient in sporty_folk:
    if patient["patient_id"] in parachutist_ids:
        continue
    clinical_events.append(clinical_event(patient, random.choice(other_sports)))


with open("example-data/patients.csv", "w") as f:
    writer = csv.DictWriter(
        f, fieldnames=["patient_id", "date_of_birth", "sex", "date_of_death"]
    )
    writer.writeheader()
    writer.writerows(patients)

with open("example-data/clinical_events.csv", "w") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "patient_id",
            "date",
            "snomedct_code",
            "ctv3_code",
            "numeric_value",
        ],
    )
    writer.writeheader()
    random.shuffle(clinical_events)
    writer.writerows(clinical_events)

with open("example-data/practice_registrations.csv", "w") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "patient_id",
            "start_date",
            "end_date",
            "practice_pseudo_id",
            "practice_stp",
            "practice_nuts1_region_name",
        ],
    )
    writer.writeheader()
    writer.writerows(practice_registrations)


with open("example-data/medications.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["patient_id", "date", "dmd_code"])
    writer.writeheader()
    writer.writerows(medications)
