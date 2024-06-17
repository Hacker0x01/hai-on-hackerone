# pylint: disable=R0902,R0903
"""
Config module
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Settings class
    """
    def __init__(self):
        """
        Initialize settings

        api_name (str): The name of the API.
        api_key (str): The API key.
        program_handle (str): The handle of the program.
        headers (dict): The headers for API requests.
        cf_1 (str): The custom field ID for validity.
        cf_2 (str): The custom field ID for complexity.
        cf_3 (str): The custom field ID for product area.
        cf_4 (str): The custom field ID for squad owner.
        ownership_file_path (str): The path to the ownership file.
        csv_output_file (str): The path to the CSV output file.
        """
        self.api_name = os.environ["API_NAME"]
        self.api_key = os.environ["API_KEY"]
        self.program_handle = os.environ["PROGRAM_HANDLE"]
        self.headers = {'Accept': 'application/json'}

        self.cf_1 = os.getenv("CUSTOM_FIELD_ID_VALIDITY")
        self.cf_2 = os.getenv("CUSTOM_FIELD_ID_COMPLEXITY")
        self.cf_3 = os.getenv("CUSTOM_FIELD_ID_PRODUCT_AREA")
        self.cf_4 = os.getenv("CUSTOM_FIELD_ID_SQUAD_OWNER")

        script_dir = os.path.dirname(__file__)
        self.ownership_file_path = os.getenv('OWNERSHIP_FILE', f"{script_dir}/config-data/ownership.csv")
        self.csv_output_file_path = os.getenv("CSV_OUTPUT_FILE", f"{script_dir}/data/hai-on-hackerone-output.csv")

def load_settings():
    """
    Load settings from environment variables.

    Returns:
      Settings: An object containing all the settings.
    """
    return Settings()
