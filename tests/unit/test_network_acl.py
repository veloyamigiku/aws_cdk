import aws_cdk as cdk
import aws_cdk.assertions as assertions

from aws_cdk_15.aws_cdk_15_stack import AwsCdk15Stack

def test_network_acl():
    system_name = 'starwars'
    env_type = 'prd'
    app = cdk.App(context={
        'systemName': system_name,
        'envType': env_type
    })
    stack = AwsCdk15Stack(app, "aws-cdk-15")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is(
        'AWS::EC2::NetworkAcl',
        3)
    template.has_resource_properties(
        'AWS::EC2::NetworkAcl',
        {
            'VpcId': {
                'Ref': 'Vpc'
            },
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'nacl-public'
                    ])
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::EC2::NetworkAcl',
        {
            'VpcId': {
                'Ref': 'Vpc'
            },
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'nacl-app'
                    ])
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::EC2::NetworkAcl',
        {
            'VpcId': {
                'Ref': 'Vpc'
            },
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'nacl-db'
                    ])
                }
            ]
        }
    )

    template.resource_count_is(
        'AWS::EC2::NetworkAclEntry',
        6)
    template.has_resource_properties(
        'AWS::EC2::NetworkAclEntry',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclPublic'
            },
            'Protocol': -1,
            'RuleAction': 'allow',
            'RuleNumber': 100,
            'CidrBlock': '0.0.0.0/0',
            'Egress': False
        }
    )
    template.has_resource_properties(
        'AWS::EC2::NetworkAclEntry',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclPublic'
            },
            'Protocol': -1,
            'RuleAction': 'allow',
            'RuleNumber': 100,
            'CidrBlock': '0.0.0.0/0',
            'Egress': True
        }
    )
    template.has_resource_properties(
        'AWS::EC2::NetworkAclEntry',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclApp'
            },
            'Protocol': -1,
            'RuleAction': 'allow',
            'RuleNumber': 100,
            'CidrBlock': '0.0.0.0/0',
            'Egress': False
        }
    )
    template.has_resource_properties(
        'AWS::EC2::NetworkAclEntry',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclApp'
            },
            'Protocol': -1,
            'RuleAction': 'allow',
            'RuleNumber': 100,
            'CidrBlock': '0.0.0.0/0',
            'Egress': True
        }
    )
    template.has_resource_properties(
        'AWS::EC2::NetworkAclEntry',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclDb'
            },
            'Protocol': -1,
            'RuleAction': 'allow',
            'RuleNumber': 100,
            'CidrBlock': '0.0.0.0/0',
            'Egress': False
        }
    )
    template.has_resource_properties(
        'AWS::EC2::NetworkAclEntry',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclDb'
            },
            'Protocol': -1,
            'RuleAction': 'allow',
            'RuleNumber': 100,
            'CidrBlock': '0.0.0.0/0',
            'Egress': True
        }
    )

    template.resource_count_is(
        'AWS::EC2::SubnetNetworkAclAssociation',
        6)
    template.has_resource_properties(
        'AWS::EC2::SubnetNetworkAclAssociation',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclPublic'
            },
            'SubnetId': {
                'Ref': 'SubnetPublic1a'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SubnetNetworkAclAssociation',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclPublic'
            },
            'SubnetId': {
                'Ref': 'SubnetPublic1c'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SubnetNetworkAclAssociation',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclApp'
            },
            'SubnetId': {
                'Ref': 'SubnetApp1a'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SubnetNetworkAclAssociation',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclApp'
            },
            'SubnetId': {
                'Ref': 'SubnetApp1c'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SubnetNetworkAclAssociation',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclDb'
            },
            'SubnetId': {
                'Ref': 'SubnetDb1a'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SubnetNetworkAclAssociation',
        {
            'NetworkAclId': {
                'Ref': 'NetworkAclDb'
            },
            'SubnetId': {
                'Ref': 'SubnetDb1c'
            }
        }
    )
    