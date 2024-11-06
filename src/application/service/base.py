import asyncio
from multiprocessing import Queue

from src.application.mediator.kafka import KafkaMediator
from src.application.mediator.redis import RedisClient


class BaseService:
    kafka_mediator: KafkaMediator | None
    redis_mediator: RedisClient | None

    def __init__(self):
        self.kafka_mediator = KafkaMediator()
        self.redis_mediator = RedisClient()
        self.call_methods = dict()

    async def listener(self, service_name: str, queue: Queue):
        await self.kafka_mediator.listener(
            queue=queue, service_name=service_name
        )

    async def data_producer(self, service_name: str, queue: Queue):
        await self.kafka_mediator.data_producer(
            queue=queue,
            service_name=service_name,
            access_methods=self.call_methods
        )
