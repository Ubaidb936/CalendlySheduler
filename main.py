import os
import openai 
from fastapi import FastAPI, Body
from pydantic import BaseModel
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from openai import OpenAI as openAI
from calendly import get_events, delete_event
from datetime import date

from config import OPENAI_API_KEY, CALENDLY_API_KEY, CALENDLY_USER_ID


if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY is None. Please set the  it in config.py.")
if CALENDLY_API_KEY is None:
    raise ValueError("CALENDLY_API_KEY is None. Please set the  it in config.py.")
if CALENDLY_USER_ID is None:
    raise ValueError("CALENDLY_USER_ID is None. Please set the  it in config.py.")



app = FastAPI()

# Load OpenAI LLM with your API key
llm = OpenAI(temperature=1.0, openai_api_key=OPENAI_API_KEY)


client = openAI(api_key=OPENAI_API_KEY) 


def event_checking_intent_agent(user_input):
    
    prompt = """
    ### Task Description:
    Your task is to categorize the input into two categories: 'yes' or 'no'.
    - If the input is about showing events, print 'yes'.
    - If the input is about listing events, print 'yes'.
    - If the input is about canceling an event or meeting, print 'yes'.
    - For all other cases, print 'no'.
    Please ensure the output consists solely of 'yes' or 'no', without any additional text.

    Here is the input:
    Input: {user_input}
    """
    
    prompt = prompt.format(user_input=user_input)
    
    # client = openAI(api_key=OPENAI_API_KEY) 
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    res = response.choices[0].message.content.strip()
    
    print("--------event_checking_intent_agent-------"+res)

    return "yes" in res.lower() 
    
def cancelling_checking_intent_agent(user_input):
    prompt = """
    ### Task Description:
    Your task is to categorize the input into two categories: 'yes' or 'no'.
    - If the input is about showing events, print 'no'.
    - If the input is about listing all scheduled events or meetings, print 'no'.
    - If the input is about canceling an event or meeting, print 'yes'.
    Please ensure the output consists solely of 'yes' or 'no', without any additional text.

    Here is the input:
    Input: {user_input}
    """  
    prompt = prompt.format(user_input=user_input)
    
    # client = openAI(api_key=OPENAI_API_KEY) 
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    res = response.choices[0].message.content.strip()
    
    print("------cancelling_checking_intent_agent---------"+res)
    
    return "yes" in res.lower() 

def checking_time_and_date_agent(user_input):
    """### Task Description:
    Your task is to categorize the input into two categories: 'yes' or 'no'.
    - If the info provioded in the text can be converted into a timestamp, print "yes"
    - If the info provioded in the text cannot be converted into a timestamp, print "no"
    Please ensure the output consists solely of 'yes' or 'no', without any additional text.

    Here is the input:
    Input: {user_input}
    """ 
    prompt = prompt.format(current_date=current_date, user_input=user_input)
    
    # client = openAI(api_key=OPENAI_API_KEY) 
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    res = response.choices[0].message.content.strip()
    
    print("------checking_time_and_date_agent---------"+res)
    
    return "yes" in res.lower() 


def time_stamp_generating_agent(user_input):
    current_date = date.today()
    prompt = """
    Task: convert the date, time mentioned in input text into a timestamp using today as reference.
    
    Instructions:
    - The timestamp should follow the format: YYYY-MM-DDTHH:MM:SS.ffffffZ
    - Ensure that the output consists solely of the timestamp.
    - todays date is {current_date}

    Here is the input text:
    Input: {user_input}
    """ 
    prompt = prompt.format(current_date=current_date, user_input=user_input)
    
    # client = openAI(api_key=OPENAI_API_KEY) 
    
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    
    res = response.choices[0].message.content.strip()
    
    print("------time_stamp_generating_agent---------"+res)
    
    return res
    
    

class UserInput(BaseModel):
    text: str

@app.get("/chat")
async def chat(user_input: str):
    
    isEventIntent = event_checking_intent_agent(user_input)
    
    if isEventIntent:
        isCancellingIntent = cancelling_checking_intent_agent(user_input)
        
        if isCancellingIntent:
            containsTimeAndDate = checking_time_and_date_agent
            if containsTimeAndDate:
                timeStamp = time_stamp_generating_agent(user_input)
                res = delete_event(timeStamp)
                return res
            return "Please event time more specifically"
            
        else:
            return get_events()
        
    response = llm("Tell the user that you are only programmed to list and cancel calendly events.")
    return {"response": response}