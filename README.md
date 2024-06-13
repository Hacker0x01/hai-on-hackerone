![image info](images/haigh-on-h1onh1.webp)

# H(a)igh on HackerOne

This script allows retrieving and processing reports from the HackerOne API. It can fetch reports matching specified filters, send them to the HackerOne AI for triage, and perform actions like posting comments and populating custom fields based on the AI response.

## Usage

The script accepts the following arguments:

- `-Fr, --rating`: Filter by severity **rating**
- `-Fs, --state`: Filter by report **state**
- `-r, --report`: Specific report ID(s) to retrieve
- `-ch, --comment_hai`: Post private comment based on HackerOne AI response
- `-cfh, --custom_field_hai`: Update custom fields based on HackerOne AI response
- `-csv, --csv_output`: Output HackerOne AI responses to CSV file
- `-v, --verbose`: Increase output verbosity

## Examples

This will retrieve critical vulnerability reports for the specified program:

```
python3 main.py -Fr critical
```

This will retrieve a specific report to be assessed on validity and its custom field will be updated:

```
python3 main.py -r 2332211 --custom_field_hai
```

## Requirements

- Python 3.6+
- `requests` module
- HackerOne API credentials (API token, API identifier)

## About credentials

Ensure that you grant HAI access to the API token.

To do this, navigate to https://support-app.inverselink.com/support/better_features/hai and select 'Enable for users'. Then, input the name of the API token and press 'Enable'.

## Setup

1. Clone the repository
2. Install dependencies: `pip3 install -r requirements.txt`
3. Create an `.env` file (`touch .env`)
4. Add credentials with Hai access to `.env` file, see example:

```
API_NAME=<name>
API_KEY=<token>
PROGRAM_ID=<handle>
```

5. Run the script with desired options. See usage for tips.

## Features

- Retrieve reports matching filters for program, severity, state
- Output reports as PDFs (if enabled for program)
- Send reports to HackerOne AI for triage
- Post private comments on reports based on AI decision
- Update custom fields on reports based on AI

## To Do

- Improve error handling
- Add more tests
- Async report retrieval

## Useful resources

- https://docs.google.com/document/d/1BK-kAvcJ9q8hwExKCW2yS0ESeuD4LX4upzfA3QEGUtI/edit
- https://hackerone.atlassian.net/wiki/spaces/TRIAGE/pages/3878125575/Triage+HAI+Cheat+Sheet
- https://api.hackerone.com/customer-resources/?python#customer-resources

## Contributing

Contributions are welcome! Please open an issue or PR for any enhancements.

## Credits

Credits go to Dane Sherrets (@dane) and Antoine Williams-Baisy (@antoine) for the first-time inspiration. This project is forked from this [repository](https://gitlab.inverselink.com/hackerone/engineering_and_product/sa-team/disclosure-assistance-hai/-/tree/main?ref_type=heads).
