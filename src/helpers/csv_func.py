'''helper class for CSV methods'''
from io import BytesIO
import pandas as pd


class CsvHelper:
    """A helper class for reading CSV files."""
    
    def __init__(self, file):
        """
        Constructor method for CsvHelper
        Parameters:
        - file: A file object representing the CSV file to be read.
        """
        self.file = file

    def read_csv_file(self):
        """
        Read the CSV file specified during initialization.
        Returns:
        - df: A Pandas DataFrame containing the data from the CSV file.
        """
        if not self.file:
            return None, "Invalid CSV file or empty csv file"
        # Read the bytes from the file object
        csv_bytes = self.file.file.read()
        # Create a BytesIO buffer from the bytes
        buffer = BytesIO(csv_bytes)
        # Read the CSV data into a Pandas DataFrame
        df = pd.read_csv(buffer)
        # Return the DataFrame
        return df
    
    @staticmethod
    def write_csv_df(data):
        """
        Write to the CSV file.
        Parameters:
        - data: a dict list.
        Returns:
        - df: A Pandas DataFrame containing the data from the CSV file.
        """
        if not data:
            return None, "Data passed is an empty array: require a dict list"
        df = pd.DataFrame(data)
        return df
