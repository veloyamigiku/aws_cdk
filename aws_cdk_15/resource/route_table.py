import aws_cdk as cdk

from aws_cdk.aws_ec2 import CfnInternetGateway
from aws_cdk.aws_ec2 import CfnRoute
from aws_cdk.aws_ec2 import CfnRouteTable
from aws_cdk.aws_ec2 import CfnSubnet
from aws_cdk.aws_ec2 import CfnSubnetRouteTableAssociation
from aws_cdk.aws_ec2 import CfnVPC


from aws_cdk_15.resource.abstract.resource import Resource

class RouteInfo:

    def __init__(
        self,
        id: str,
        destination_cidr_block: str,
        gateway_prop_name=None,
        nat_gateway_prop_name=None) -> None:
        
        self.id = id
        self.destination_cidr_block = destination_cidr_block
        self.gateway_prop_name = gateway_prop_name
        self.nat_gateway_prop_name = nat_gateway_prop_name

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
        routes: list[RouteInfo],
        associations: list[AssociationInfo],
        prop_name: str) -> None:
        
        self.id = id
        self.resource_name = resource_name
        self.routes = routes
        self.associations = associations
        self.prop_name = prop_name

class RouteTable(Resource):

    def __init__(
        self,
        vpc: CfnVPC,
        subnet_public_1a: CfnSubnet,
        subnet_public_1c: CfnSubnet,
        subnet_app_1a: CfnSubnet,
        subnet_app_1c: CfnSubnet,
        subnet_db_1a: CfnSubnet,
        subnet_db_1c: CfnSubnet,
        internet_gateway: CfnInternetGateway) -> None:

        super().__init__()
        self.public = None
        self.app1a = None
        self.app1c = None
        self.db = None
        self.vpc = vpc
        self.subnet_public_1a = subnet_public_1a
        self.subnet_public_1c = subnet_public_1c
        self.subnet_app_1a = subnet_app_1a
        self.subnet_app_1c = subnet_app_1c
        self.subnet_db_1a = subnet_db_1a
        self.subnet_db_1c = subnet_db_1c
        self.internet_gateway = internet_gateway
        self.resources = [
            ResourceInfo(
                id='RouteTablePublic',
                resource_name='rtb-public',
                routes=[
                    RouteInfo(
                        id='RoutePublic',
                        destination_cidr_block='0.0.0.0/0',
                        gateway_prop_name='internet_gateway')
                ],
                associations=[
                    AssociationInfo(
                        id='AssociationPublic1a',
                        subnet_prop_name='subnet_public_1a'),
                    AssociationInfo(
                        id='AssociationPublic1c',
                        subnet_prop_name='subnet_public_1c'),
                ],
                prop_name='public'
            ),
            ResourceInfo(
                id='RouteTableApp1a',
                resource_name='rtb-app-1a',
                routes=[
                    #RouteInfo(
                    #    id='RouteApp1a',
                    #    destination_cidr_block='0.0.0.0/0',
                    #    nat_gateway_prop_name='nat_gateway_1a')
                ],
                associations=[
                    AssociationInfo(
                        id='AssociationApp1a',
                        subnet_prop_name='subnet_app_1a'
                    )
                ],
                prop_name='app1a'
            ),
            ResourceInfo(
                id='RouteTableApp1c',
                resource_name='rtb-app-1c',
                routes=[
                    #RouteInfo(
                    #    id='RouteApp1c',
                    #    destination_cidr_block='0.0.0.0/0',
                    #    nat_gateway_prop_name='nat_gateway_1c')
                ],
                associations=[
                    AssociationInfo(
                        id='AssociationApp1c',
                        subnet_prop_name='subnet_app_1c'
                    )
                ],
                prop_name='app1c'
            ),
            ResourceInfo(
                id='RouteTableDb',
                resource_name='rtb-db',
                routes=[],
                associations=[
                    AssociationInfo(
                        id='AssociationDb1a',
                        subnet_prop_name='subnet_db_1a'),
                    AssociationInfo(
                        id='AssociationDb1c',
                        subnet_prop_name='subnet_db_1c'),
                ],
                prop_name='db'
            )
        ]
    
    def create_resources(
        self,
        stack: cdk.Stack):
        
        for resource_info in self.resources:
            route_table = self.create_route_table(
                stack,
                resource_info)
            setattr(self, resource_info.prop_name, route_table)

    def create_route_table(
        self,
        stack: cdk.Stack,
        resource_info: ResourceInfo) -> CfnRouteTable:
        
        route_table = CfnRouteTable(
            stack,
            resource_info.id,
            vpc_id=self.vpc.ref,
            tags=[
                {
                    'key': 'Name',
                    'value': self.create_resource_name(
                        stack,
                        resource_info.resource_name
                    )
                }
            ]
        )
        
        for route_info in resource_info.routes:
            self.create_route(
                stack,
                route_info,
                route_table)
        
        for association_info in resource_info.associations:
            self.create_association(
                stack,
                association_info,
                route_table)
        
        return route_table

    def create_route(
        self,
        stack: cdk.Stack,
        route_info: RouteInfo,
        route_table: CfnRouteTable):
        
        route = CfnRoute(
            stack,
            route_info.id,
            route_table_id=route_table.ref,
            destination_cidr_block=route_info.destination_cidr_block)
        
        if getattr(self, route_info.gateway_prop_name):
            route.gateway_id = getattr(self, route_info.gateway_prop_name).ref
        elif getattr(self, route_info.nat_gateway_prop_name):
            route.nat_gateway_id = getattr(self, route_info.nat_gateway_prop_name).ref

    def create_association(
        self,
        stack: cdk.Stack,
        association_info: AssociationInfo,
        route_table: CfnRouteTable):
        
        CfnSubnetRouteTableAssociation(
            stack,
            association_info.id,
            route_table_id=route_table.ref,
            subnet_id=getattr(self, association_info.subnet_prop_name).ref
        )
