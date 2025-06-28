import boto3
from botocore.exceptions import ClientError

def get_enabled_regions():
    ec2_client = boto3.client('ec2', region_name='us-east-1')  # us-east-1 always works
    regions = ec2_client.describe_regions(AllRegions=False)
    return [region['RegionName'] for region in regions['Regions']]

def check_default_vpcs(regions):
    default_vpc_info = {}

    for region in regions:
        ec2 = boto3.client('ec2', region_name=region)
        try:
            vpcs = ec2.describe_vpcs(
                Filters=[{'Name': 'isDefault', 'Values': ['true']}]
            )
            if vpcs['Vpcs']:
                default_vpc_info[region] = vpcs['Vpcs'][0]['VpcId']
            else:
                default_vpc_info[region] = None
        except ClientError as e:
            print(f"[{region}] Error checking VPCs: {e}")
            default_vpc_info[region] = "ERROR"

    return default_vpc_info

def main():
    print("Getting all enabled regions...")
    regions = get_enabled_regions()
    print(f"Found {len(regions)} regions.")

    print("Checking for default VPCs...")
    vpc_results = check_default_vpcs(regions)

    print("\nDefault VPC Report:")
    for region, vpc_id in vpc_results.items():
        if vpc_id:
            print(f"[{region}] Default VPC ID: {vpc_id}")
        elif vpc_id is None:
            print(f"[{region}] No default VPC")
        else:
            print(f"[{region}] Error occurred")

if __name__ == "__main__":
    main()
