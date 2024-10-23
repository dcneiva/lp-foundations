""" TBD """
import argparse
from pathlib import Path
import pandas as pd
from life_expectancy.strategy import _get_data_strategy

def load_data(input_filepath: Path) -> pd.DataFrame:
    """
    Reads the TSV file containing raw life expectancy data from the specified input path.

    Args:
        input_filepath (Path): The path to the input TSV file.

    Returns:
        pd.DataFrame: The loaded data as a DataFrame.
    """
    strategy = _get_data_strategy(input_filepath)
    return strategy.load_data(input_filepath)


def clean_data(data_frame: pd.DataFrame, country: str = 'PT') -> pd.DataFrame:
    """
    REESCREVER NO FUTURO!!
    Cleans the life expectancy data DataFrame and filters it by the specified country.

    Args:
        data_frame (pd.DataFrame): The raw life expectancy data.
        country (str): The country code to filter the data (default is 'PT').

    Returns:
        pd.DataFrame: The cleaned and filtered data.
    """
    df_long = pd.melt(data_frame, id_vars=['unit,sex,age,geo\\time'],
                      var_name='year', value_name='value')

    split_columns = df_long['unit,sex,age,geo\\time'].str.split(',', expand=True)
    df_long[['unit', 'sex', 'age', 'geo\\time']] = split_columns

    df_long.drop(columns=['unit,sex,age,geo\\time'], inplace=True)
    df_long.rename(columns={'geo\\time': 'region'}, inplace=True)
    df_long = df_long[['unit', 'sex', 'age', 'region', 'year', 'value']]

    df_long['year'] = pd.to_numeric(df_long['year'], errors='coerce', downcast='integer')
    df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')
    df_long.dropna(subset=['value'], inplace=True)

    df_long_filtered = df_long[df_long['region'] == country]

    return df_long_filtered


def save_data(filtered_data_frame: pd.DataFrame, output_filepath: Path) -> None:
    """
    Saves the cleaned and filtered DataFrame to the specified file path in CSV format.

    Args:
        filtered_data_frame (pd.DataFrame): The cleaned and filtered data.
        output_filepath (Path): The path to save the output CSV file.
    """
    save_strategy = _get_data_strategy(output_filepath)
    save_strategy.save_data(filtered_data_frame, output_filepath)


def main(file_path: Path, output_file_path: Path, country: str) -> None:
    """
    Main function to load, clean, and save life expectancy data.

    Args:
        file_path (Path): The path to the input TSV file.
        output_file_path (Path): The path to save the output CSV file.
        country (str): The country code to filter data.
    """
    data_frame = load_data(file_path)
    cleaned_data = clean_data(data_frame, country)
    save_data(cleaned_data, output_file_path)

    return cleaned_data


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description='Clean life expectancy data.')
    parser.add_argument('--country', type=str, default='PT',
                        help='Country code to filter data (default: PT)')
    args = parser.parse_args()

    input_path = Path('life_expectancy', 'data', 'eurostat_life_expect.json')
    output_path = Path('life_expectancy', 'data', f'{args.country}_life_expectancy_raw.json')

    main(input_path, output_path, args.country)
