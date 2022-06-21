import aws_cdk as cdk
from aws_cdk.aws_ec2 import CfnSubnet
from aws_cdk.aws_ec2 import CfnVPC
from constructs import Construct

from aws_cdk_15.resource.abstract.resource import Resource

class ResourceInfo:

    def __init__(
        self,
        id: str,
        cidr_block: str,
        availability_zone: str,
        resource_name: str,
        prop: str) -> None:
        self.id = id
        self.cidr_block = cidr_block
        self.availability_zone = availability_zone
        self.resource_name = resource_name
        self.prop = prop


class Subnet(Resource):

    public1a = None
    public1c = None
    app1a = None
    app1c = None
    db1a = None
    db1c = None
    vpc = None
    resource_info = None

    def __init__(
        self,
        vpc: CfnVPC) -> None:
        super().__init__()
        self.vpc = vpc
        self.resource_info = [
            ResourceInfo(
                id="SubnetPublic1a",
                cidr_block='10.0.11.0/24',
                availability_zone='ap-northeast-1a',
                resource_name='subnet-public-1a',
                prop="public1a"),
            ResourceInfo(
                id="SubnetPublic1c",
                cidr_block='10.0.12.0/24',
                availability_zone='ap-northeast-1c',
                resource_name='subnet-public-1c',
                prop="public1c"),
            ResourceInfo(
                id="SubnetApp1a",
                cidr_block='10.0.21.0/24',
                availability_zone='ap-northeast-1a',
                resource_name='subnet-app-1a',
                prop="app1a"),
            ResourceInfo(
                id="SubnetApp1c",
                cidr_block='10.0.22.0/24',
                availability_zone='ap-northeast-1c',
                resource_name='subnet-app-1c',
                prop="app1c"),
            ResourceInfo(
                id="SubnetDb1a",
                cidr_block='10.0.31.0/24',
                availability_zone='ap-northeast-1a',
                resource_name='subnet-db-1a',
                prop="db1a"),
            ResourceInfo(
                id="SubnetDb1c",
                cidr_block='10.0.32.0/24',
                availability_zone='ap-northeast-1c',
                resource_name='subnet-db-1c',
                prop="db1c"),
        ]

    def create_resources(
        self,
        stack: cdk.Stack):
        
        for ri in self.resource_info:
            subnet = self.create_subnet(
                stack,
                ri)
            setattr(self, ri.prop, subnet)
    
    def create_subnet(
        self,
        stack: Construct,
        resource_info: ResourceInfo):
        subnet = CfnSubnet(
            stack,
            resource_info.id,
            cidr_block=resource_info.cidr_block,
            vpc_id=self.vpc.ref,
            availability_zone=resource_info.availability_zone,
            tags=[
                {
                    'key': 'Name',
                    'value': self.create_resource_name(
                        stack,
                        resource_info.resource_name)
                }
            ]
        )
        return subnet
