import json
import os
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key='your-secret-key')

# Directory setup
prompt_dir = "prompts"
response_dir = "responses"
os.makedirs(response_dir, exist_ok=True)

# Filenames for different categories
categories = ["art_lit", "everyday", "personal", "technical"]

# Function to load prompts for a given category
def load_prompts(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Function to save responses for a given category
def save_responses(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


# Generate and save responses for each category
for category in categories:
    prompt_file = os.path.join(prompt_dir, f"{category}_prompts.json")
    response_file = os.path.join(response_dir, f"{category}_responses.json")
    
    # Load prompts
    prompts = load_prompts(prompt_file)
    
    # Generate responses
    prompt_responses = {}
    for id, prompt_triplet in prompts.items():
        prompt_tone_responses = {}
        for tone, prompt in prompt_triplet.items():
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt}
                ],
                # We use a temperature of 0 to minimize noise, so that any differences in response
                # are directly attributable to differences in the prompts.
                temperature=0
            )
            prompt_tone_responses[tone] = response.choices[0].message.content.strip()  # Strip to remove any extra whitespace
        prompt_responses[id] = prompt_tone_responses
    
    # Save responses
    save_responses(response_file, prompt_responses)
    print(f"Responses for {category} saved to {response_file}")