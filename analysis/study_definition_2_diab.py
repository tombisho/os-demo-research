## LIBRARIES

# cohort extractor
from cohortextractor import (
    StudyDefinition,
    Measure,
    patients,
    codelist_from_csv,
    codelist,
    filter_codes_by_category,
    combine_codelists
)

## CODELISTS
# All codelist are held within the codelist/ folder.

codes_diab = codelist_from_csv(
    "codelists/opensafely-type-2-diabetes.csv", system="ctv3", column="CTV3ID"
)

## STUDY POPULATION
# Defines both the study population and points to the important covariates

index_date = "2020-01-01"
end_date = "2020-09-30"


study = StudyDefinition(
        # Configure the expectations framework
    default_expectations={
        "date": {"earliest": index_date, "latest": end_date},
        "rate": "uniform",
    },

    index_date = index_date,

    # This line defines the study population
    population = patients.satisfying(
        """
        (sex = 'F' OR sex = 'M') AND
        (age >= 18 AND age < 120) AND
        (NOT died) AND
        (registered)
        """,
        
        registered = patients.registered_as_of(index_date),
        died = patients.died_from_any_cause(
		    on_or_before=index_date,
		    returning="binary_flag",
        ),
    ),

    age = patients.age_as_of(
        index_date,
        return_expectations={
            "int": {"distribution": "population_ages"},
            "incidence": 1
        },
    ),

    sex = patients.sex(
        return_expectations={
            "category": {"ratios": {"M": 0.49, "F": 0.51}},
            "incidence": 1
        }
    ),
    
    bmi = patients.most_recent_bmi(
      between=["2010-02-01", "2020-01-31"],
      minimum_age_at_measurement=18,
      include_measurement_date=True,
      date_format="YYYY-MM",
      return_expectations={
          "date": {"earliest": "2010-02-01", "latest": "2020-01-31"},
          "float": {"distribution": "normal", "mean": 28, "stddev": 8},
          "incidence": 0.80,
      }
    ),
    
    has_diab = patients.with_these_clinical_events(
    codes_diab,
    returning = "binary_flag",
    between = ["index_date", "index_date + 1 month"],
    return_expectations={
        "incidence": 0.1,
        },
    ),
 
)
