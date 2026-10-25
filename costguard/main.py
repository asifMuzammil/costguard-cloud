from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import boto3
from costguard.scanners.ebs import scan_unattached_ebs
from costguard.scanners.eip import scan_unassociated_eips
from costguard.scanners.nat_gateway import scan_idle_nat_gateways
from costguard.scanners.ecr import scan_untagged_ecr_images
from costguard.report import generate_json_report

app = FastAPI(
    title="CostGuard Cloud (AWS) API",
    description="Automated AWS Zombie Resource & Cloud Waste Detection Engine",
    version="1.0.0"
)


class ScanRequest(BaseModel):
    role_arn: str
    external_id: str
    regions: Optional[List[str]] = ["us-east-1", "us-east-2", "us-west-2", "ap-south-1", "eu-west-1"]


@app.get("/")
def health_check():
    return {
        "service": "CostGuard Cloud (AWS)",
        "status": "healthy",
        "description": "Ready to scan AWS accounts for wasted spend"
    }


@app.post("/api/scan")
def scan_aws_account(req: ScanRequest):
    """
    Assumes the client-provided Read-Only Cross-Account Role securely via STS.
    """
    sts_client = boto3.client("sts")

    try:
        assumed = sts_client.assume_role(
            RoleArn=req.role_arn,
            RoleSessionName="CostGuardAuditSession",
            ExternalId=req.external_id,
            DurationSeconds=900  # 15 minutes temporary token
        )
        credentials = assumed["Credentials"]
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to assume role: {str(e)}")

    account_id = req.role_arn.split(":")[4] if len(req.role_arn.split(":")) > 4 else "Unknown"

    session = boto3.Session(
        aws_access_key_id=credentials["AccessKeyId"],
        aws_secret_access_key=credentials["SecretAccessKey"],
        aws_session_token=credentials["SessionToken"]
    )

    all_findings = []

    for region in req.regions:
        try:
            ec2 = session.client("ec2", region_name=region)
            cw = session.client("cloudwatch", region_name=region)
            ecr = session.client("ecr", region_name=region)

            all_findings.extend(scan_unattached_ebs(ec2, region))
            all_findings.extend(scan_unassociated_eips(ec2, region))
            all_findings.extend(scan_idle_nat_gateways(ec2, cw, region))
            all_findings.extend(scan_untagged_ecr_images(ecr, region))
        except Exception:
            continue

    return generate_json_report(all_findings, account_id, req.regions)
