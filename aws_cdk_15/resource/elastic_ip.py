import aws_cdk as cdk
from aws_cdk.aws_ec2 import CfnEIP

from aws_cdk_15.resource.abstract.resource import Resource

class ResourceInfo:

    def __init__(
        self,
        id: str,
        resource_name: str,
        prop_name: str) -> None:
        self.id = id
        self.resource_name = resource_name
        self.prop_name = prop_name
    
class ElasticIp(Resource):

    ngw1a = None
    ngw1c = None
    resource_info = [
        ResourceInfo(
            id='ElasticIpNgw1a',
            resource_name='eip-ngw-1a',
            prop_name='ngw1a'
        ),
        ResourceInfo(
            id='ElasticIpNgw1c',
            resource_name='eip-ngw-1c',
            prop_name='ngw1c'
        )
    ]

    def create_resources(
        self,
        stack: cdk.Stack) -> None:
        
        for resource_info in self.resource_info:
            elastic_ip = self.create_elastic_ip(
                stack,
                resource_info)
            setattr(self, resource_info.prop_name, elastic_ip)
    
    def create_elastic_ip(
        self,
        stack: cdk.Stack,
        resource_info: ResourceInfo) -> CfnEIP:

        elastic_ip = CfnEIP(
            stack,
            resource_info.id,
            domain='vpc',
            tags=[
                {
                    'key': 'Name',
                    'value': self.create_resource_name(
                        stack,
                        resource_info.resource_name)
                }
            ]
        )
        return elastic_ip