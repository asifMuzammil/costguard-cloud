import argparse
import sys
import os
import boto3
from typing import List
from costguard.scanners.ebs import scan_unattached_ebs
from costguard.scanners.eip import scan_unassociated_eips
from costguard.scanners.nat_gateway import scan_idle_nat_gateways
from costguard.scanners.ecr import scan_untagged_ecr_images
from costguard.report import generate_text_report, generate_json_report, generate_html_report
import json


DEFAULT_REGIONS = ["us-east-1", "us-east-2", "us-west-2", "ap-south-1", "eu-west-1"]


DEFAULT_OUTPUT_DIR = os.environ.get("COSTGUARD_OUTPUT_DIR", "./costguard-report")


def run_scan(regions: List[str] = None, profile: str = None, output_dir: str = None, as_json: bool = False, no_html: bool = False) -> None:
    if not output_dir:
        output_dir = DEFAULT_OUTPUT_DIR

    session = boto3.Session(profile_name=profile) if profile else boto3.Session()
    
    try:
        sts = session.client("sts")
        caller = sts.get_caller_identity()
        account_id = caller.get("Account", "Unknown")
    except Exception as e:
        print(f"❌ Error authenticating with AWS: {e}")
        print("Please configure your AWS credentials using 'aws configure' or specify a --profile.")
        sys.exit(1)

    print(f"🚀 Initializing CostGuard Cloud (AWS) Scan for Account: {account_id}...")
    
    if not regions:
        regions = DEFAULT_REGIONS

    all_findings = []

    for region in regions:
        print(f"  🔍 Scanning region: {region}...")
        try:
            ec2 = session.client("ec2", region_name=region)
            cw = session.client("cloudwatch", region_name=region)
            ecr = session.client("ecr", region_name=region)

            # 1. EBS
            all_findings.extend(scan_unattached_ebs(ec2, region))
            # 2. EIP
            all_findings.extend(scan_unassociated_eips(ec2, region))
            # 3. NAT Gateways
            all_findings.extend(scan_idle_nat_gateways(ec2, cw, region))
            # 4. ECR Containers
            all_findings.extend(scan_untagged_ecr_images(ecr, region))
        except Exception as e:
            print(f"     ⚠️ Skipping {region} (Access error: {e})")

    if as_json:
        report_json = generate_json_report(all_findings, account_id, regions)
        print(json.dumps(report_json, indent=2))
        return

    report_text = generate_text_report(all_findings, account_id, regions)
    print("\n" + report_text)

    if not no_html:
        try:
            os.makedirs(output_dir, exist_ok=True)
            html_content = generate_html_report(all_findings, account_id, regions)
            html_path = os.path.join(output_dir, "index.html")
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"📁 Detailed Interactive HTML Report generated at:\n   {os.path.abspath(html_path)}\n")
        except Exception as e:
            print(f"⚠️ Warning: Could not save HTML report ({e})")


def main():
    # Support optional 'scan' subcommand (e.g. 'costguard scan' or 'docker run ... scan')
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        sys.argv.pop(1)
    elif "scan" in sys.argv:
        sys.argv.remove("scan")

    parser = argparse.ArgumentParser(
        description="CostGuard Cloud (AWS) - 60-Second Zombie Resource & Cloud Waste Scanner"
    )
    parser.add_argument("--profile", help="AWS CLI profile name to use", default=None)
    parser.add_argument("--regions", nargs="+", help="AWS regions to scan (default: top 5)", default=None)
    parser.add_argument("--all-regions", action="store_true", help="Scan all enabled AWS regions")
    parser.add_argument("--json", action="store_true", help="Output results in JSON format")
    parser.add_argument("--output-dir", help="Directory where HTML report will be saved", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--no-html", action="store_true", help="Disable generating HTML report")

    args = parser.parse_args()

    regions = args.regions
    if args.all_regions:
        try:
            session = boto3.Session(profile_name=args.profile) if args.profile else boto3.Session()
            ec2 = session.client("ec2", region_name="us-east-1")
            regions = [r["RegionName"] for r in ec2.describe_regions()["Regions"]]
        except Exception:
            regions = DEFAULT_REGIONS

    run_scan(regions=regions, profile=args.profile, output_dir=args.output_dir, as_json=args.json, no_html=args.no_html)


if __name__ == "__main__":
    main()
