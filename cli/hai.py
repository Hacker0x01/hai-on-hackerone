"""
Hai module

This module contains functions for sending prompts to the Hai API and receiving responses.
The main function, `send_to_hai`, sends prompts to the Hai API for evaluating the validity, complexity, and ownership of a security report.
The module also includes helper functions for sending individual prompts and waiting for the response from the Hai API.

Functions:
- send_to_hai: Sends prompts to the Hai API and returns the predicted validity, complexity, ownership, and other information of a security report.
- send_individual_prompt: Sends an individual prompt to the Hai API and returns the response.
- wait_for_hai: Waits for the response from the Hai API and returns the response data.

"""

import asyncio
import time
import aiohttp
from utils import parse_json_with_control_chars
from config import load_settings
from termcolor import colored

settings = load_settings()

async def send_to_hai(report, verbose):
    """
    Sends prompts to the Hai API and returns the predicted validity, complexity, ownership, and other information of a security report.
    
    Args:
        report (str): The ID of the security report.
        verbose (bool): Whether to print verbose output.

    Returns:
        tuple: A tuple containing the following information:
            - predictedValidity (str): The predicted validity of the security report.
            - predictedValidityCertaintyScore (float): The certainty score of the predicted validity.
            - predictedValidityReasoning (str): The reasoning for the predicted validity.
            - predictedComplexity (str): The predicted complexity of the security report.
            - predictedComplexityCertaintyScore (float): The certainty score of the predicted complexity.
            - predictedComplexityReasoning (str): The reasoning for the predicted complexity.
            - predictedOwnershipCertaintyScore (float): The certainty score of the predicted ownership.
            - predictedOwnershipReasoning (str): The reasoning for the predicted ownership.
            - productArea (str): The product area mapped to the security report.
            - squadOwner (str): The squad owner responsible for the product area.
    """
    with open(settings.ownership_file_path, encoding='UTF-8') as file:
        csv_data = [line.strip() for line in file.readlines() if line.strip()]

    prompts = [
        {
            "role": "user",
            "content": f"""
            Based on the provided information your task is to evaluate the validity of the security report with ID {report}. When assessing validity evaluate if the report is complete, correct, relevant per policy, and describes a valid security vulnerability for bug bounty programs. Provide in your reasoning a percentage value of how certain you are that the report is valid. Your response should be in, without any exception, JSON format without newlines with the following structure: "predictedValidity": [Valid/Invalid], "validityCertaintyScore": [0-100%], "validityReasoning": [Reasoning for the decision]. Please approach the problem methodically and ensure that your reasoning for the decision is clearly outlined. Even if certain information is lacking, use your judgment to make an educated guess to facilitate a streamlined assessment process. Now, take a deep breath and work on this problem step by step. Good luck!
            """
        },
        {
            "role": "user",
            "content": f"""
            Based on the provided information your task is to evaluate the complexity of the security report with ID {report}. When assessing difficulty, use a percentage scale to evaluate if the level of effort required to reproduce the vulnerability based on the report's content. Consider a report high on difficulty when it demands extensive setup, involves numerous steps, or requires specialized expertise beyond common web application security. This includes reports necessitating multiple accounts with different permissions, configuring and installing applications, or following complex steps for reproducing the vulnerability. Conversely, reports that are straightforward to reproduce, lack detailed information, or feature minimal content are categorized on low difficulty. Provide a percentage value of how certain you are that the report is difficult, where 0 is not difficult at all and 100 is extremely difficult. Your response should be in, without any exception, JSON format without newlines with the following structure: "predictedComplexity": [Low/Medium/High], "complexityCertaintyScore": [0-100%], "complexityReasoning": [Reasoning for the decision]. Please approach the problem methodically and ensure that your reasoning for the decision is clearly outlined. Even if certain information is lacking, use your judgment to make an educated guess to facilitate a streamlined assessment process. Now, take a deep breath and work on this problem step by step. Good luck!
            """
        },
        {
            "role": "user",
            "content": f"""
            Based on the provided information your task is to evaluate the ownership of the security report with ID {report}. Use the CSV data to match the report to its product area and squad owner. The CSV data contains two columns: 'Product Area' and 'Squad Owner'. The 'Product Area' column contains the product area to which the report belongs, and the 'Squad Owner' column contains the squad owner responsible for the product area. Use this information to determine the correct product area and squad owner for the report. Your response should be in, without any exception, JSON format without newlines with the following structure: "productArea": [Product Area], "squadOwner": [Squad Owner], "ownershipCertaintyScore": [0-100%], "ownershipReasoning": [Reasoning for the decision]. Provide in your reasoning a percentage value of how certain you are that the report is correctly mapped to the right product area and squad owner. Please approach the problem methodically and ensure that your reasoning for the decision is clearly outlined. Even if certain information is lacking, use your judgment to make an educated guess to facilitate a streamlined assessment process. Now, take a deep breath and work on this problem step by step. Good luck! The CSV data is: {csv_data}
            """
        }
    ]

    if verbose:
        start_time = time.time()

    tasks = [send_individual_prompt(prompt, report, verbose) for prompt in prompts]
    responses = await asyncio.gather(*tasks)

    if verbose:
        end_time = time.time()
        execution_time = end_time - start_time
        print(colored(f"Execution Time: {execution_time} seconds", 'cyan'))
        print(colored("Responses from Hai:", 'blue'))
        print(responses)

    if responses[0] is None or 'response' not in responses[0]:
        print(colored("Error: Validity response is None or invalid.", 'light_red'))
        return None

    if responses[1] is None or 'response' not in responses[1]:
        print(colored("Error: Complexity response is None or invalid.", 'light_red'))
        return None

    if responses[2] is None or 'response' not in responses[2]:
        print(colored("Error: Ownership response is None or invalid.", 'light_red'))
        return None

    try:
        pV = parse_json_with_control_chars(responses[0]['response'])
        pC = parse_json_with_control_chars(responses[1]['response'])
        pO = parse_json_with_control_chars(responses[2]['response'])
    except Exception as e:
        print(colored(f"Error parsing JSON response: {e}", 'light_red'))
        return None

    predictedValidity = pV.get('predictedValidity', 'Unknown')
    predictedValidityCertaintyScore = pV.get('validityCertaintyScore', 0)
    predictedValidityReasoning = pV.get('validityReasoning', 'No reasoning provided')
    predictedComplexity = pC.get('predictedComplexity', 'Unknown')
    predictedComplexityCertaintyScore = pC.get('complexityCertaintyScore', 0)
    predictedComplexityReasoning = pC.get('complexityReasoning', 'No reasoning provided')
    predictedOwnershipCertaintyScore = pO.get('ownershipCertaintyScore', 0)
    predictedOwnershipReasoning = pO.get('ownershipReasoning', 'No reasoning provided')
    productArea = pO.get('productArea', 'Unknown')
    squadOwner = pO.get('squadOwner', 'Unknown')

    return (predictedValidity, predictedValidityCertaintyScore, predictedValidityReasoning,
            predictedComplexity, predictedComplexityCertaintyScore, predictedComplexityReasoning,
            predictedOwnershipCertaintyScore, predictedOwnershipReasoning, productArea, squadOwner)

