import argparse
import pandas as pd
import os
from pathlib import Path

def load_data(input_path: Path) -> pd.DataFrame:
    """
    Reads the TSV file containing raw life expectancy data from the specified input path.

    Args:
        input_path (Path): The path to the input TSV file.

    Returns:
        pd.DataFrame: The loaded data as a DataFrame.
    """

    df = pd.read_csv(input_path, sep='\t')

    return df


def clean_data(df: pd.DataFrame, country:str = 'PT') -> pd.DataFrame:
    """
    Cleans the life expectancy data DataFrame and filters it by the specified country.

    Args:
        df (pd.DataFrame): The raw life expectancy data.
        country (str): The country code to filter the data (default is 'PT').

    Returns:
        pd.DataFrame: The cleaned and filtered data.
    """
    
    df_long = pd.melt(df, id_vars=['unit,sex,age,geo\\time'], var_name='year', value_name='value')
    df_long[['unit', 'sex', 'age', 'geo\\time']] = df_long['unit,sex,age,geo\\time'].str.split(',', expand=True) # pylint: disable=line-too-long
    df_long.drop(columns=['unit,sex,age,geo\\time'], inplace=True)
    df_long.rename(columns={'geo\\time': 'region'}, inplace=True)
    df_long = df_long[['unit', 'sex', 'age', 'region', 'year', 'value']]

    df_long['year'] = pd.to_numeric(df_long['year'], errors='coerce', downcast='integer')
    df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')
    df_long.dropna(subset=['value'], inplace=True)

    df_long_filtered = df_long[df_long['region'] == country]

    return df_long_filtered

def save_data(df_long_filtered: pd.DataFrame, output_file_path: Path) -> None :
    """
    Saves the cleaned and filtered DataFrame to the specified file path in CSV format.

    Args:
        df_long_filtered (pd.DataFrame): The cleaned and filtered data.
        output_file_path (Path): The path to save the output CSV file.
    """
    
    df_long_filtered.to_csv(output_file_path, index=False)


def main(file_path: Path, output_file_path: Path, country:str = 'PT') -> None:
    """
    Main function to load, clean, and save life expectancy data.

    Args:
        file_path (Path): The path to the input TSV file.
        output_file_path (Path): The path to save the output CSV file.
        country (str): The country code to filter data (default is 'PT').
    """

    df = load_data(file_path)
    df_cleaned = clean_data(df, args.country)
    save_data(df_cleaned, output_file_path)


if __name__ == "__main__": # pragma: no cover
    parser = argparse.ArgumentParser(description='Clean life expectancy data.')
    parser.add_argument('--country', type=str, default='PT', help='Country code to filter data (default: PT)') # pylint: disable=line-too-long
    args = parser.parse_args()

    input_path = os.path.join('life_expectancy', 'data', 'eu_life_expectancy_raw.tsv')
    output_file_path = os.path.join('life_expectancy', 'data', f'{args.country}_life_expectancy_raw.tsv')

    main(input_path, output_file_path, country = 'PT')
