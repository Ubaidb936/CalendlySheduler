import requests

from config import OPENAI_API_KEY, CALENDLY_API_KEY, CALENDLY_USER_ID


if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY is None. Please set the  it in config.py.")
if CALENDLY_API_KEY is None:
    raise ValueError("CALENDLY_API_KEY is None. Please set the  it in config.py.")
if CALENDLY_USER_ID is None:
    raise ValueError("CALENDLY_USER_ID is None. Please set the  it in config.py.")


    
## Gets all the events
def get_events():
    
    # URL for get all events
    API_URL = 'https://api.calendly.com/scheduled_events'
    
    # Headers containing the API key for authentication
    headers = {
    'method':'GET',
        'Authorization': f'Bearer {CALENDLY_API_KEY}',
        'Content-Type': 'application/json'
    }
    
    # Parameters to pass in the request
    params = {
        'user': CALENDLY_USER_ID
    }
    
    response = requests.get(API_URL, headers=headers, params=params)

    # Checking if the request was successful (status code 200)
    if response.status_code == 200:
        # Parsing the JSON response
        data = response.json()
        # Do something with the data, such as print or process it further
        events = data["collection"]
        
        eventList = []
        
        for event in events:
            if event["status"] != 'canceled':
                eventList.append(event)
        return eventList        
    else:
        # Print an error message if the request was not successful
        print(f"Failed to fetch scheduled events. Status code: {response.status_code}")
        return "Failed to call the API, Try again......"
        

def get_uuid(startTime):
    uuid = None
    events = get_events()
    for event in events:
        if event["start_time"] == startTime:
            uri = event["uri"]
            segments = uri.split("/")
            uuid = segments[-1]
        return uuid
    return uuid

        
## Deletes an event
def delete_event(startTime):
    
    uuid = get_uuid(startTime)
    
    if uuid == None:
        return "No event to delete at the mentioned time."
    
    API_URL = f'https://api.calendly.com/scheduled_events/{uuid}/cancellation'

    headers = {
        'Content-Type': "application/json",
        'Authorization': f"Bearer {CALENDLY_API_KEY}"
        }

    response = requests.post(API_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        # Print an error message if the request was not successful
        print(f"Failed to fetch find the events. Status code: {response.status_code}")
        return "Event does not exist"
