import string
import aws_cdk as cdk 
from abc import abstractmethod

class Resource:

    def __init__(self) -> None:
        pass

    @abstractmethod
    def create_resources(
        self,
        stack: cdk.Stack):
        pass

    def create_resource_name(
        self,
        stack: cdk.Stack,
        original_name: string):
        system_name = stack.node.try_get_context('systemName')
        env_type = stack.node.try_get_context('envType')
        return '-'.join([
            system_name,
            env_type,
            original_name
        ])