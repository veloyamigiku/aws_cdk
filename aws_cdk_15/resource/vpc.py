import aws_cdk as cdk
from aws_cdk.aws_ec2 import CfnVPC

from aws_cdk_15.resource.abstract.resource import Resource

class Vpc(Resource):

    vpc = None

    def __init__(self) -> None:
        super()
    
    def create_resources(
        self,
        stack: cdk.Stack):
        self.vpc = CfnVPC(
            stack,
            'Vpc',
            cidr_block='10.0.0.0/16',
            tags=[
                {
                    'key': 'Name',
                    'value': self.create_resource_name(
                        stack,
                        'vpc')
                }
            ]
        )
