"""
AWS Estimated Resource Pricing Constants (Standard US East baseline).
Used to calculate monthly wasted dollars.
"""

# Hourly rates ($)
NAT_GATEWAY_HOURLY_COST = 0.045       # ~$32.40 / month (720h)
UNASSOCIATED_EIP_HOURLY_COST = 0.005  # ~$3.60 / month (720h)

# Storage per GB-Month ($)
EBS_STORAGE_PER_GB = {
    "gp3": 0.08,
    "gp2": 0.10,
    "io1": 0.125,
    "io2": 0.125,
    "st1": 0.045,
    "sc1": 0.015,
    "standard": 0.05,
}
DEFAULT_EBS_PER_GB = 0.08

SNAPSHOT_STORAGE_PER_GB = 0.05        # Standard EBS Snapshot storage
ECR_STORAGE_PER_GB = 0.10             # Elastic Container Registry storage per GB-month

HOURS_PER_MONTH = 720


def calculate_nat_waste(hours: int = HOURS_PER_MONTH) -> float:
    return round(NAT_GATEWAY_HOURLY_COST * hours, 2)


def calculate_eip_waste(hours: int = HOURS_PER_MONTH) -> float:
    return round(UNASSOCIATED_EIP_HOURLY_COST * hours, 2)


def calculate_ebs_waste(volume_type: str, size_gb: int) -> float:
    rate = EBS_STORAGE_PER_GB.get(volume_type.lower(), DEFAULT_EBS_PER_GB)
    return round(rate * size_gb, 2)


def calculate_snapshot_waste(size_gb: int) -> float:
    return round(SNAPSHOT_STORAGE_PER_GB * size_gb, 2)


def calculate_ecr_waste(size_bytes: int) -> float:
    size_gb = size_bytes / (1024 ** 3)
    return round(ECR_STORAGE_PER_GB * size_gb, 2)
