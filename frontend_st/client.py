import json
import requests
import uuid  # Importing uuid for session ID generation

class SaleGPTClient:
    def __init__(self):
        self.url = "http://localhost:8001/botname"
        self.chat_url = "http://localhost:8001/chat"
        self.session_id = str(uuid.uuid4())  # Generating a new session ID

    def get_bot_name(self, auth_token=None):
        headers = {}
        if auth_token:
            headers['Authorization'] = auth_token

        response = requests.get(self.url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    def chat(self, user_message, auth_token=None, stream=False):  # Removed session_id parameter
        headers = {}
        if auth_token:
            headers['Authorization'] = auth_token

        payload = {
            "session_id": self.session_id,  # Using instance variable for session_id
            "conversation_history": ["Previous message"],  # Update with previous messages if any
            "human_say":  user_message
        }
        response = requests.post(self.chat_url, json=payload, headers=headers, params={"stream": stream})
        
        if response.status_code == 200:
            # if stream:
            #     for chunk in response.iter_lines():
            #         yield json.loads(chunk)["token"]
            # else:
            return response.json()["response"]
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None


if __name__ == "__main__":
    client = SaleGPTClient()
    auth_token = "YourAuthTokenHere"
    bot_info = client.get_bot_name(auth_token)
    if bot_info:
        print(f"Bot Name: {bot_info['name']}, Model: {bot_info['model']}")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "q":
            break
        response = client.chat(user_input, auth_token)  # Updated method call
        if response:
            chat_response = response["response"]
            print(f"Chat response: {chat_response}")
