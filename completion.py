from openai import OpenAI
from readProp import *

key = readProperties("OPENAI_KEY")
client = OpenAI(api_key=key)


def generate_completion(messages, model="gpt-4o-mini", max_tokens=150):
    print('generate_completion')
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            n=1,  # Number of completions to generate
            stop=None,  # Optionally specify stop sequences
            temperature=0.7  # Controls the randomness of the output
        )
        # Extract the completion text
        completion_text = response.choices[0].message
        return completion_text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None