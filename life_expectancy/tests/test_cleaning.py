"""Tests for the cleaning module"""
from life_expectancy.tests.conftest import *
from life_expectancy.cleaning import *
from unittest.mock import patch

def test_load_data(read_sample_tsv):
    input_data = load_data(FIXTURE_SAMPLE_PATH)
    assert read_sample_tsv.equals(input_data)


def test_clean_save_data(sample_data, expected_data):
    test_clean_data = clean_data(sample_data)
   
    with patch('life_expectancy.cleaning.save_data') as mock_save_data:
 
        save_data(test_clean_data, EXPECTED_OUTPUT_PATH)
        mock_save_data.assert_called_once_with(test_clean_data, EXPECTED_OUTPUT_PATH)

    assert expected_data.equals(test_clean_data)