async def send_individual_prompt(prompt, report, verbose):
    """
    Sends an individual prompt to the Hai API and returns the response.

    Args:
        prompt (dict): The prompt to send to the Hai API.
        report (str): The ID of the security report.
        verbose (bool): Whether to print verbose output.

    Returns:
        dict: The response from the Hai API.

    """
    async with aiohttp.ClientSession() as session:
        data = {
            "data": {
                "type": "completion-request",
                "attributes": {
                    "messages": [prompt],
                    "report_ids": [report]     
                }
            },
        }

        if verbose:
            print(colored("Request sent to Hai:", 'blue'))
            print(data)

        try:
            async with session.post('https://api.hackerone.com/v1/hai/chat/completions', auth=aiohttp.BasicAuth(settings.api_name, settings.api_key), json=data, headers=settings.headers) as r:
                try:
                    response_data = await r.json()
                except aiohttp.ContentTypeError:
                    # Print the raw response text if not JSON
                    raw_response = await r.text()
                    print(colored(f"Error: Received non-JSON response from API: {raw_response}", 'light_red'))
                    return None

                if verbose:
                    print(colored("Response from Hai:", 'blue'))
                    print(response_data)
                return await wait_for_hai(response_data, verbose)
        except Exception as err:
            print(colored(f"Unexpected error: {err}, {type(err)}", 'light_red'))
            raise err

async def wait_for_hai(response_data, verbose=False):
    """
    Waits for the response from the Hai API and returns the response data.

    Args:
        response_data (dict): The response data from the Hai API.
        verbose (bool): Whether to print verbose output.

    Returns:
        dict: The response data from the Hai API.

    """
    if verbose:
        print(colored("Initial response from Hai:", 'blue'))
        print(response_data)

    if not response_data or 'data' not in response_data or 'attributes' not in response_data['data']:
        print(colored("Error: Invalid response format from API.", 'light_red'))
        return None

    if response_data['data']['attributes']['state'] == 'completed':
        print(colored("Response received and the request has been successfully completed!", 'light_green'))
        return response_data['data']['attributes']
    else:
        print(colored("Waiting for response completion...", 'light_grey'))
        await asyncio.sleep(2)
        url = f"https://api.hackerone.com/v1/hai/chat/completions/{response_data['data']['id']}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, auth=aiohttp.BasicAuth(settings.api_name, settings.api_key)) as r:
                new_response_data = await r.json()
                return await wait_for_hai(new_response_data, verbose)
