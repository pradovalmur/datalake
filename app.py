from aws_cdk import core

from stacks.data_lake.stack import DatalakeStack

app = core.App()
data_lake = DatalakeStack(app)
app.synth()
