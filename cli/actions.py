"""
Run actions based on the predictions

This module contains functions to perform various actions based on the predictions made by the HAI (Human Augmentation Intelligence) system. The actions include posting private comments, updating custom fields, and writing to a CSV file.

Functions:
- hai_actions: Runs the actions based on the predictions.
- post_private_comment: Posts a private comment on a report with the predicted validity, complexity, ownership, and reasoning.
- update_custom_field: Updates the custom fields of a report with the predicted validity, complexity, product area, and squad owner.
- write_to_csv: Writes the report ID, predicted validity, complexity, product area, and squad owner to a CSV file.
"""

import csv

import requests
from config import load_settings
from utils import bcolors

settings = load_settings()

def hai_actions(predictedValidity, predictedValidityCertaintyScore, predictedValidityReasoning, predictedComplexity, predictedComplexityCertaintyScore, predictedComplexityReasoning, predictedOwnershipCertaintyScore, predictedOwnershipReasoning, productArea, squadOwner, report_id, comment_hai_flag, custom_field_hai_flag, csv_output_flag, verbose):
    """
    Run actions based on the predictions.

    This function runs the actions based on the predictions made by the HAI system. The actions include posting a private comment, updating custom fields, and writing to a CSV file.

    Args:
    - predictedValidity: The predicted validity of the report.
    - predictedValidityCertaintyScore: The certainty score of the predicted validity.
    - predictedValidityReasoning: The reasoning behind the predicted validity.
    - predictedComplexity: The predicted complexity of the report.
    - predictedComplexityCertaintyScore: The certainty score of the predicted complexity.
    - predictedComplexityReasoning: The reasoning behind the predicted complexity.
    - predictedOwnershipCertaintyScore: The certainty score of the predicted ownership.
    - predictedOwnershipReasoning: The reasoning behind the predicted ownership.
    - productArea: The product area of the report.
    - squadOwner: The squad owner of the report.
    - report_id: The ID of the report.
    - comment_hai_flag: A flag indicating whether to post a private comment.
    - custom_field_hai_flag: A flag indicating whether to update custom fields.
    - csv_output_flag: A flag indicating whether to write to a CSV file.
    - verbose: A flag indicating whether to print verbose output.

    Returns:
    - None
    """
    if comment_hai_flag:
        print(f"{bcolors.OKBLUE}Posting Private Comment...{bcolors.ENDC}")
        post_private_comment(report_id, predictedValidity, predictedValidityCertaintyScore, predictedValidityReasoning, predictedComplexity, predictedComplexityCertaintyScore, predictedComplexityReasoning, predictedOwnershipCertaintyScore, predictedOwnershipReasoning, productArea, squadOwner, verbose)
        print(f"{bcolors.OKGREEN}Private Comment is successfully posted{bcolors.ENDC}")
    if custom_field_hai_flag:
        print(f"{bcolors.OKBLUE}Updating Custom Fields...{bcolors.ENDC}")
        update_custom_field(report_id, predictedValidity, predictedComplexity, productArea, squadOwner, verbose)
        print(f"{bcolors.OKGREEN}Custom Fields have been successfully updated{bcolors.ENDC}")
    if csv_output_flag:
        write_to_csv(report_id, predictedValidity, predictedComplexity, productArea, squadOwner)

