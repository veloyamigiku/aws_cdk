import aws_cdk as cdk
import aws_cdk.assertions as assertions

from aws_cdk_15.aws_cdk_15_stack import AwsCdk15Stack

def test_subnet():
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
        'AWS::EC2::Subnet',
        6)
    template.has_resource_properties(
        'AWS::EC2::Subnet',
        {
            'CidrBlock': '10.0.11.0/24',
            'AvailabilityZone': 'ap-northeast-1a',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'subnet-public-1a'
                    ])
                }
            ]
        })
    template.has_resource_properties(
        'AWS::EC2::Subnet',
        {
            'CidrBlock': '10.0.12.0/24',
            'AvailabilityZone': 'ap-northeast-1c',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'subnet-public-1c'
                    ])
                }
            ]
        })
    template.has_resource_properties(
        'AWS::EC2::Subnet',
        {
            'CidrBlock': '10.0.21.0/24',
            'AvailabilityZone': 'ap-northeast-1a',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'subnet-app-1a'
                    ])
                }
            ]
        })
    template.has_resource_properties(
        'AWS::EC2::Subnet',
        {
            'CidrBlock': '10.0.22.0/24',
            'AvailabilityZone': 'ap-northeast-1c',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'subnet-app-1c'
                    ])
                }
            ]
        })
    template.has_resource_properties(
        'AWS::EC2::Subnet',
        {
            'CidrBlock': '10.0.31.0/24',
            'AvailabilityZone': 'ap-northeast-1a',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'subnet-db-1a'
                    ])
                }
            ]
        })
    template.has_resource_properties(
        'AWS::EC2::Subnet',
        {
            'CidrBlock': '10.0.32.0/24',
            'AvailabilityZone': 'ap-northeast-1c',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'subnet-db-1c'
                    ])
                }
            ]
        })
    