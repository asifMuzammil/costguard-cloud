from typing import List, Dict, Any
from costguard.pricing import calculate_eip_waste


def scan_unassociated_eips(ec2_client, region: str) -> List[Dict[str, Any]]:
    """
    Finds allocated Elastic IPs that are not associated with any running instance or ENI.
    """
    waste_items = []
    response = ec2_client.describe_addresses()

    for addr in response.get("Addresses", []):
        # If AssociationId or InstanceId is missing, it's unassociated
        if not addr.get("AssociationId") and not addr.get("InstanceId") and not addr.get("NetworkInterfaceId"):
            public_ip = addr.get("PublicIp", "Unknown")
            alloc_id = addr.get("AllocationId", "")
            tags = {t["Key"]: t["Value"] for t in addr.get("Tags", [])}
            name = tags.get("Name", "Unnamed")

            monthly_waste = calculate_eip_waste()

            waste_items.append({
                "resource_type": "Unassociated Elastic IP",
                "resource_id": alloc_id or public_ip,
                "name": name,
                "region": region,
                "details": f"Public IP: {public_ip} (Idle, incurring penalty)",
                "monthly_waste_usd": monthly_waste,
                "remediation_cli": f"aws ec2 release-address --allocation-id {alloc_id} --region {region}" if alloc_id else f"aws ec2 release-address --public-ip {public_ip} --region {region}",
                "severity": "LOW"
            })

    return waste_items
