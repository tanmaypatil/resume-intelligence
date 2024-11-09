import os
from dotenv import load_dotenv
def set_instructions():
    load_dotenv()
    instruction_id = os.getenv("instruction_id")
