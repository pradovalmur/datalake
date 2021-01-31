from aws_cdk import core

from stacks.data_lake.stack import DataLakeStack
from stacks.glue_catalog.stack import GlueCatalogStack
from stacks.athena.stack import AthenaStack

app = core.App()
data_lake = DataLakeStack(app)
glue_catalog = GlueCatalogStack(app, data_lake_bucket=data_lake.data_lake_raw_bucket)
athena = AthenaStack(app)
app.synth()
