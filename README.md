# LineProvider
*The API interface is used for service purposes only; the main work is performed in a separate thread that listens to and responds to requests from the main backend. When any event is updated, the information is also sent to the main backend to update the betting data.*

*.env файл специально оставлен в гите чтобы не делать доп действия с envexampe и тд)*

### Run docker compose:
```bash
docker compose -f compose.yaml up -d
```

### Swagger:
[Тык](http://127.0.0.1:9000/api/v1/docs#)

### Endpoints:
**PATCH /api/v1/events/<event_id>**
```
Update event by id
```

**POST /api/v1/events/**
```
Create event
Body:
  {
  "id": "a4868508710243fca118287bb7873afd",
  "status": "wait",
  "coefficient": 1.5,
  "end_date": "2024-12-06T20:52:03.510Z"
}
```

#### TODO: 
1. Make custom exception handlers, but later)