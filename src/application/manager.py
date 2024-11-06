from src.application.mediator.kafka import KafkaMediator
from src.application.mediator.redis import RedisClient
from src.application.service.events import EventsService


class ServiceManager:
    events: EventsService

    def __init__(self):
        self.events: EventsService = EventsService()


async def get_service_manager():
    manager = ServiceManager()
    yield manager
