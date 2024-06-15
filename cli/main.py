"""
Main module
"""
import argparse
import asyncio
import sys
from reports import get_all_reports, get_reports
from utils import print_banner, bcolors

# Print the banner
print_banner()

def parse_args():
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: The parsed command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", help="Specific report ID(s) to fetch", action="append")
    parser.add_argument("-r", "--rating", help="Filter reports based on severity", choices=["none", "low", "medium", "high", "critical"])
    parser.add_argument("-s", "--state", help="Filter reports based on state", choices=["new", "triaged", "pending-program-review", "needs-more-info", "resolved", "not-applicable", "informative", "duplicate", "spam", "retesting"])
    parser.add_argument("-i", "--reference", help="Filter reports based on NOT having an issue tracker reference", action="store_true")
    parser.add_argument("-c", "--comment_hai", help="Have Hai make a private comment to the reviewed report", action="store_true")
    parser.add_argument("-f", "--custom_field_hai", help="Have Hai update a specific custom field", action="store_true")
    parser.add_argument("-o", "--csv_output", action="store_true", help="Output Hai responses to CSV file")
    parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()

def run(cli_args):
    """
    Run the CLI application.

    Args:
        cli_args (argparse.Namespace): The parsed command line arguments.
    """
    report_list = cli_args.report
    severity = cli_args.rating
    state = cli_args.state
    reference = cli_args.reference
    comment_hai_flag = cli_args.comment_hai
    custom_field_hai_flag = cli_args.custom_field_hai
    csv_output_flag = cli_args.csv_output
    verbose = cli_args.verbose

    async def main():
        if report_list:
            print(f"{bcolors.OKCYAN}Retrieving specified reports{bcolors.ENDC}")
            await get_reports(report_list, severity, state, comment_hai_flag, custom_field_hai_flag, csv_output_flag, verbose)
        else:
            print(f"{bcolors.OKCYAN}Retrieving all reports matching criteria{bcolors.ENDC}")
            await get_all_reports(severity, state, reference, comment_hai_flag, custom_field_hai_flag, csv_output_flag, verbose)

    asyncio.run(main())

if __name__ == "__main__":
    args = parse_args()
    run(args)
