from src.application.service.base import BaseService
from src.domain.events.schemas import Event, UpdateEvent


class EventsService(BaseService):

    def __init__(self):
        super().__init__()
        self.service_name = "events"
        self.call_methods = {"get_events": self.get_events}

    async def get_events(
        self,
    ) -> list[Event] | list:

        collection = await self.redis_mediator.all_collection_elements(
            self.service_name
        )
        response = []
        for ev in collection.values():
            encoded_event_str = ev.decode()
            event_instance = Event.model_validate_json(encoded_event_str)
            response.append(event_instance.model_dump())
        return response

    async def update_event(self, event_id: str, update_event: UpdateEvent):
        storage_info = dict(
            collection_name="events", key=event_id
        )
        current_event = await self.redis_mediator.get_collection_element(
            **storage_info
        )
        event = Event.model_validate_json(current_event)
        update_event.event_id = event_id
        new_event = event.copy(update=update_event.model_dump())
        storage_info["value"] = new_event.model_dump_json()
        await self.redis_mediator.update_collection_element(**storage_info)
        await self.kafka_mediator.remote_call(
            topic="events_changes", data=update_event.model_dump_json()
        )
        return new_event

