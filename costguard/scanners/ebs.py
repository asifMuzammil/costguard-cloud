from typing import List, Dict, Any
from costguard.pricing import calculate_ebs_waste


def scan_unattached_ebs(ec2_client, region: str) -> List[Dict[str, Any]]:
    """
    Finds EBS volumes in 'available' status (unattached to any EC2 instance).
    """
    waste_items = []
    paginator = ec2_client.get_paginator("describe_volumes")
    page_iterator = paginator.paginate(
        Filters=[{"Name": "status", "Values": ["available"]}]
    )

    for page in page_iterator:
        for volume in page.get("Volumes", []):
            vol_id = volume["VolumeId"]
            size_gb = volume.get("Size", 0)
            vol_type = volume.get("VolumeType", "gp3")
            create_time = volume.get("CreateTime").isoformat() if volume.get("CreateTime") else "Unknown"
            
            # Extract tags for context
            tags = {t["Key"]: t["Value"] for t in volume.get("Tags", [])}
            name = tags.get("Name", "Unnamed")

            monthly_waste = calculate_ebs_waste(vol_type, size_gb)

            waste_items.append({
                "resource_type": "Unattached EBS Volume",
                "resource_id": vol_id,
                "name": name,
                "region": region,
                "details": f"{size_gb} GB ({vol_type}), Created: {create_time[:10]}",
                "monthly_waste_usd": monthly_waste,
                "remediation_cli": f"aws ec2 delete-volume --volume-id {vol_id} --region {region}",
                "severity": "HIGH" if monthly_waste > 20 else "MEDIUM"
            })

    return waste_items
