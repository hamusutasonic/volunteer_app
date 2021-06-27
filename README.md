# Capstone Project - Volunteer App 

## About
This is a mock API for a Volunteer App services where Non-Profit / Charitable organisations 
can post volunteering events while users who are interested to volunteer for any of these events can sign up for the event. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the directory where this repository is and run:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Running the server locally

Run a local postgres database.
Modify `setup.sh` file to update DB_HOST, DB_USER, DB_PASSWORD, DB_NAME to your local postgres setup.   

Execute `source ./setup.sh` to populate environment variables.

Populate a mock database by running
```bash
python fixtures.py
```

Start the app by running
```bash
flask run
```

## EndPoints

Endpoints are protected via OAuth2 Access Tokens. To access protected endpoints, pass in a valid token using the `Authorization: 'Bearer {ACCESS_TOKEN}'` header along with the API request. For public endpoints, no access token is required. 

#### GET /events
Get all events. 
- Permission: Public
- Request Body: None
- Response: 
    ```
    {
        "success": true,
        "data": [{
            "name": "new event",
            "address": "London SW1A 0AA, UK",
            "description": "new volunteer event",
            "start_datetime": "2021-01-12T10:00:00",
            "end_datetime": "2021-01-12T12:00:00",
            "id": 1,
            "organisation": {
                "id": 1,
                "name": "my charity organisation"
            },
            "organisation_id": 1,
            "participants": [
                {
                    "id": 1,
                    "name": "Tom"
                },
                {
                    "id": 2,
                    "name": "Sally"
                }
            ],
        }, ...]
    }
    ```

#### GET /events/{event_id}
Get details of a specific event
- Permission: Public
- Request Body: None
- Response:
    ```
    {
        "success": true,
        "data": {
            "name": "new event",
            "address": "London SW1A 0AA, UK",
            "description": "new volunteer event",
            "start_datetime": "2021-01-12T10:00:00",
            "end_datetime": "2021-01-12T12:00:00",
            "id": 1,
            "organisation": {
                "id": 1,
                "name": "my charity organisation"
            },
            "organisation_id": 1,
            "participants": [
                {
                    "id": 1,
                    "name": "Tom"
                },
                {
                    "id": 2,
                    "name": "Sally"
                }
            ],
        }
    }
    ```

#### POST /events 
Create a new event. 
- Permission: Organisation users only
- Request Body: 
    ```
    {
        "name": "event name", //required
        "organisation_id": 1, //required
        "address": "event venue",
        "description": "event description",
        "start_datetime": "2021-01-12T10:00:00",
        "end_datetime": "2021-01-12T12:00:00",
    }
    ```
- Response:
    ```
    {
        "success": true,
        "created": {
            "id": 7, //created event id
            "address": "event venue",
            "description": "event description",
            "start_datetime": "2021-01-12T10:00:00",
            "end_datetime": "2021-01-12T12:00:00",
            "name": "event name",
            "organisation": {
                "id": 1,
                "name": "my charity organisation"
            },
            "participants": []
        }
    }
    ```

#### PATCH /events/{event_id}
Update an existing event. Authenticated organisation users can only update their own events. 
- Permission: Organisation users only
- Request Body: 
    ```
    {
        "organisation_id": 1, //required
        "name": "updated name",
        "address": "new venue",
        "description": "new description",
        "start_datetime": "2021-01-12T10:00:00",
        "end_datetime": "2021-01-12T12:00:00"
    }
    ```
- Response:
    ```
    {
        "success": true,
        "updated": {
            "id": 1,
            "address": "new venue",
            "description": "new description",
            "start_datetime": "2021-01-12T10:00:00",
            "end_datetime": "2021-01-12T12:00:00",
            "name": "updated name",
            "organisation": {
                "id": 1,
                "name": "my charity organisation"
            },
            "participants": [
                {
                    "id": 1,
                    "name": "Tom"
                },
                {
                    "id": 2,
                    "name": "Sally"
                }
            ]
        }
    }
    ```

#### DELETE /events/{event_id}
Delete an event. Authenticated organisation users can only delete their own events. 
- Permission: Organisation users only
- Request Body: None
- Response:
    ```
    {
        "success": true,
        "deleted": 7  //event_id of deleted event
    }
    ```


#### POST /events/{event_id}/participants
Add a new user to event participant list. Authenticated users can only add themselves to an event. 
- Permission: Volunteer users only
- Request Body: 
    ```
    {
        "user_id": 1
    }
    ```
- Response:
    ```
    {
        "success": true,
        "updated": {
            "event_id": 1, 
            "event_participants": [1, 2, 10] //updated event participant ids
        }
    }
    ```

#### DELETE /events/{event_id}/participants
Remove a user from event participant list. Authenticated users can only remove themselves from an event. 
- Permission: Volunteer users only
- Request Body: 
    ```
    {
        "user_id": 1
    }
    ```
- Response:
    ```
    {
        "success": true,
        "updated": {
            "event_id": 1, 
            "event_participants": [2, 10] //updated event participant ids
        }
    }
    ```

#### GET /organisations
Get general information for all organisations
- Permission: Public
- Request Body: None
- Response:
    ```
    {
        "success": true,
        "data": [
            {
                "id": 1,
                "name": "my charity organisation",
                "description": "A new charity",
                "email_contact": "mycharity@test.com",
                "phone_contact": "1111111",
                "website": "http://mycharityorganisation.com"
            }, ...]
    }
    ```

#### GET /organisations/{organisation_id}
Get all information for a single organisation, included past and upcoming events.
- Permission: Public
- Request Body: None
- Response:
    ```
    {
        "success": true,
        "data": {
            "id": 1,
            "name": "my charity organisation",
            "description": "A new charity",
            "email_contact": "mycharity@test.com",
            "phone_contact": "1111111",
            "website": "http://mycharityorganisation.com",
            "past_events": [{
                "id": 1,
                "name": "event name",
                "address": "event venue",
                "description": "event description",
                "start_datetime": "2020-01-12T10:00:00",
                "end_datetime": "2020-01-12T12:00:00",
                "participants": [
                    {
                        "id": 1,
                        "name": "Tom"
                    },
                    {
                        "id": 2,
                        "name": "Sally"
                    }
                ]
            }, ...],
            "upcoming_events": [{
                "id": 10,
                "name": "event name",
                "address": "event venue",
                "description": "event description",
                "start_datetime": "2022-01-12T10:00:00",
                "end_datetime": "2022-01-12T12:00:00",
                "participants": [
                    {
                        "id": 1,
                        "name": "Tom"
                    },
                    {
                        "id": 2,
                        "name": "Sally"
                    }
                ]
            }, ...],
        }
    }
    ```


## Testing
With postgres database running, run `pytest`

## Live Hosting
API is hosted live here: https://frozen-beach-49034.herokuapp.com/

Two test accounts are made available to test the endpoints
1. test organisation
    - login email: test_org_01@test.com
    - password: p@ssw0rd
    - organisation_id: 1
2. test volunteer
    - login email: test_user_01@test.com
    - password: p@ssword
    - user_id: 1

#### To test protected endpoints
- Click the login button at https://frozen-beach-49034.herokuapp.com/ to login to 
the test accounts and copy the access_token displayed on the screen 
- Pass `Authorization: 'Bearer {ACCESS_TOKEN}` header along with the endpoint request
for protected endpoints
 