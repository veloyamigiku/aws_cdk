import aws_cdk as cdk
import aws_cdk.assertions as assertions

from aws_cdk_15.aws_cdk_15_stack import AwsCdk15Stack

def test_iam_role():
    system_name = 'starwars'
    env_type = 'prd'
    app = cdk.App(context={
        'systemName': system_name,
        'envType': env_type
    })
    stack = AwsCdk15Stack(app, "aws-cdk-15")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is(
        'AWS::IAM::Role',
        2)
    template.has_resource_properties(
        'AWS::IAM::Role',
        {
            'AssumeRolePolicyDocument': {
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Principal': {
                            'Service': {
                                'Fn::Join': [
                                    '',
                                    [
                                        'ec2.',
                                        {
                                            'Ref': 'AWS::URLSuffix'
                                        }
                                    ]
                                ]
                            }
                        },
                        'Action': 'sts:AssumeRole'
                    }
                ]
            },
            'ManagedPolicyArns': [
                'arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore',
                'arn:aws:iam::aws:policy/AmazonRDSFullAccess'
            ],
            'RoleName': "-".join([system_name, env_type, 'role-ec2'])
        }
    )
    template.has_resource_properties(
        'AWS::IAM::Role',
        {
            'AssumeRolePolicyDocument': {
                'Statement': [
                    {
                        'Effect': 'Allow',
                        'Principal': {
                            'Service': 'monitoring.rds.amazonaws.com'
                        },
                        'Action': 'sts:AssumeRole'
                    }
                ]
            },
            'ManagedPolicyArns': [
                'arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole'
            ],
            'RoleName': "-".join([system_name, env_type, 'role-rds'])
        }
    )

    template.resource_count_is(
        'AWS::IAM::InstanceProfile',
        1)
    template.has_resource_properties(
        'AWS::IAM::InstanceProfile',
        {
            'Roles': [
                {
                    'Ref': 'RoleEc2'
                }
            ],
            'InstanceProfileName': '-'.join([system_name, env_type, 'role-ec2'])
        }
    )