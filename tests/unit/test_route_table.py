import aws_cdk as cdk
import aws_cdk.assertions as assertions

from aws_cdk_15.aws_cdk_15_stack import AwsCdk15Stack

def test_route_table():
    system_name = 'starwars'
    env_type = 'prd'
    app = cdk.App(context={
        'systemName': system_name,
        'envType': env_type
    })
    stack = AwsCdk15Stack(app, "aws-cdk-15")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is(
        'AWS::EC2::RouteTable',
        4)
    template.has_resource_properties(
        'AWS::EC2::RouteTable',
        {
            'VpcId': {
                'Ref': 'Vpc',
            },
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'rtb-public'
                    ])
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::EC2::RouteTable',
        {
            'VpcId': {
                'Ref': 'Vpc',
            },
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'rtb-app-1a'
                    ])
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::EC2::RouteTable',
        {
            'VpcId': {
                'Ref': 'Vpc',
            },
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'rtb-app-1c'
                    ])
                }
            ]
        }
    )
    template.has_resource_properties(
        'AWS::EC2::RouteTable',
        {
            'VpcId': {
                'Ref': 'Vpc',
            },
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': '-'.join([
                        system_name,
                        env_type,
                        'rtb-db'
                    ])
                }
            ]
        }
    )

    template.resource_count_is(
        'AWS::EC2::Route',
        1)#3)
    template.has_resource_properties(
        'AWS::EC2::Route',
        {
            'RouteTableId': {
                'Ref': 'RouteTablePublic'
            },
            'DestinationCidrBlock': '0.0.0.0/0',
            'GatewayId': {
                'Ref': 'InternetGateway'
            }
        }
    )

    template.resource_count_is(
        'AWS::EC2::SubnetRouteTableAssociation',
        6)
    template.has_resource_properties(
        'AWS::EC2::SubnetRouteTableAssociation',
        {
            'RouteTableId': {
                'Ref': 'RouteTablePublic',
            },
            'SubnetId': {
                'Ref': 'SubnetPublic1a'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SubnetRouteTableAssociation',
        {
            'RouteTableId': {
                'Ref': 'RouteTablePublic',
            },
            'SubnetId': {
                'Ref': 'SubnetPublic1c'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SubnetRouteTableAssociation',
        {
            'RouteTableId': {
                'Ref': 'RouteTableApp1a',
            },
            'SubnetId': {
                'Ref': 'SubnetApp1a'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SubnetRouteTableAssociation',
        {
            'RouteTableId': {
                'Ref': 'RouteTableApp1c',
            },
            'SubnetId': {
                'Ref': 'SubnetApp1c'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SubnetRouteTableAssociation',
        {
            'RouteTableId': {
                'Ref': 'RouteTableDb',
            },
            'SubnetId': {
                'Ref': 'SubnetDb1a'
            }
        }
    )
    template.has_resource_properties(
        'AWS::EC2::SubnetRouteTableAssociation',
        {
            'RouteTableId': {
                'Ref': 'RouteTableDb',
            },
            'SubnetId': {
                'Ref': 'SubnetDb1c'
            }
        }
    )