import requests
from ec2_metadata import EC2Metadata, ec2_metadata
from pydantic import BaseModel


class CloudProviders(BaseModel):
    instance_type: str
    region_name: str

    @staticmethod
    def is_running_on_cloud_provider() -> bool:
        """
        Check if it's running on a cloud provider.

        :return:
        """
        return AWS.is_ec2()

    @staticmethod
    def auto_detect() -> "CloudProviders":
        """
        Autodetect the cloud provider.

        :return: the cloud provider
        """
        return AWS(
            region_name=ec2_metadata.region,
            instance_type=ec2_metadata.instance_type,
        )


class AWS(CloudProviders):
    @staticmethod
    def is_ec2() -> bool:
        """
        Check if it's running on a AWS EC2 instance.

        :return: is a EC2
        """
        ec2_metadata = EC2Metadata()
        try:
            requests.head(ec2_metadata.service_url, timeout=1)
        except Exception:
            return False
        return True
