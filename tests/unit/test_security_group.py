import aws_cdk as cdk
import aws_cdk.assertions as assertions

from aws_cdk_15.aws_cdk_15_stack import AwsCdk15Stack

def test_security_group():
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
        'AWS::EC2::SecurityGroup',
        3)
    template.has_resource_properties(
        'AWS::EC2::SecurityGroup',
        {
            'GroupDescription': 'for ALB',
            'Tags': [{
                'Key': 'Name',
                'Value': '-'.join([
                    system_name,
                    env_type,
                    'sg-alb'
                ])
            }],
            'VpcId': {
                'Ref': 'Vpc'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SecurityGroup',
        {
            'GroupDescription': 'for EC2',
            'Tags': [{
                'Key': 'Name',
                'Value': '-'.join([
                    system_name,
                    env_type,
                    'sg-ec2'
                ])
            }],
            'VpcId': {
                'Ref': 'Vpc'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SecurityGroup',
        {
            'GroupDescription': 'for RDS',
            'Tags': [{
                'Key': 'Name',
                'Value': '-'.join([
                    system_name,
                    env_type,
                    'sg-rds'
                ])
            }],
            'VpcId': {
                'Ref': 'Vpc'
            }
        }
    )
    template.resource_count_is(
        'AWS::EC2::SecurityGroupIngress',
        4)
    template.has_resource_properties(
        'AWS::EC2::SecurityGroupIngress',
        {
            'IpProtocol': 'tcp',
            'CidrIp': '0.0.0.0/0',
            'FromPort': 80,
            'ToPort': 80,
            'GroupId': {
                'Fn::GetAtt': [
                    "SecurityGroupAlb",
                    "GroupId"
                ]
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SecurityGroupIngress',
        {
            'IpProtocol': 'tcp',
            'CidrIp': '0.0.0.0/0',
            'FromPort': 443,
            'ToPort': 443,
            'GroupId': {
                'Fn::GetAtt': [
                    "SecurityGroupAlb",
                    "GroupId"
                ]
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SecurityGroupIngress',
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'GroupId': {
                'Fn::GetAtt': [
                    "SecurityGroupEc2",
                    "GroupId"
                ]
            },
            'SourceSecurityGroupId': {
                'Fn::GetAtt': [
                    "SecurityGroupAlb",
                    "GroupId"
                ]
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SecurityGroupIngress',
        {
            'IpProtocol': 'tcp',
            'FromPort': 3306,
            'ToPort': 3306,
            'GroupId': {
                'Fn::GetAtt': [
                    "SecurityGroupRds",
                    "GroupId"
                ]
            },
            'SourceSecurityGroupId': {
                'Fn::GetAtt': [
                    "SecurityGroupEc2",
                    "GroupId"
                ]
            }
        }
    )
    """
    template.has_resource_properties(
        'AWS::EC2::VPC',
        {
            'CidrBlock': '10.0.0.0/16',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'vpc'
                    ])
                }
            ]
        }
    )
    """
