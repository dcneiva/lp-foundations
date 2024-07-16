import argparse
import pandas as pd
import os

def clean_data(country='PT'):
    """
    This function read and clean the file eu_life_expectancy_raw.tsv
    and at the end save the new clean file as pt_life_expectancy.csv
    """

    file_path = os.path.join('life_expectancy', 'data', 'eu_life_expectancy_raw.tsv')

    df = pd.read_csv(file_path, sep='\t')

    # Unpivot DataFrame to long format
    df_long = pd.melt(df, id_vars=['unit,sex,age,geo\\time'], var_name='year', value_name='value')
    df_long[['unit', 'sex', 'age', 'geo\\time']] = df_long['unit,sex,age,geo\\time'].str.split(',', expand=True) # pylint: disable=line-too-long
    df_long.drop(columns=['unit,sex,age,geo\\time'], inplace=True)
    df_long.rename(columns={'geo\\time': 'region'}, inplace=True)
    df_long = df_long[['unit', 'sex', 'age', 'region', 'year', 'value']]

    df_long['year'] = pd.to_numeric(df_long['year'], errors='coerce', downcast='integer')

    df_long['value'] = pd.to_numeric(df_long['value'], errors='coerce')
    df_long.dropna(subset=['value'], inplace=True)

    df_long_filtered = df_long[df_long['region'] == country]

    output_file_path = os.path.join('life_expectancy', 'data', f'{country}_life_expectancy_raw.tsv')
    df_long_filtered.to_csv(output_file_path, index=False)

if __name__ == "__main__": # pragma: no cover--> QUE É ISTO? XD
    parser = argparse.ArgumentParser(description='Clean life expectancy data.')
    parser.add_argument('--country', type=str, default='PT', help='Country code to filter data (default: PT)') # pylint: disable=line-too-long
    args = parser.parse_args()

    clean_data(args.country)
