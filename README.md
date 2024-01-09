# OpenAI-Reverse-Proxy
A Very Basic OpenAI Reverse Proxy to get your API Service Started + A Discord Bot for Key/Usage Management.

Note: This Will Only Work on Replit as it uses Replit DataBase

This Project on API was done by  [@SamirXR](https://www.instagram.com/samir.xr/) and [@Herumes](https://github.com/herumes) So give us Proper Credit as we Worked our ASS Off for This!

Join [Discord Server](https://discord.gg/P9gGZaXWGR) for any Assist/Issues or Testing it!

If You like My OpenSource Work you can Support : https://www.buymeacoffee.com/samir.xr


# PreRequisites

- A Replit Account : [Click here](https://replit.com/~)
- A Discord Token  : [Click here](https://discord.com/developers/applications/)
- An OpenAI Key          : [Click here](https://platform.openai.com/api-keys/)


# Features

| Feature                  | Description                             |
|--------------------------|-----------------------------------------|
| Stream/Non Stream                | Supports Streaming/Non-Streaming Response|
| Discord Bot             | Bot With Key Generation/Regeneration & Usage Information|
| Multiple Users                   | Can Handle Multiple Rqeuests Altogether |
| Master Key              | A Master Key Only For the Developer |
| Credit System          | A Credit System that Can be Customized |
| OpenAI Library        | Supports the Latest OpenAI Library |

# Installation 

1. Clone the Repository.

```pyton
git clone https://github.com/SamirXR/OpenAI-Reverse-Proxy
```

2. Change Directory.
   
```pyton
cd OpenAI-Reverse-Proxy
```

3. Make Your Secret Token/APIs on Replit's Secret.
   
```python
 DISCORD_TOKEN
 OPEN_AI_KEY
 MASTER_KEY
```

4. Install the Requirements

```python
pip install -r requirements.txt
```

5. Then run the API
```python
python main.py
```

Congratulations! Your API is Up and Running!


## Usage

Replace the Base_url with your Replit URL and Use Your API Key Generated From Discord Bot/Developer Master Key.


```python
pip install openai==1.7.0
```

```python

from openai import OpenAI

client = OpenAI(api_key="/generate-key", base_url="Your replit.dev URL Here")

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
)

print(completion.choices[0].message.content)
```









