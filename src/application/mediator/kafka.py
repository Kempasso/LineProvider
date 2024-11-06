import asyncio
import json
from asyncio import Queue
from typing import Any

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from src.config import server


class KafkaMediator:
    def __init__(self):
        self.bootstrap_servers = server.conf.kafka.bootstrap_servers

    async def remote_call(self, topic, data):
        producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers
        )
        await producer.start()
        try:
            await producer.send(topic, data.encode())
        finally:
            await producer.stop()

    async def _make_read_topic(self, service_name) -> str:
        return f"{service_name}-to-service"

    async def _make_write_topic(self, service_name) -> str:
        return f"{service_name}-to-server"

    async def listener(self, service_name: str, queue: Queue):
        topic = await self._make_read_topic(service_name)
        consumer = AIOKafkaConsumer(
            topic, bootstrap_servers=self.bootstrap_servers
        )
        await consumer.start()
        async for message in consumer:
            try:
                await queue.put(message)
            except Exception as e:
                print(e)

    async def data_producer(
        self,
        service_name: str,
        queue: Queue,
        access_methods: dict[str, Any]
    ):
        producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers
        )
        send_topic = await self._make_write_topic(service_name)
        await producer.start()
        while True:
            if queue.empty():
                await asyncio.sleep(2.5)
            message = await queue.get()
            request_key = message.key.decode()
            data = json.loads(message.value.decode())
            method = access_methods.get(data.get('action'))
            if not method:
                continue
            response = await method()
            if response:
                await producer.send(
                    send_topic,
                    json.dumps(response).encode(),
                    key=request_key.encode()
                )