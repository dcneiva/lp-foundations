"""Pytest configuration file"""
import pandas as pd
import pytest
from pathlib import Path
from life_expectancy.cleaning import clean_data

# Path to the raw input data
RAW_DATA_PATH = Path('life_expectancy/data/eu_life_expectancy_raw.tsv')
# Path to the fixture sample data
FIXTURE_SAMPLE_PATH = Path('life_expectancy/tests/fixtures/eu_life_expectancy_raw.tsv')
# Path to the expected output fixture data
EXPECTED_OUTPUT_PATH = Path('life_expectancy/tests/fixtures/eu_life_expectancy_expected_raw.csv')


def create_sample_data() -> pd.DataFrame:

    #Criar a pasta Fixtures caso ela nao exista
    FIXTURE_SAMPLE_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Load the raw data
    data = pd.read_csv(RAW_DATA_PATH, sep='\t')

    # Create a sample of the raw data for testing
    sample_data = data.sample(n=10, random_state=42)  # adjust the sample size as needed
   
    # Save the sample data to the directory
    sample_data.to_csv(FIXTURE_SAMPLE_PATH, sep='\t', index=False)
    
    read_sample_data = pd.read_csv(FIXTURE_SAMPLE_PATH, sep='\t')
    
    clean_sample_data = clean_data(read_sample_data, country='SK')
    print(clean_sample_data)
    clean_sample_data.to_csv(EXPECTED_OUTPUT_PATH, index=False)

create_sample_data()

@pytest.fixture(scope="session")
def read_sample_tsv():
    return pd.read_csv(FIXTURE_SAMPLE_PATH, sep='\t')

@pytest.fixture(scope="session")
def read_sample_csv():
    return pd.read_csv(EXPECTED_OUTPUT_PATH)