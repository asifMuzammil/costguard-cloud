from typing import List, Dict, Any
from costguard.pricing import calculate_ecr_waste


def scan_untagged_ecr_images(ecr_client, region: str) -> List[Dict[str, Any]]:
    """
    Finds untagged (orphaned/dangling) container images taking up billable storage in ECR.
    """
    waste_items = []
    
    try:
        repos_response = ecr_client.describe_repositories()
    except Exception:
        return waste_items

    for repo in repos_response.get("repositories", []):
        repo_name = repo["repositoryName"]

        try:
            images_paginator = ecr_client.get_paginator("describe_images")
            images_iter = images_paginator.paginate(repositoryName=repo_name)

            untagged_count = 0
            untagged_bytes = 0

            for page in images_iter:
                for img in page.get("imageDetails", []):
                    # An image without imageTags is an untagged/dangling image
                    if not img.get("imageTags"):
                        untagged_count += 1
                        untagged_bytes += img.get("imageSizeInBytes", 0)

            if untagged_count > 0:
                monthly_waste = calculate_ecr_waste(untagged_bytes)
                mb_size = round(untagged_bytes / (1024 * 1024), 1)

                waste_items.append({
                    "resource_type": "Untagged ECR Container Images",
                    "resource_id": f"{repo_name} ({untagged_count} untagged images)",
                    "name": repo_name,
                    "region": region,
                    "details": f"{untagged_count} dangling images occupying {mb_size} MB",
                    "monthly_waste_usd": monthly_waste,
                    "remediation_cli": f"# Add an ECR Lifecycle Policy to auto-expire untagged images\naws ecr put-lifecycle-policy --repository-name {repo_name} ...",
                    "severity": "MEDIUM" if monthly_waste > 5 else "LOW"
                })

        except Exception:
            continue

    return waste_items
