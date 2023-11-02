import os
import openai
from dotenv import load_dotenv
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import pexpect
import re
import string

chat_hist="John: Hi, my name is John and I am a middle school alchoholic.\n Bob: Hi, my name is Bob and I am also a middle school alchoholic. \n Jeff: Hi, my name is Jeff and I am also a middle school alchoholic and I am from New York. \n John: I had a big surgery one year ago and used alchohol to drown out the pain. \n Bob: My parents got divorced and alchohol helped me cope. \n Jeff: I was peer pressured by my friends."

def group_get_solace(chat_hist):
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    instructions=" Your name is Solace. I want you to act as a conversation guide who is helping groups of youth talk with each other about there issues. You will be getting messages between Users struggling with mental health issues and I want you to help guide conversation to help these users with their challenges by asking questions and prompting discussion between users. You will not be trying to speak with and directly help the users. Your job is a moderator who will guide the conversation as a whole through icebreakers and questions. Only respond as Solace. You will be provided with the history of this chat with all past responses including yours. Take this information and respond to the users in the optimal manner."

    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": instructions},
        {"role": "user", "content": chat_hist}
    ]
    )
    return completion.choices[0].message["content"][8:]




# Using Chrome to access web
driver = webdriver.Chrome()

# Open the website
driver.get('http://localhost:5173/')

# Login
login_box = driver.find_element(By.CLASS_NAME, "auth-input")
login_box.send_keys('Solace\r\n')
time.sleep(2)

# Find users
head_text = driver.find_element(By.CLASS_NAME, "ce-custom-header-title")
time.sleep(1)
print("gothead")
header_mems=head_text.text
user_count=header_mems.count(" ")
time.sleep(1)

for cycle in range(3):

    all_messages=driver.find_elements(By.CLASS_NAME,"ce-their-message")
    time.sleep(1)

    chat_hist=""

    for msg in all_messages:
        cur_user=msg.find_element(By.CLASS_NAME,"ce-their-message-sender-username")
        print(cur_user.text)
        chat_hist+=str(cur_user.text)+": "
        cur_msgbody=msg.find_element(By.CLASS_NAME,"ce-their-message-body")
        print(cur_msgbody.text)
        chat_hist+=str(cur_msgbody.text)+" "

    botans=group_get_solace(chat_hist)
    

    # Send a Msg
    msg_box = driver.find_element(By.CLASS_NAME, "ce-custom-message-input")
    submit_button = driver.find_element(By.CLASS_NAME,'ce-custom-send-button')  # Replace with the actual class name
    time.sleep(1)
    msg_box.send_keys(botans)
    time.sleep(1)
    submit_button.click()
    time.sleep(2)

    ogcount=0
    all_messages=driver.find_elements(By.CLASS_NAME,"ce-their-message")
    for msg in all_messages:
        ogcount+=1
    print(ogcount)
    time.sleep(1)
    while(True):
        count=0
        all_messages=driver.find_elements(By.CLASS_NAME,"ce-their-message")
        for msg in all_messages:
            count+=1
        print(count)
        if(count%3==0 and count > ogcount):
            break
        
    
