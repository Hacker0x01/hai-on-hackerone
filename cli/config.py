"""
Config module
"""
import os
from dotenv import load_dotenv

load_dotenv()

def load_api_variables():
    """
    Load API variables from environment variables.

    Returns:
      api_name (str): The name of the API.
      api_key (str): The API key.
      program_handle (str): The handle of the program.
      headers (dict): The headers for API requests.
    """
    api_name = os.getenv("API_NAME")
    api_key = os.getenv("API_KEY")
    program_handle = os.getenv("PROGRAM_HANDLE")

    headers = {'Accept': 'application/json'}
    return api_name, api_key, program_handle, headers

def load_actions_variables():
    """
    Load action variables from environment variables.

    Returns:
      cf_1 (str): The custom field ID for validity.
      cf_2 (str): The custom field ID for complexity.
      cf_3 (str): The custom field ID for product area.
      cf_4 (str): The custom field ID for squad owner.
    """
    cf_1 = os.getenv("CUSTOM_FIELD_ID_VALIDITY")
    cf_2 = os.getenv("CUSTOM_FIELD_ID_COMPLEXITY")
    cf_3 = os.getenv("CUSTOM_FIELD_ID_PRODUCT_AREA")
    cf_4 = os.getenv("CUSTOM_FIELD_ID_SQUAD_OWNER")
    return cf_1, cf_2, cf_3, cf_4

def load_ownership_file():
    """
    Load ownership file from environment variable.

    Returns:
      ownership (str): The path to the ownership file.
    """
    return os.getenv("OWNERSHIP_FILE", "./cli/config/ownership.csv.sample")

def load_csv_output_file():
    """
    Load CSV output file from environment variable.

    Returns:
      csv_output_file (str): The path to the CSV output file.
    """
    return os.getenv("CSV_OUTPUT_FILE", "./cli/data/hai-on-hackerone-output.csv")
