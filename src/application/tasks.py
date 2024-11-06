import json
import random
from datetime import timezone, datetime, timedelta
from uuid import uuid4

from src.application.mediator.redis import RedisClient


async def initial_data():
    next_day = datetime.now(tz=timezone.utc) + timedelta(days=1)
    half_day = datetime.now(tz=timezone.utc) + timedelta(hours=12)
    mediator = RedisClient()
    for i in range(10):
        event_id = uuid4().hex
        event_end_date = random.randint(
            int(half_day.timestamp()), int(next_day.timestamp())
        )
        event_end_date = datetime.fromtimestamp(
            event_end_date, tz=timezone.utc
        ).isoformat()
        event_data = dict(
            id=event_id,
            end_date=event_end_date,
            status="wait",
            coefficient=round(random.randint(1, 7) * float(f"1.{random.randint(10,99)}"), 2)
        )
        event_data = json.dumps(event_data).encode()
        await mediator.update_collection_element(
            collection_name="events",
            key=event_id,
            value=event_data
        )
