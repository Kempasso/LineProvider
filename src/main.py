import asyncio
from multiprocessing import Process
from typing import Any

from fastapi import FastAPI

from src.api import events
from src.application.manager import ServiceManager
from src.application.tasks import initial_data


async def run_listener_and_producer(service: Any, service_name: str):
    queue = asyncio.Queue(maxsize=100)
    await asyncio.gather(
        service.listener(
            queue=queue, service_name=service_name
        ),
        service.data_producer(
            queue=queue, service_name=service_name
        )
    )


def initiate_process(service: Any, service_name: str):
    asyncio.run(
        run_listener_and_producer(
            service=service,
            service_name=service_name
        )
    )


def run():
    needed_processes = ["events"]
    manager = ServiceManager()
    processes = []
    for proc_trigger in needed_processes:
        service = manager.__dict__.get(proc_trigger)
        process = Process(
            target=initiate_process(
                service=service,
                service_name=proc_trigger
            )
        )
        processes.append((proc_trigger, process))
    for _, process in processes:
        process.start()
        process.join()


async def lifespan(app: FastAPI):
    await initial_data()
    yield


base_router_path = "/api/v1"
app = FastAPI(
    lifespan=lifespan,
    docs_url=f"{base_router_path}/docs",
    openapi_url=f"{base_router_path}/openapi.json",
    description="Line Provider"
)
app.include_router(events.router, prefix=base_router_path)

if __name__ == "__main__":
    run()
