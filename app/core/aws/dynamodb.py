from typing import Any

from app.core.aws.base import BaseService
from app.core.logging import logger
from app.exceptions import DynamoDBServiceError


class DynamoDBService(BaseService):
    def _get_service_name(self):
        return 'dynamodb'

    async def create_table(
        self,
        name: str,
        attribute_definitions: list[dict],
        key_schema: list[dict],
        provisioned_throughput: dict,
    ) -> None:
        async for dynamodb in self._get_client():
            try:
                await dynamodb.create_table(
                    TableName=name,
                    AttributeDefinitions=attribute_definitions,
                    KeySchema=key_schema,
                    ProvisionedThroughput=provisioned_throughput,
                )
            except dynamodb.exceptions.ResourceInUseException:
                logger.error(f"DynamoDB table '{name}' already exists")
                raise DynamoDBServiceError(f"DynamoDB table '{name}' already exists")
            except Exception as e:
                logger.exception(f'Error creating DynamoDB table: {str(e)}')
                raise DynamoDBServiceError(f'Error creating DynamoDB table: {str(e)}')

    async def query(
        self,
        table: str,
        expression: str,
        names: dict,
        values: dict,
        limit: int,
        scan_forward: bool,
    ) -> Any | None:
        async for dynamodb in self._get_client():
            response = await dynamodb.query(
                TableName=table,
                KeyConditionExpression=expression,
                ExpressionAttributeNames=names,
                ExpressionAttributeValues=values,
                Limit=limit,
                ScanIndexForward=scan_forward,
            )

            return response.get('Items')

        return None

    async def put(self, table: str, item: dict) -> None:
        async for dynamodb in self._get_client():
            try:
                await dynamodb.put_item(TableName=table, Item=item)
            except dynamodb.exceptions.ResourceNotFoundException:
                raise DynamoDBServiceError(f"The specified tabel '{table}' does not found.")
