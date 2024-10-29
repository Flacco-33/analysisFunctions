import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

model_name = "gpt-4o-mini"

token = os.getenv('OPENAI_API_KEY')
endpoint = os.getenv('ENDPOINT')

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def analyze_data(data, prompt:str):
    
    string_data = json.dumps(data)
    # print(string_data)
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content":prompt,
            },
            {
                "role": "user",
                "content": string_data,
            },
        ],
        temperature=0,
        top_p=1.0,
        max_tokens=1000,
        model=model_name
    )
    
    output = response.choices[0].message.content;

    # print(output)

    return output