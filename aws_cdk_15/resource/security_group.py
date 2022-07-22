import aws_cdk as cdk
from aws_cdk.aws_ec2 import CfnSecurityGroup, CfnSecurityGroupIngress, CfnSecurityGroupIngressProps, CfnVPC
from aws_cdk_15.resource.abstract.resource import Resource
from typing import List

class IngressInfo:
    
    def __init__(
        self,
        id: str,
        security_group_ingress_props: CfnSecurityGroupIngressProps,
        source_security_group_prop_name: str) -> None:
        
        self.id = id
        self.security_group_ingress_props = security_group_ingress_props
        self.source_security_group_prop_name = source_security_group_prop_name

class ResourceInfo:

    def __init__(
        self,
        id: str,
        group_description: str,
        ingresses: List[IngressInfo],
        resource_name: str,
        security_group_prop_name: str) -> None:
        
        self.id = id
        self.group_description = group_description
        self.ingresses = ingresses
        self.resource_name = resource_name
        self.security_group_prop_name = security_group_prop_name

class SecurityGroup(Resource):

    def __init__(
        self,
        vpc: CfnVPC) -> None:

        super().__init__()

        self.alb = None
        self.ec2 = None
        self.rds = None
        self.vpc = vpc
        self.resources = [
            ResourceInfo(
                id='SecurityGroupAlb',
                group_description='for ALB',
                ingresses=[
                    IngressInfo(
                        id='SecurityGroupIngressAlb1',
                        security_group_ingress_props={
                            'ip_protocol': 'tcp',
                            'cidr_ip': '0.0.0.0/0',
                            'from_port': 80,
                            'to_port': 80
                        },
                        source_security_group_prop_name=None
                    ),
                    IngressInfo(
                        id='SecurityGroupIngressAlb2',
                        security_group_ingress_props={
                            'ip_protocol': 'tcp',
                            'cidr_ip': '0.0.0.0/0',
                            'from_port': 443,
                            'to_port': 443
                        },
                        source_security_group_prop_name=None
                    )
                ],
                resource_name='sg-alb',
                security_group_prop_name='alb'
            ),
            ResourceInfo(
                id='SecurityGroupEc2',
                group_description='for EC2',
                ingresses=[
                    IngressInfo(
                        'SecurityGroupIngressEc21',
                        security_group_ingress_props={
                            'ip_protocol': 'tcp',
                            'from_port': 80,
                            'to_port': 80
                        },
                        source_security_group_prop_name = 'alb'
                    )
                ],
                resource_name='sg-ec2',
                security_group_prop_name='ec2'
            ),
            ResourceInfo(
                id='SecurityGroupRds',
                group_description='for RDS',
                ingresses=[
                    IngressInfo(
                        'SecurityGroupIngressRds1',
                        security_group_ingress_props={
                            'ip_protocol': 'tcp',
                            'from_port': 3306,
                            'to_port': 3306
                        },
                        source_security_group_prop_name = 'ec2'
                    )
                ],
                resource_name='sg-rds',
                security_group_prop_name='rds'
            )
            
        ]
    
    def create_resources(
        self,
        stack: cdk.Stack):

        for resource_info in self.resources:
            security_group = self.create_security_group(
                stack,
                resource_info
            )
            setattr(self, resource_info.security_group_prop_name, security_group)

            self.create_security_group_ingress(
                stack,
                resource_info)
    
    def create_security_group(
        self,
        stack: cdk.Stack,
        resource_info: ResourceInfo):

        resource_name = self.create_resource_name(
            stack,
            resource_info.resource_name)
        security_group = CfnSecurityGroup(
            stack,
            resource_info.id,
            group_description=resource_info.group_description,
            vpc_id=self.vpc.ref,
            tags=[{
                'key': 'Name',
                'value': resource_name
            }]
        )

        return security_group
    
    def create_security_group_ingress(
        self,
        stack: cdk.Stack,
        resource_info: ResourceInfo):

        for ingress in resource_info.ingresses:
            security_group_ingress = CfnSecurityGroupIngress(
                stack,
                ingress.id,
                **ingress.security_group_ingress_props)
            security_group_ingress.group_id = getattr(self, resource_info.security_group_prop_name).attr_group_id

            if ingress.source_security_group_prop_name:
                security_group_ingress.source_security_group_id = getattr(self, ingress.source_security_group_prop_name).attr_group_id

