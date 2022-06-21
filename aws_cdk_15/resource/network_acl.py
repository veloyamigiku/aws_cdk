from aws_cdk_15.resource.abstract.resource import Resource

import aws_cdk as cdk
from aws_cdk.aws_ec2 import CfnNetworkAcl
from aws_cdk.aws_ec2 import CfnNetworkAclEntry
from aws_cdk.aws_ec2 import CfnSubnet
from aws_cdk.aws_ec2 import CfnSubnetNetworkAclAssociation
from aws_cdk.aws_ec2 import CfnVPC


class AssociationInfo:

    def __init__(
        self,
        id: str,
        subnet_prop_name) -> None:
        self.id = id
        self.subnet_prop_name = subnet_prop_name

class ResourceInfo:

    def __init__(
        self,
        id: str,
        resource_name: str,
        entry_id_inbound: str,
        entry_id_outbound: str,
        associations: list[AssociationInfo],
        prop_name: str) -> None:
        self.id = id
        self.resource_name = resource_name
        self.entry_id_inbound = entry_id_inbound
        self.entry_id_outbound = entry_id_outbound
        self.associations = associations
        self.prop_name = prop_name

class NetworkAcl(Resource):

    def __init__(
        self,
        vpc: CfnVPC,
        subnet_public_1a: CfnSubnet,
        subnet_public_1c: CfnSubnet,
        subnet_app_1a: CfnSubnet,
        subnet_app_1c: CfnSubnet,
        subnet_db_1a: CfnSubnet,
        subnet_db_1c: CfnSubnet) -> None:
        
        super().__init__()
        self.public = None
        self.app = None
        self.db = None
        self.vpc = vpc
        self.subnet_public_1a = subnet_public_1a
        self.subnet_public_1c = subnet_public_1c
        self.subnet_app_1a = subnet_app_1a
        self.subnet_app_1c = subnet_app_1c
        self.subnet_db_1a = subnet_db_1a
        self.subnet_db_1c = subnet_db_1c
        self.resources = [
            ResourceInfo(
                id='NetworkAclPublic',
                resource_name='nacl-public',
                entry_id_inbound='NetworkAclEntryInboundPublic',
                entry_id_outbound='NetworkAclEntryOutboundPublic',
                associations=[
                    AssociationInfo(
                        id='NetworkAclAssociationPublic1a',
                        subnet_prop_name='subnet_public_1a'),
                    AssociationInfo(
                        id='NetworkAclAssociationPublic1c',
                        subnet_prop_name='subnet_public_1c')
                ],
                prop_name='public'
            ),
            ResourceInfo(
                id='NetworkAclApp',
                resource_name='nacl-app',
                entry_id_inbound='NetworkAclEntryInboundApp',
                entry_id_outbound='NetworkAclEntryOutboundApp',
                associations=[
                    AssociationInfo(
                        id='NetworkAclAssociationApp1a',
                        subnet_prop_name='subnet_app_1a'),
                    AssociationInfo(
                        id='NetworkAclAssociationApp1c',
                        subnet_prop_name='subnet_app_1c')
                ],
                prop_name='app'
            ),
            ResourceInfo(
                id='NetworkAclDb',
                resource_name='nacl-db',
                entry_id_inbound='NetworkAclEntryInboundDb',
                entry_id_outbound='NetworkAclEntryOutboundDb',
                associations=[
                    AssociationInfo(
                        id='NetworkAclAssociationDb1a',
                        subnet_prop_name='subnet_db_1a'),
                    AssociationInfo(
                        id='NetworkAclAssociationDb1c',
                        subnet_prop_name='subnet_db_1c')
                ],
                prop_name='db'
            ),
        ]
    
    def create_entry(
        self,
        stack: cdk.Stack,
        id: str,
        network_acl: CfnNetworkAcl,
        egress: bool) -> None:

        CfnNetworkAclEntry(
            stack,
            id,
            network_acl_id=network_acl.ref,
            protocol=-1,
            rule_action='allow',
            rule_number=100,
            cidr_block='0.0.0.0/0',
            egress=egress
        )

    
    def create_association(
        self,
        stack: cdk.Stack,
        association_info: AssociationInfo,
        network_acl: CfnNetworkAcl) -> None:

        CfnSubnetNetworkAclAssociation(
            stack,
            association_info.id,
            network_acl_id=network_acl.ref,
            subnet_id=getattr(self, association_info.subnet_prop_name).ref
        )
    
    def create_network_acl(
        self,
        stack: cdk.Stack,
        resource_info: ResourceInfo) -> CfnNetworkAcl:

        network_acl = CfnNetworkAcl(
            stack,
            resource_info.id,
            vpc_id=self.vpc.ref,
            tags=[
                {
                    'key': 'Name',
                    'value': self.create_resource_name(
                        stack,
                        resource_info.resource_name)
                }
            ]
        )

        self.create_entry(
            stack,
            resource_info.entry_id_inbound,
            network_acl,
            False)
        self.create_entry(
            stack,
            resource_info.entry_id_outbound,
            network_acl,
            True)
        
        for association_info in resource_info.associations:
            self.create_association(
                stack,
                association_info,
                network_acl)
        
        return network_acl
    
    def create_resources(
        self,
        stack: cdk.Stack) -> None:

        for resource_info in self.resources:
            network_acl = self.create_network_acl(
                stack,
                resource_info)
            setattr(self, resource_info.prop_name, network_acl)
    