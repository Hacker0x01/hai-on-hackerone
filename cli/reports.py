# pylint: disable=W0612
"""
Reports Module

This module contains functions for retrieving and processing reports from the HackerOne API.
"""
import requests
from actions import hai_actions
from hai import send_to_hai
from config import load_settings
from termcolor import colored

settings = load_settings()

async def get_all_reports(
        severity,
        state,
        reference,
        comment_hai_flag,
        custom_field_hai_flag,
        csv_output_flag,
        verbose):
    """
    Retrieves all reports from the HackerOne API based on the specified filters.

    Args:
        severity (str): The severity level of the reports to retrieve.
        state (str): The state of the reports to retrieve.
        reference (bool): Flag indicating whether to filter reports based on the presence of an issue tracker reference.
        comment_hai_flag (bool): Flag indicating whether to comment on the reports using HAI.
        custom_field_hai_flag (bool): Flag indicating whether to update custom fields on the reports using HAI.
        csv_output_flag (bool): Flag indicating whether to output the reports in CSV format.
        verbose (bool): Flag indicating whether to display verbose output.
    
    Returns:
        None
    """
    url = "https://api.hackerone.com/v1/reports"
    pageNum = 1

    while url:
        params = {
            'filter[program][]': [settings.program_handle],
            'filter[severity][]': [severity],
            'filter[state][]': [state],
            'page[number]': pageNum
        }
        if reference:
            params['filter[issue_tracker_reference_id__null]'] = [reference]

        try:
            r = requests.get(
                url,
                auth=(settings.api_name, settings.api_key),
                params=params,
                headers=settings.headers,
                timeout=(5, 10)
            )
            r.raise_for_status()
            response = r.json()
            print("Results Page: "+ str(pageNum))
        except requests.exceptions.RequestException as e:
            print(colored(f"An error occurred: {e}"),'light_red')
            raise
        await show_reports(response, verbose, comment_hai_flag, custom_field_hai_flag, csv_output_flag)

        if "next" in response["links"]:
            print(response["links"])
            pageNum += 1
        else:
            print(colored("No further pages", 'cyan'))
            url = None

async def get_reports(report_ids, severity, state, comment_hai_flag, custom_field_hai_flag, csv_output_flag, verbose):
    """
    Retrieves specific reports from the HackerOne API based on the provided report IDs.

    Args:
        report_ids (list): A list of report IDs to retrieve.
        severity (str): The severity level of the reports to retrieve.
        state (str): The state of the reports to retrieve.
        comment_hai_flag (bool): Flag indicating whether to comment on the reports using HAI.
        custom_field_hai_flag (bool): Flag indicating whether to update custom fields on the reports using HAI.
        csv_output_flag (bool): Flag indicating whether to output the reports in CSV format.
        verbose (bool): Flag indicating whether to display verbose output.

    Returns:
        None
    """
    url = "https://api.hackerone.com/v1/reports/"
    # WIP Multiple report numbers are not saved in reportList
    reportList = []
    for report in report_ids:
        urlreport = url + str(report)

        try:
            r = requests.get(
                urlreport,
                auth=(settings.api_name, settings.api_key),
                params={
                    'filter[severity][]': [severity],
                    'filter[state][]': [state]
                },
                headers=settings.headers,
                timeout=(5, 10)
            )
            r.raise_for_status()
            response = r.json()
            show_single_report(response)
            predictedValidity, predictedValidityCertaintyScore, predictedValidityReasoning, predictedComplexity, predictedComplexityCertaintyScore, predictedComplexityReasoning, predictedOwnershipCertaintyScore, predictedOwnershipReasoning, productArea, squadOwner = await send_to_hai(report, verbose)
            hai_actions(predictedValidity, predictedValidityCertaintyScore, predictedValidityReasoning, predictedComplexity, predictedComplexityCertaintyScore, predictedComplexityReasoning, predictedOwnershipCertaintyScore, predictedOwnershipReasoning, productArea, squadOwner, report, comment_hai_flag, custom_field_hai_flag, csv_output_flag, verbose)
            print("_____________")
        except requests.exceptions.RequestException as e:
            print(colored(f"An error occurred: {e}"),'light_red')
            raise
    if len(report_ids) == 1:
        print(colored("1 report has been successfully processed", 'cyan'))
    else:
        print(colored(f"{len(report_ids)} reports have been successfully processed", 'cyan'))

async def show_reports(response, verbose, comment_hai_flag, custom_field_hai_flag, csv_output_flag):
    """
    Iterates through the reports in the API response and processes each report.

    Args:
        response (dict): The API response containing the reports.
        verbose (bool): Flag indicating whether to display verbose output.
        comment_hai_flag (bool): Flag indicating whether to comment on the reports using HAI.
        custom_field_hai_flag (bool): Flag indicating whether to update custom fields on the reports using HAI.
        csv_output_flag (bool): Flag indicating whether to output the reports in CSV format.

    Returns:
        None
    """
    print(response)
    report_ids = []
    for report in response["data"]:
        show_single_report(report)
        report_ids.append(report["id"])
    print("All done!")
    counter = 0
    for report in report_ids:
        counter += 1
        # print(colored(f"{banner}", 'light_magenta'))
        print(colored(f"Processing report {counter} of {len(report_ids)}", 'cyan'))
        print(colored(f"Sending report {report} to Hai...", 'cyan'))
        predictedValidity, predictedValidityCertaintyScore, predictedValidityReasoning, predictedComplexity, predictedComplexityCertaintyScore, predictedComplexityReasoning, predictedOwnershipCertaintyScore, predictedOwnershipReasoning, productArea, squadOwner = await send_to_hai(report, verbose)
        hai_actions(predictedValidity, predictedValidityCertaintyScore, predictedValidityReasoning, predictedComplexity, predictedComplexityCertaintyScore, predictedComplexityReasoning, predictedOwnershipCertaintyScore, predictedOwnershipReasoning, productArea, squadOwner, report, comment_hai_flag, custom_field_hai_flag, csv_output_flag, verbose)
    print(colored(f"{len(report_ids)} reports have been successfully processed", 'cyan'))

def show_single_report(report):
    """
    Prints details of a single report.

    Args:
        report (dict): The report data.

    Returns:
        None
    """
    try:
        report_data = report.get("data", report)
        print("_____________")
        print("Report ID: " + report_data["id"])
        print("Report Title: " + report_data["attributes"]["title"])
        print("Report State: " + report_data["attributes"]["state"])
        reporter_stats = report_data.get("relationships", {}).get("reporter", {}).get("data", {}).get("attributes", {})
        if "reputation" in reporter_stats:
            print("Reporter Reputation: " + str(reporter_stats["reputation"]))
        else:
            print("Reporter Reputation: N/A")
        if "signal" in reporter_stats:
            print("Reporter Signal: " + str(reporter_stats["signal"]))
        else:
            print("Reporter Signal: N/A")
    except Exception as err:
        print(colored(f"Unexpected {err=}, {type(err)=}", 'light_red'))
        raise err
