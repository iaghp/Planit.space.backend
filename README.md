# API Specification


## Tasks (api/plan/schedule)


### Get all subtasks in a given date range

```
GET /:scheduleId/tasks

/d6544db6-8098-4cf4-ba08-872aa7015bca/tasks?startTime=2025-10-04T00:00:00.000Z&endTime=2025-10-04T22:00:00.000Z
```
##### input

| name       | example                  | type  |     |
| ---------- | ------------------------ | ----- | --- |
| startTime  | 2025-10-03T22:00:00.000Z | query |     |
| endTime    | 2025-10-03T22:00:00.000Z | query |     |
| scheduleId | UUID                     | path  |     |
#### sample output

```
[
    {
        "id": "0385250d-ccb3-4554-8d5e-5d2dc1f4ac9b",
        "name": "My New Subtask",
        "startTime": "2025-10-04 00:00:00.000",
        "endTime": "2025-10-04 00:00:00.000",
        "description": "SUBTASK: I'm just testing some stuff lol. As long as its not apples, oranges or lemons",
        "status": "PLANNED",
        "parent": {
            "id": "782a4022-67bc-4793-b1ac-09d1cabe7d99",
            "name": "My New Task",
            "deadline": "2025-10-05 00:00:00.000",
            "start": "2025-10-04 00:00:00.000"
        }
    },
    {
        "id": "baf25a5d-e73b-4a52-9341-03d215a7aa5c",
        "name": "Gemini Plan Generation",
        "startTime": "2025-10-04 08:00:00.000",
        "endTime": "2025-10-04 16:00:00.000",
        "description": "blah blah blah",
        "status": "LIVE",
        "parent": {
            "id": "53187ddb-4793-406a-b89a-9596b7b289f0",
            "name": "HAck the 10th",
            "deadline": "2025-10-05 10:00:00.000",
            "start": "2025-10-03 22:00:00.000"
        }
    }
]
```


### Get all subtasks in for today

```
GET /:scheduleId/dailyTasks
```

#### input
| name       | example | type |
| ---------- | ------- | ---- |
| scheduleId | UUID    | path |

example output:

```
[
    {
        "id": "baf25a5d-e73b-4a52-9341-03d215a7aa5c",
        "name": "Gemini Plan Generation",
        "startTime": "2025-10-04 08:00:00.000",
        "endTime": "2025-10-04 16:00:00.000",
        "description": "blah blah blah",
        "status": "LIVE",
        "parent": {
            "id": "53187ddb-4793-406a-b89a-9596b7b289f0",
            "name": "HAck the 10th",
            "deadline": "2025-10-05 10:00:00.000",
            "start": "2025-10-03 22:00:00.000"
        }
    }
]
```

## Update a task

```
PATCH /:scheduleId/task/:taskId/update
```


Body contains key/value pairs of columns to update
Example request body: 

```
{
	"status": "COMPLETE"
}
```

## Update a subtask

```
PATCH /:scheduleId/task/:taskId/subtask/:subtaskId/update
```


Body contains key/value pairs of columns to update
Example request body: 

```
{
	"name": "Updated name"
}
```


## Create a task

```
POST /:scheduleId/task
```

Example request body:
```
{
	"name": "Name",
	"context": "dsgsfgfd",
	"start": "2025-01-01",
	"deadline": "2025-06-03"
	"status": "LIVE" # defaults to 'PLANNED' if not included
}
```

Response returns: 
```
{
	id: "UUID"
}
```

## Create a subtask

```
POST /:scheduleId/task/:taskId/subtask
```

Example request body:
```
{
	"name": "Name",
	"description": "dsgsfgfd",
	"startTime": "2025-01-01",
	"endTime": "2025-06-03"
	"status": "LIVE" # defaults to 'PLANNED' if not included
}
```

Response returns: 
```
{
	id: "UUID"
}
```

## Delete task

```
DELETE /:scheduleId/task/:taskId
```


## Delete subtask

```
DELETE /:scheduleId/task/:taskId/subtask/:subtaskId
```