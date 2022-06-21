import aws_cdk as cdk
import aws_cdk.assertions as assertions

from aws_cdk_15.aws_cdk_15_stack import AwsCdk15Stack

def test_internet_gateway():
    system_name = 'starward'
    env_type = 'prd'
    app = cdk.App(context={
            'systemName': system_name,
            'envType': env_type
            }
    )
    stack = AwsCdk15Stack(app, "aws-cdk-15")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is(
        'AWS::EC2::InternetGateway',
        1)
    template.has_resource_properties(
        'AWS::EC2::InternetGateway',
        {
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': "-".join([
                        system_name,
                        env_type,
                        'igw'
                    ])
                }
            ]
        }
    )
    template.resource_count_is(
        'AWS::EC2::VPCGatewayAttachment',
        1)
