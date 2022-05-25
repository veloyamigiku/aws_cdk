import aws_cdk as core
import aws_cdk.assertions as assertions

from aws_cdk_15.aws_cdk_15_stack import AwsCdk15Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in aws_cdk_15/aws_cdk_15_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = AwsCdk15Stack(app, "aws-cdk-15")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
