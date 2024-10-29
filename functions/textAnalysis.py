import os
from openai import OpenAI
import json
from dotenv import load_dotenv

load_dotenv()

model_name = "gpt-4o-mini"

token = os.getenv('OPENAI_API_KEY')
endpoint = os.getenv('ENDPOINT')

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def analyze_comment(comment):
    response = client.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": "You are a sentiment and emotion analyzer of comments that are expressed by students referring to their teachers, from each sentence I need to obtain its meaning, it is spoken negatively, neutrally or positively, in the same way I require that you give me the emotions that are detected in the sentence based on these emotions (happy, sad, Anger, Surprise, Neutral, Disgust, Fear, contempt), when detecting the emotions I want you to assign a total percentage to each emotion that you detect and I want the sum of the emotions to be 1, I want you to return the result in raw type JSON format. Do not include any markdown, escape characters, or special formatting (e.g., no \n or \t).",
            },
            {
                "role": "user",
                "content": comment,
            },
        ],
        temperature=0,
        top_p=1.0,
        max_tokens=1000,
        model=model_name
    )
    
    output = response.choices[0].message.content;
    json_data = json.loads(output)  
    compact_json = json.dumps(json_data, separators=(',', ':'))

    print(compact_json)

    return compact_json

