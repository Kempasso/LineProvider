from typing import Annotated

from fastapi import APIRouter, Depends

from src.application.manager import ServiceManager, get_service_manager
from src.application.mediator.redis import RedisClient, get_redis_mediator
from src.domain.events.schemas import UpdateEvent, Event

router = APIRouter(prefix="/events", tags=["events"])


@router.patch("/{event_id}")
async def update_event(
    event_id: str,
    update_event: UpdateEvent,
    manager: Annotated[
        ServiceManager,
        Depends(get_service_manager)
    ]
) -> Event:
    return await manager.events.update_event(
        event_id=event_id,
        update_event=update_event
    )


@router.post("/")
async def create_event(
    event_data: Event,
    redis_mediator: Annotated[
        RedisClient,
        Depends(get_redis_mediator)
    ]
) -> Event:
    storage_info = dict(
        collection_name="events",
        key=event_data.id,
        value=event_data.model_dump_json()
    )
    await redis_mediator.update_collection_element(**storage_info)
    return event_data
