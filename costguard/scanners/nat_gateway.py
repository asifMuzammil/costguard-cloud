from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from costguard.pricing import calculate_nat_waste


def scan_idle_nat_gateways(ec2_client, cloudwatch_client, region: str) -> List[Dict[str, Any]]:
    """
    Finds NAT Gateways that have near-zero traffic in CloudWatch over the past 7 days.
    """
    waste_items = []
    response = ec2_client.describe_nat_gateways(
        Filters=[{"Name": "state", "Values": ["available"]}]
    )

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(days=7)

    for nat in response.get("NatGateways", []):
        nat_id = nat["NatGatewayId"]
        vpc_id = nat.get("VpcId", "Unknown")
        tags = {t["Key"]: t["Value"] for t in nat.get("Tags", [])}
        name = tags.get("Name", "Unnamed")

        # Query CloudWatch metric BytesInFromSource
        is_idle = False
        bytes_transferred = 0

        try:
            metric_data = cloudwatch_client.get_metric_statistics(
                Namespace="AWS/NATGateway",
                MetricName="BytesInFromSource",
                Dimensions=[{"Name": "NatGatewayId", "Value": nat_id}],
                StartTime=start_time,
                EndTime=now,
                Period=86400 * 7,  # 7-day rollup
                Statistics=["Sum"],
            )
            datapoints = metric_data.get("Datapoints", [])
            if datapoints:
                bytes_transferred = datapoints[0].get("Sum", 0)
                # If less than 5 MB over 7 days, it's considered effectively idle
                if bytes_transferred < 5 * 1024 * 1024:
                    is_idle = True
            else:
                # No metrics emitted often means zero traffic
                is_idle = True
        except Exception:
            # If CloudWatch permission is missing or metrics unavailable, report state
            is_idle = True

        if is_idle:
            monthly_waste = calculate_nat_waste()
            mbs = round(bytes_transferred / (1024 * 1024), 2)
            waste_items.append({
                "resource_type": "Idle NAT Gateway",
                "resource_id": nat_id,
                "name": name,
                "region": region,
                "details": f"VPC: {vpc_id}, Only {mbs} MB transferred in 7 days",
                "monthly_waste_usd": monthly_waste,
                "remediation_cli": f"aws ec2 delete-nat-gateway --nat-gateway-id {nat_id} --region {region}",
                "severity": "CRITICAL"
            })

    return waste_items
