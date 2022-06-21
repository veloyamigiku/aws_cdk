import aws_cdk as cdk
from aws_cdk.aws_ec2 import CfnInternetGateway
from aws_cdk.aws_ec2 import CfnVPCGatewayAttachment
from aws_cdk.aws_ec2 import CfnVPC

from aws_cdk_15.resource.abstract.resource import Resource

class InternetGateway(Resource):

    igw = None
    vpc = None

    def __init__(
        self,
        vpc: CfnVPC) -> None:

        super().__init__()
        self.vpc = vpc
    

    def create_resources(
        self,
        stack: cdk.Stack):

        self.igw = CfnInternetGateway(
            stack,
            'InternetGateway',
            tags=[
                {
                    'key': 'Name',
                    'value': self.create_resource_name(
                        stack,
                        'igw')
                }
            ]
        )

        CfnVPCGatewayAttachment(
            stack,
            'VpcGatewayAttachment',
            vpc_id=self.vpc.ref,
            internet_gateway_id=self.igw.ref
        )