def post_private_comment(report, predictedValidity, predictedValidityCertaintyScore, predictedValidityReasoning, predictedComplexity, predictedComplexityCertaintyScore, predictedComplexityReasoning, predictedOwnershipCertaintyScore, predictedOwnershipReasoning, productArea, squadOwner, verbose):
    """
    Post a private comment on a report with the predicted validity, complexity, ownership, and reasoning.

    This function posts a private comment on a report with the predicted validity, complexity, ownership, and reasoning provided by the HAI system.

    Args:
    - report: The ID of the report.
    - predictedValidity: The predicted validity of the report.
    - predictedValidityCertaintyScore: The certainty score of the predicted validity.
    - predictedValidityReasoning: The reasoning behind the predicted validity.
    - predictedComplexity: The predicted complexity of the report.
    - predictedComplexityCertaintyScore: The certainty score of the predicted complexity.
    - predictedComplexityReasoning: The reasoning behind the predicted complexity.
    - predictedOwnershipCertaintyScore: The certainty score of the predicted ownership.
    - predictedOwnershipReasoning: The reasoning behind the predicted ownership.
    - productArea: The product area of the report.
    - squadOwner: The squad owner of the report.
    - verbose: A flag indicating whether to print verbose output.

    Returns:
    - None
    """
    data = {
        "data": {
            "type": "activity-comment",
            "attributes": {
                "message": f"""
                # Hai has completed the triage process for this report. 
                
                ## Validity 
                The predicted validity is {predictedValidity} and Hai is {predictedValidityCertaintyScore}% sure about this. The reasoning behind it is as follows: {predictedValidityReasoning}.
                
                ## Complextity
                The predicted complexity is {predictedComplexity} and Hai is {predictedComplexityCertaintyScore}% sure about this. The reasoning behind it is as follows: {predictedComplexityReasoning}.
                
                ## Ownership 
                The product area is {productArea} and the squad owner is {squadOwner}. Hai is {predictedOwnershipCertaintyScore}% sure about the ownership. The reasoning behind it is as follows: {predictedOwnershipReasoning}""",
                "internal": True,
                "attachment_ids": []
            }
        }
    }

    if verbose:
        print(f"{bcolors.OKBLUE}Data that is sent to Hai{bcolors.ENDC}")
        print(data)

    try:
        r = requests.post(
            'https://api.hackerone.com/v1/reports/' + str(report) + '/activities',
            auth=(settings.api_name, settings.api_key),
            json=data,
            headers=settings.headers,
            timeout=(5, 10)
        )
        r.raise_for_status()
        if verbose:
            print(f"{bcolors.OKBLUE}Response from Hai{bcolors.ENDC}")
            print(r.json())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise

def update_custom_field(report, predictedValidity, predictedComplexity, productArea, squadOwner, verbose):
    """
    Update custom fields for a given report.

    Args:
        report (int): The ID of the report to update.
        predictedValidity (str): The predicted validity value.
        predictedComplexity (str): The predicted complexity value.
        productArea (str): The product area value.
        squadOwner (str): The squad owner value.
        verbose (bool): Whether to print additional information.

    Returns:
        None
    """
    field_updates = {
        settings.cf_1: predictedValidity,
        settings.cf_2: predictedComplexity,
        settings.cf_3: productArea,
        settings.cf_4: squadOwner
    }

    for field_id, field_value in field_updates.items():
        data = {
            "data": {
                "attributes": {
                    "custom_field_attribute_id": field_id,
                    "value": field_value
                }
            }
        }

        if verbose:
            print(f"{bcolors.OKBLUE}Data that is sent to Hai{bcolors.ENDC}")
            print(data)

        try:
            r = requests.post(
                'https://api.hackerone.com/v1/reports/' + str(report) + '/custom_field_values',
                auth=(settings.api_name, settings.api_key),
                json=data,
                headers=settings.headers,
                timeout=(5, 10)
            )
            r.raise_for_status()
            if verbose:
                print(f"{bcolors.OKBLUE}Response from Hai{bcolors.ENDC}")
                print(r.json())
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            raise

def write_to_csv(report_id, predictedValidity, predictedComplexity, productArea, squadOwner):
    """
    Writes the provided data to a CSV file.

    Args:
        report_id (str): The report ID.
        predictedValidity (str): The predicted validity.
        predictedComplexity (str): The predicted complexity.
        productArea (str): The product area.
        squadOwner (str): The squad owner.

    Returns:
        str: A message indicating that the CSV output file has been successfully updated.
    """
    print(f"{bcolors.OKBLUE}Beginning the process of writing to the CSV file...{bcolors.ENDC}")
    with open(settings.csv_output_file_path, "a+", encoding='UTF-8') as file:
        csv_writer = csv.writer(file)
        if file.tell() == 0:
            csv_writer.writerow(["Report ID", "Predicted Validity", "Predicted Difficulty", "Product Area", "Squad Owner"])
        csv_writer.writerow([report_id, predictedValidity, predictedComplexity, productArea, squadOwner])
    print(f"{bcolors.OKGREEN}The CSV output file has been successfully updated{bcolors.ENDC}")
    return "Done"
