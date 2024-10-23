from abc import ABC, abstractmethod
import pandas as pd
import os

class DataStrategy(ABC):
    """Abstract base class for data loading and saving strategies.

    This class defines the interface for loading and saving data, 
    allowing for different data formats to be handled by concrete 
    implementations.
    """

    @abstractmethod
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from a specified file path.

        Args:
            file_path (str): The path to the file from which to load data.

        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame.
        """
        pass

    @abstractmethod
    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        """Save the provided DataFrame to a specified output path.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            output_path (str): The path to the file where the data will be saved.
        """
        pass

class CSVDataStrategy(DataStrategy):
    """Concrete strategy for handling CSV data."""

    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from a CSV file.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame.
        """
        return pd.read_csv(file_path)

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        """Save the DataFrame to a CSV file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            output_path (str): The path to the CSV file where the data will be saved.
        """
        df.to_csv(output_path, index=False)

class ExcelDataStrategy(DataStrategy):
    """Concrete strategy for handling Excel data."""

    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from an Excel file.

        Args:
            file_path (str): The path to the Excel file.

        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame.
        """
        return pd.read_excel(file_path)

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        """Save the DataFrame to an Excel file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            output_path (str): The path to the Excel file where the data will be saved.
        """
        df.to_excel(output_path, index=False)

class ParquetDataStrategy(DataStrategy):
    """Concrete strategy for handling Parquet data."""

    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from a Parquet file.

        Args:
            file_path (str): The path to the Parquet file.

        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame.
        """
        return pd.read_parquet(file_path)

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        """Save the DataFrame to a Parquet file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            output_path (str): The path to the Parquet file where the data will be saved.
        """
        df.to_parquet(output_path, index=False)

class PickleDataStrategy(DataStrategy):
    """Concrete strategy for handling Pickle data."""

    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from a Pickle file.

        Args:
            file_path (str): The path to the Pickle file.

        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame.
        """
        return pd.read_pickle(file_path)

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        """Save the DataFrame to a Pickle file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            output_path (str): The path to the Pickle file where the data will be saved.
        """
        df.to_pickle(output_path)

class JSONDataStrategy(DataStrategy):
    """Concrete strategy for handling JSON data."""

    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from a JSON file.

        Args:
            file_path (str): The path to the JSON file.

        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame.
        """
        return pd.read_json(file_path)

    def save_data(self, df: pd.DataFrame, output_path: str) -> None:
        """Save the DataFrame to a JSON file.

        Args:
            df (pd.DataFrame): The DataFrame to save.
            output_path (str): The path to the JSON file where the data will be saved.
        """
        df.to_json(output_path, orient='records', lines=True)



def _get_data_strategy(file_path: str) -> DataStrategy:
    """Select the appropriate data strategy based on the file extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        DataStrategy: The appropriate strategy for handling the file format.
    """
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()

    if file_extension == '.csv':
        return CSVDataStrategy()
    elif file_extension == '.xlsx':
        return ExcelDataStrategy()
    elif file_extension == '.parquet':
        return ParquetDataStrategy()
    elif file_extension == '.pkl' or file_extension == '.pickle':
        return PickleDataStrategy()
    elif file_extension == '.json':
        return JSONDataStrategy()
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")
