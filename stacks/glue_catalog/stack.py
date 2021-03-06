from aws_cdk import core
from aws_cdk import (
    aws_s3 as s3,
)
from stacks import active_environment
from stacks.data_lake.base import BaseDataLakeBucket
from stacks.glue_catalog.base import (
    BaseDataLakeGlueDatabase,
    BaseDataLakeGlueRole,
    BaseGlueCrawler,
    OrdersTable,
)


class GlueCatalogStack(core.Stack):
    def __init__(
            self, scope: core.Construct, data_lake_bucket: BaseDataLakeBucket, **kwargs
    ) -> None:
        self.data_lake_bucket = data_lake_bucket
        self.deploy_env = active_environment
        super().__init__(scope, id=f"{self.deploy_env.value}-glue-catalog", **kwargs)

        self.database = BaseDataLakeGlueDatabase(
            self, data_lake_bucket=self.data_lake_bucket
        )

        self.role = BaseDataLakeGlueRole(self, data_lake_bucket=self.data_lake_bucket)

        self.atomic_events_crawler = BaseGlueCrawler(
            self,
            glue_database=self.database,
            glue_role=self.role,
            table_name="atomic_events",
            schedule_expression="cron(0/15 * * * ? *)",
        )

        self.atomic_events_crawler.node.add_dependency(self.role)
        self.atomic_events_crawler.node.add_dependency(self.database)

        self.orders_table = OrdersTable(
            self, glue_database=self.database, glue_role=self.role
        )
