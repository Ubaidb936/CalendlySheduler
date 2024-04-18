# Function calling coding challenge

## Overview

Your task is to create an interactive chatbot using OpenAI's function calling capabilities. 
This chatbot will allow users to interact with their Calendly account directly through the chat interface. 
The chatbot should be able to list scheduled events and cancel events using the Calendly API.

## Requirements

Build a simple chatbot that can interact with the REST API. The chatbot may be a web server, and the user may interact 
with it through REST API. It will be a bonus if you can make the chatbot interactive through a web interface. 

Use OpenAI's function calling feature to integrate external APIs with your chatbot. 
This will involve crafting requests to the Calendly API and processing responses within the chatbot's logic.
Specifically, you'll need to implement the following functionality:

 - Once the user says something like "show me the scheduled events", retrieve a list of the user's scheduled events from Calendly.
 - When the user says something like "cancel my event at 3pm today", find the event and cancel it from Calendly.

### Language

Please use Python for this code challenge.

## References

### OpenAI Function Calling Reference

Below are some resources to help you get started:

- [OpenAI Function Calling Documentation](https://platform.openai.com/docs/guides/function-calling)
- You may use Langchain to make the development of the chatbot easier. 
  - [Langchain function calling](https://python.langchain.com/docs/modules/model_io/chat/function_calling)

For this code challenge, we provide you with a test API key to use with OpenAI's function calling feature.
Please don't use this key for any other purpose.

```
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
```

### Calendly API Reference

First, you'll need to create a Calendly account and obtain an API key. Follow the instructions in the 
[authentication document](https://developer.calendly.com/how-to-authenticate-with-personal-access-tokens) to get started.

Second, here is the documentation for the [Calendly API](https://developer.calendly.com/api-docs/):

- List Scheduled Events: Use the `/scheduled_events` endpoint to list the user's scheduled events. 
  [API Documentation](https://developer.calendly.com/api-docs/2d5ed9bbd2952-list-events)

- Cancel an Event: Use the `/scheduled_events/{event_uuid}/cancel` endpoint to cancel an event. 
  [API Documentation](https://developer.calendly.com/api-docs/afb2e9fe3a0a0-cancel-event)


### How to run the project

1. clone the repository: `https://github.com/Ubaidb936/CalendlySheduler.git`
2. Cd into CalendlySheduler:  `cd CalendlySheduler`
3. create a new virtual env using this command `python3 -m venv venv` for linux/mac and `python -m venv venv` for windows.
4. to activate the venv run source `source venv/bin/activate` for macOS
5. run `pip install -r requirements.txt` to install dependencies...
6. Settup the Variables in the config.py file
7.  run `uvicorn main:app --reload ` to run FASTAPI Application. if there is error `any module not found` Please the command in new terminal
8.  Go to `localhost:8000/chat?user_input= list all my events?` to test the application

### Thanks!!!!




  
