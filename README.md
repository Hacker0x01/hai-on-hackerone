![image info](images/haigh-on-h1onh1.webp)

# Hai on Hackerone

Leveraging Hai trough our API. This repository contains a few tools allowing retrieving and processing reports from the HackerOne API. It can fetch reports matching specified filters, send them to the Hai (HackerOne's Copilot) for triage, and perform actions like posting comments and populating custom fields based on the AI response.

## Table of Contents

- [Hai on Hackerone](#hai-on-hackerone)
  - [Features at a Glance](#features-at-a-glance)
  - [Quick Start](#quick-start)
  - [Docker Usage](#docker-usage)
  - [CLI Usage](#cli-usage)
  - [CLI Example](#cli-examples)
  - [Webhook Endpoint](#webhook-endpoint)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [Troubleshooting](#troubleshooting)

## Features at a Glance

- **Fetching Reports**: The script retrieves reports that match our specified filters, such as program, severity, and state. This allows us to focus on the most critical issues first.

- **AI-Powered Triage**: Reports are sent to HackerOne AI for assessment. The AI evaluates each report and provides insights, helping us determine the validity and urgency of the issues.

- **Automated Actions**: Based on the AI’s response, the script can post private comments on reports, update custom fields, and export responses to a CSV file for further analysis.

## Quick Start

To install this project, you can use Docker Compose. Here are the steps:

1. Clone the repository: `git clone hai-on-hackerone`
2. Create a new file named `.env` in the root directory of the project with the following content (see .env.sample)

```bash
API_NAME=
API_KEY=
PROGRAM_HANDLE=
WEBHOOK_SECRET=
CUSTOM_FIELD_ID_VALIDITY=
CUSTOM_FIELD_ID_COMPLEXITY=
CUSTOM_FIELD_ID_PRODUCT_AREA=
CUSTOM_FIELD_ID_SQUAD_OWNER=
OWNERSHIP_FILE="./cli/config/ownership.csv.sample"
CSV_OUTPUT_FILE="./cli/data/hai-on-hackerone-output.csv"
```

## Docker Usage

To run the script, simply execute the following command:

```bash
docker-compose up
```

This will start the Python script and begin processing reports.

## CLI Usage

The CLI tool accepts the following arguments:

- `-Fr, --rating`: Filter by severity **rating**
- `-Fs, --state`: Filter by report **state**
- `-r, --report`: Specific report ID(s) to retrieve
- `-ch, --comment_hai`: Post private comment based on HackerOne AI response
- `-cfh, --custom_field_hai`: Update custom fields based on HackerOne AI response
- `-csv, --csv_output`: Output HackerOne AI responses to CSV file
- `-v, --verbose`: Increase output verbosity

## CLI Examples

This will retrieve critical vulnerability reports for the specified program:

```python
python3 main.py -Fr critical
```

This will retrieve a specific report to be assessed on validity and its custom field will be updated:

```python
python3 main.py -r 12345 --custom_field_hai
```

## Webhook Endpoint

The project also includes a webhook endpoint that can be used to receive and process reports. To use this endpoint, you'll need to configure your HackerOne API settings in the `.env` file.

Here's an example of how you can use the webhook endpoint:

```bash
curl -X POST \
  http://localhost:5000/webhook \
  -H 'Content-Type: application/json' \
  -d '{"data": {"report": {"id": "12345"}}}'
```

This will trigger the webhook endpoint to process the report with ID `12345`.

## Testing

Tests will run on each pull request and merge to the primary branch. To run them locally:

```bash
pytest 
```

## Contributing

Contributions are welcome! Please open an issue or PR for any enhancements.

## Troubleshooting

If you encounter any issues, please report them.
