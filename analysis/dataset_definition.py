from ehrql import create_dataset
from ehrql.tables.tpp import patients, practice_registrations, clinical_events
from ehrql import codelist_from_csv

dataset = create_dataset()

index_date = "2020-03-31"

has_registration = practice_registrations.for_patient_on(
    index_date
).exists_for_patient()

dataset.define_population(has_registration)

dataset.sex = patients.sex

bites_codelist = codelist_from_csv(
    "local-codelists/bites.csv",
    column="code"
)

dataset.bites = clinical_events.where(clinical_events.snomedct_code.is_in(bites_codelist)).count_for_patient()
dataset.ferret_bites = clinical_events.where(clinical_events.snomedct_code.is_in(['242612006'])).count_for_patient()
