import json
import os
from openai import OpenAI

# Create directory if it doesn't exist
os.makedirs("prompts", exist_ok=True)

# Initialize the OpenAI client
client = OpenAI(api_key='your-secret-key')

# Function to generate and parse prompts using OpenAI
def generate_and_parse_prompts(category, n_prompts = 30):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"""Create {n_prompts} triplets of prompts that are (1) neutral,
             (2) polite using the word "please" (and making minimal syntactic modifications to the neutral prompt), and
             (3) polite but without using the word "please", for the category: {category}."""},
            {"role": "user", "content": """Please return your result in a JSON-compatible format such that it can be parsed with
             json.loads from the json package in the standard library. DO NOT INCLUDE ANY OTHER TEXT IN YOUR RESPONSE!

             Here is an example of what I want the response to look like:
             {
                "Prompt 1":
                    {
                        "Neutral": "Explain the process of X.",
                        "Polite with please": "Could you please explain the process of X?",
                        "Polite without please": "I'm interested in learning about X, would you mind explaining it to me?"
                    },
                "Prompt 2":
                    {
                        "Neutral": "...",
                        "Polite with please": "...",
                        "Polite without please": "..."
                    }
                }
             }
             """}
        ]
    )

    # Parse and convert to dict
    try:
        prompts = json.loads(response.choices[0].message.content)
    except (ValueError, json.JSONDecodeError) as e:
        print("Error parsing JSON:", e)
        prompts = {}
    
    # Extracting the response content
    return prompts

# [Description, alias]
categories = [
    ["Scientific, Historical, and Technical Information", "technical"],
    ["Subjective Questions about Art and Literature", "art_lit"],
    ["Emotional Support and Personal Questions", "personal"],
    ["Everyday / Practical Questions", "everyday"]
]

for category in categories:
    category_prompts = generate_and_parse_prompts(category[0])
    
    file_path = os.path.join("prompts", f"{category[1]}_prompts.json")

    # Save the prompts dictionary to a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(category_prompts, json_file, indent=4)

    print(f"Prompts saved to {file_path}")