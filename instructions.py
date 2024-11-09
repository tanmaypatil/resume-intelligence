import os
import json
from dotenv import load_dotenv
import logging
def get_instructions():
    load_dotenv()
    instruction_id = os.getenv("instruction_id")
    with open('.\\system_config\\instructions.json') as file:
        inst_arr = json.load(file)
    instructions = [item for item in inst_arr if item["instruction_id"] == instruction_id]
    assert len(instructions) == 1
    inst_file_id = instructions[0]['instruction']
    with open('.\\system_config\\' + inst_file_id) as file:
        instruction_text = file.read()
    return instruction_text,inst_file_id
    