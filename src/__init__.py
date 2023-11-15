import pandas as pd 

# helpers function
def read_csv_file(file_name, column_index='organization_website'):
    """Read the CSV file and extract a specific column."""
    df = pd.read_csv(file_name)
    # Extract the specified column
    urls = df[column_index].drop_duplicates().to_list()
    return urls