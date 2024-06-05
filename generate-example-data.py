import csv
import random

N_PATIENTS = 3000
patients = []
for patient_id in range(1, N_PATIENTS + 1):
    patient = {"patient_id": patient_id}
    patient["sex"] = random.choice(["male", "female", None])
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
    patients.append(patient)

with open("example-data/patients.csv", "w") as f:
    writer = csv.DictWriter(
        f, fieldnames=["patient_id", "date_of_birth", "sex", "date_of_death"]
    )
    writer.writeheader()
    writer.writerows(patients)
