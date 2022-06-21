from aws_cdk_15.resource.abstract.resource import Resource

import aws_cdk as cdk
from aws_cdk.aws_iam import CfnRole
from aws_cdk.aws_iam import CfnInstanceProfile
from aws_cdk.aws_iam import Effect
from aws_cdk.aws_iam import PolicyStatement
from aws_cdk.aws_iam import PolicyDocument
from aws_cdk.aws_iam import PolicyStatementProps
from aws_cdk.aws_iam import ServicePrincipal

class ResourceInfo:

    def __init__(
        self,
        id: str,
        policy_statement_props: PolicyStatementProps,
        managed_policy_arns: list[str],
        role_name: str,
        prop_name: str) -> None:
        
        self.id = id
        self.policy_statement_props = policy_statement_props
        self.managed_policy_arns = managed_policy_arns
        self.role_name = role_name
        self.prop_name = prop_name

class IamRole(Resource):

    def __init__(self) -> None:

        super().__init__()
        self.ec2 = None
        self.rds = None
        self.instance_profile_ec2 = None
        self.resources = [
            ResourceInfo(
                id='RoleEc2',
                policy_statement_props=PolicyStatementProps(
                    effect=Effect.ALLOW,
                    principals=[
                        ServicePrincipal('ec2.amazonaws.com')
                    ],
                    actions=['sts:AssumeRole']
                ),
                managed_policy_arns=[
                    'arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore',
                    'arn:aws:iam::aws:policy/AmazonRDSFullAccess'
                ],
                role_name='role-ec2',
                prop_name='ec2'
            ),
            ResourceInfo(
                id='RoleRds',
                policy_statement_props=PolicyStatementProps(
                    effect=Effect.ALLOW,
                    principals=[
                        ServicePrincipal('monitoring.rds.amazonaws.com')
                    ],
                    actions=['sts:AssumeRole']
                ),
                managed_policy_arns=[
                    'arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole'
                ],
                role_name='role-rds',
                prop_name='rds'
            )
        ]
    
    def create_role(
        self,
        stack: cdk.Stack,
        resource_info: ResourceInfo) -> CfnRole:
        
        policy_statement = PolicyStatement(
            effect=resource_info.policy_statement_props.effect,
            principals=resource_info.policy_statement_props.principals,
            actions=resource_info.policy_statement_props.actions)

        policy_document = PolicyDocument(statements=[policy_statement])

        role = CfnRole(
            stack,
            resource_info.id,
            assume_role_policy_document=policy_document,
            managed_policy_arns=resource_info.managed_policy_arns,
            role_name=self.create_resource_name(stack, resource_info.role_name))
        
        return role
    
    def create_resources(
        self,
        stack: cdk.Stack):

        for resource_info in self.resources:
            role = self.create_role(stack, resource_info)
            setattr(self, resource_info.prop_name, role)
        
        self.instance_profile_ec2 = CfnInstanceProfile(
            stack,
            'InstanceProfileEc2',
            roles=[self.ec2.ref],
            instance_profile_name=self.ec2.role_name)
