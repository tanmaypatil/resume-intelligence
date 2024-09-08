
from completion import generate_completion

def test_completion():
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is a LLM?"}
  ]
  completion = generate_completion(messages)
  print("Generated Completion:")
  print(completion)