from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk_15.resource.elastic_ip import ElasticIp
from aws_cdk_15.resource.iam_role import IamRole
from aws_cdk_15.resource.internet_gateway import InternetGateway
from aws_cdk_15.resource.network_acl import NetworkAcl
from aws_cdk_15.resource.route_table import RouteTable
from aws_cdk_15.resource.subnet import Subnet
from aws_cdk_15.resource.vpc import Vpc

class AwsCdk15Stack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs) -> None:
        
        super().__init__(
            scope,
            construct_id,
            **kwargs)
        
        vpc = Vpc()
        vpc.create_resources(self)

        subnet = Subnet(vpc.vpc)
        subnet.create_resources(self)

        internet_gateway = InternetGateway(vpc.vpc)
        internet_gateway.create_resources(self)

        elastic_ip = ElasticIp()
        elastic_ip.create_resources(self)

        route_table = RouteTable(
            vpc.vpc,
            subnet.public1a,
            subnet.public1c,
            subnet.app1a,
            subnet.app1c,
            subnet.db1a,
            subnet.db1c,
            internet_gateway.igw)
        route_table.create_resources(self)

        network_acl = NetworkAcl(
            vpc.vpc,
            subnet.public1a,
            subnet.public1c,
            subnet.app1a,
            subnet.app1c,
            subnet.db1a,
            subnet.db1c)
        network_acl.create_resources(self)

        iam_role = IamRole()
        iam_role.create_resources(self)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "AwsCdk15Queue",
        #     visibility_timeout=Duration.seconds(300),
        # )
