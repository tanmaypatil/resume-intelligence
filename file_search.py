from openai import OpenAI
from typing import List
import logging
import json
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from pydantic import BaseModel
from pprint import pformat

from readProp import *

key = readProperties("OPENAI_KEY")
client = OpenAI(api_key=key)

def pretty_print_pydantic(obj):
    if isinstance(obj, BaseModel):
        return pformat(obj.dict(), indent=2, width=120)
    elif isinstance(obj, list):
        return pformat([pretty_print_pydantic(item) for item in obj], indent=2, width=120)
    elif isinstance(obj, dict):
        return pformat({k: pretty_print_pydantic(v) for k, v in obj.items()}, indent=2, width=120)
    else:
        return repr(obj)

def add_files(vector_store_name: str, files: List[str]):
    """Create a new vector store and add files to it."""
    try:
        # Create a new vector store
        vector_store = client.beta.vector_stores.create(name=vector_store_name)
        logging.info(f"Created vector store: {vector_store_name}")

        # Upload files and add them to the vector store
        file_ids = []
        for file_path in files:
            with open(file_path, "rb") as file:
                uploaded_file = client.files.create(file=file, purpose="assistants")
                file_ids.append(uploaded_file.id)
        
        # Add files to the vector store
        file_batch = client.beta.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store.id,
            file_ids=file_ids
        )

        logging.info(f"Added {len(file_ids)} files to the vector store.")
        logging.info(f"File batch status: {file_batch.status}")
        logging.debug(f"File counts: {file_batch.file_counts}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", err=True)
        

def list_stores():
    vector_stores = client.beta.vector_stores.list()
    print(vector_stores)
    list=vector_stores
    print(type(vector_stores))
    return list

def search(vector_store_names: List[str], user_input : str):
    """Search inside the openai vector store """
    try:
        # Create an assistant with file search enabled
        assistant = client.beta.assistants.create(
            name="File Chat Assistant",
            instructions="You are a helpful assistant. Use the provided vector stores to answer user questions.",
            model="gpt-4o",
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {
                    "vector_store_ids": vector_store_names
                }
            }
        )

        # Create a thread
        thread = client.beta.threads.create()

        print(f"search started. with prompt {user_input}")
          
            # Add the user's message to the thread
        client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_input
        )

        # Create a run
        run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id
        )

        # Wait for the run to complete
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            # Retrieve and display the assistant's response
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                if message.role == "assistant":
                    print(f"Assistant: {message.content[0].text.value}")
                    break

            # Retrieve and display the run step details
            run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)
            for step in run_steps.data:
                if step.type == "tool_calls":
                    for tool_call in step.step_details.tool_calls:
                        if tool_call.type == "file_search":
                            run_step = client.beta.threads.runs.steps.retrieve(
                                thread_id=thread.id,
                                run_id=run.id,
                                step_id=step.id,
                                include=["step_details.tool_calls[*].file_search.results[*].content"]
                            )
                            print("\nFile Search Results:")
                            
                            print(pretty_print_pydantic(run_step.step_details.tool_calls[0].file_search.results))

    except Exception as e:
        print(f"An error occurred: {str(e)}")
