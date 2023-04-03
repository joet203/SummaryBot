import json
import requests

#input from previous Zapier retrieval of Slack messages via API
data = json.loads(input_data['x'])

messages = data['messages']
slack_chatlog = ""
for message in reversed(messages):
    if 'user' not in message:
        continue
    user = message.get('user', '')
    text = message.get('text', '')
    slack_chatlog += f"{user}: {text}\n"

id_to_name_map = {
    'U4KKGKX3M': 'Bigs',
    'U4K5S5YF2': 'GD',
    'U4K4JA37T': 'zedge',
    'U4KU6G6NR': 'dylan',
    'U4KNLUVQU': '7',
    'U4KMFRU3C': 'Dredd',
    'U4LCKUQTG': 'TBTB12',
    'U4KNM49D2': 'Riverboat Doug',
}

for id, name in id_to_name_map.items():
    slack_chatlog = slack_chatlog.replace(id, name)

output[1] = slack_chatlog
# Set your API key
api_key = "INSERT_API_KEY_HERE"

# Define the API endpoint and headers
url = "https://api.openai.com/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Define the API request payload
payload = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "summarize this groupchat log, distill it into key bullet points including names and any important links: " + slack_chatlog  }],
    "temperature": .8,
    "max_tokens": 200,
    "n": 1,
    "stop": None,
}

# Send the API request and receive the response
response = requests.post(url, headers=headers, data=json.dumps(payload))
response_json = response.json()

# Extract and print the summary from the API response
summary = response_json["choices"][0]["message"]["content"].strip()

output[0] = (summary)
