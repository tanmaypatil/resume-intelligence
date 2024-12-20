import os
from dotenv import load_dotenv
import traceback
from pprint import pformat
from pydantic import BaseModel
from openai import OpenAI
from typing import List
import logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
key = os.getenv("OPENAI_KEY")
client = OpenAI(api_key=key)


def pretty_print_pydantic(obj):
    if isinstance(obj, BaseModel):
        logging.info(f" name : {obj.__class__.__name__}")
        logging.info(f"pydantic object instance {obj.model_fields.keys()}")
        return pformat(obj.model_dump(), indent=2, width=120)
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
        logging.info(
            f"Created vector store: {vector_store_name}  id :{vector_store.id}")

        # Upload files and add them to the vector store
        file_ids = []
        for file_path in files:
            with open(file_path, "rb") as file:
                uploaded_file = client.files.create(
                    file=file, purpose="assistants")
                file_ids.append(uploaded_file.id)

        # Add files to the vector store
        file_batch = client.beta.vector_stores.file_batches.create_and_poll(
            vector_store_id=vector_store.id,
            file_ids=file_ids
        )

        logging.info(f"Added {len(file_ids)} files to the vector store.")
        logging.info(f"File batch status: {file_batch.status}")
        logging.debug(f"File counts: {file_batch.file_counts}")
        return vector_store.id
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}", err=True)
        return None


def list_stores():
    vector_stores = client.beta.vector_stores.list()
    print(vector_stores)
    list = vector_stores
    print(type(vector_stores))
    return list


def search(vector_store_names: List[str], user_input: str, instructions: str):
    """Search inside the openai vector store """
    assistant_output = []
    annotations = []
    # Set ranking options, including a score threshold (hypothetical)
    logging.info(f"vector search search prompt is {user_input}")
    logging.info(f"vector search , store names is {vector_store_names}")
    try:
        # Create an assistant with file search enabled
        assistant = client.beta.assistants.create(
            name="File Chat Assistant",
            instructions=instructions,
            model="gpt-4o",
            tools=[{"type": "file_search", "file_search": {
                "max_num_results": 3, "ranking_options": {"score_threshold": 0.5}}}],
            tool_resources={
                "file_search": {
                    "vector_store_ids": vector_store_names,
                }
            }
        )
        # Create a thread
        thread = client.beta.threads.create()
        logging.info(f"search started. with prompt {user_input}")
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
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id)

            # Retrieve and display the assistant's response
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                if message.role == "assistant":
                    if len(message.content) > 0:
                        print(f"Assistant: {message.content[0].text.value}")
                        assistant_output.append(message.content[0].text.value)
                        print(f"Assistant annotation : {message.content[0].text.annotations}")
                        annotations.extend(message.content[0].text.annotations)
                        break

            # Retrieve and display the run step details
            run_steps = client.beta.threads.runs.steps.list(
                thread_id=thread.id, run_id=run.id)
            for step in run_steps.data:
                if step.type == "tool_calls":
                    for tool_call in step.step_details.tool_calls:
                        if tool_call.type == "file_search":
                            run_step = client.beta.threads.runs.steps.retrieve(
                                thread_id=thread.id,
                                run_id=run.id,
                                step_id=step.id,
                                include=[
                                    "step_details.tool_calls[*].file_search.results[*].content"]
                            )
                            logging.info("\nFile Search Results:")
                            logging.info(pretty_print_pydantic(
                                run_step.step_details.tool_calls[0].file_search.results))
                            # Print field names (keys) using .model_fields.keys()
                            # logging.info(f"\nModel Fields (Keys): {run_step.step_details.tool_calls[0].file_search.results[0].model_fields.keys()}")
                            if (run_step.step_details.tool_calls[0].file_search.results
                                and run_step.step_details.tool_calls[0].file_search.results[0].content
                                    and len(run_step.step_details.tool_calls[0].file_search.results[0].content) > 0):
                                found_text = run_step.step_details.tool_calls[0].file_search.results[0].content[0].text
                                logging.info(
                                    f"Chunk 30 characters {found_text[0:30]}")

        logging.info(f"output is {assistant_output}")
        return (assistant_output,annotations,found_text)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()  # Prints the full traceback

def search_v2(vector_store_names: List[str], user_input: str, instructions: str,assistant_message:str )-> tuple[list,list,str,object,object]:
    assistant,thread = create_assistant(instructions,vector_store_names)
    assistant_output,annotations,found_text = search_with_query(user_input,assistant_message,assistant,thread)
    return (assistant_output,annotations,found_text,assistant,thread)

def search_v2_cont(user_input:str,assistant_message:str,assistant:object,thread:object )->tuple[list[str],list,str,object,object]:
    """ 
      Difference between search_v2 and search_v2_cont is that for search_v2 will construct assistant 
      and search_v2_cont will use the passed assistant object.
    """
    
    assistant_output,annotations,found_text = search_with_query(user_input,assistant_message,assistant,thread)
    return assistant_output,annotations,found_text,assistant,thread


def create_assistant(instructions: str, vector_store_names: list):
    try:
        load_dotenv(override=True)
        model = os.getenv("MODEL")
        # Create an assistant with file search enabled
        logging.info(f"create assistant , vector store {vector_store_names} , model : {model}")
        assistant = client.beta.assistants.create(
            name="Resume search Assistant",
            instructions=instructions,
            model=model,
            tools=[{"type": "file_search", "file_search": {
                "max_num_results": 3, "ranking_options": {"score_threshold": 0.5}}}],
            tool_resources={
                "file_search": {
                    "vector_store_ids": vector_store_names,
                }
            }
        )
        # Create a thread
        thread = client.beta.threads.create()
        logging.info(f"Create assistant new thread : {thread.id}")
    except Exception as e:
        print(f"An error occurred while creating asistant: {str(e)}")
        traceback.print_exc()  # Prints the full traceback
    logging.info(f"created assistant : {assistant.id}, thread id :{thread.id}")
    return assistant, thread


def search_with_query(user_input: str, assistant_message: str,  assistant: object,thread: object):
      logging.info(f'search_with_query : {thread.id}')
      try:
        assistant_output = []
        annotations = []
        found_text = None
        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        # Add the assistant message to the thread
        if assistant_message:
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="assistant",
                content=assistant_message
            )

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Wait for the run to complete
        while run.status != "completed":
          run = client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id)
          logging.info(f"run id : {run.id} , run status : {run.status}")
        # Retrieve and display the assistant's response
          messages = client.beta.threads.messages.list(thread_id=thread.id)
          for message in messages.data:
            if message.role == "assistant":
              if len(message.content) > 0:
                logging.info(f"Assistant reply: {message.content[0].text.value}")
                assistant_output.append(message.content[0].text.value)
                print(f"Assistant annotation : {message.content[0].text.annotations}")
                annotations.extend(message.content[0].text.annotations)
                break
          # Retrieve and display the run step details
          run_steps = client.beta.threads.runs.steps.list(
                thread_id=thread.id, run_id=run.id)
          for step in run_steps.data:
            if step.type == "tool_calls":
              for tool_call in step.step_details.tool_calls:
                if tool_call.type == "file_search":
                  logging.info(f"file search was invoked")
                  run_step = client.beta.threads.runs.steps.retrieve(
                                thread_id=thread.id,
                                run_id=run.id,
                                step_id=step.id,
                                include=[
                                    "step_details.tool_calls[*].file_search.results[*].content"]
                            )
                  # storing the chunk
                  if (run_step.step_details.tool_calls[0].file_search.results
                      and run_step.step_details.tool_calls[0].file_search.results[0].content
                      and len(run_step.step_details.tool_calls[0].file_search.results[0].content) > 0):
                      found_text = run_step.step_details.tool_calls[0].file_search.results[0].content[0].text
                      logging.info(f"Chunk 50 characters {found_text[0:50]}")

        logging.info(f"output is {assistant_output}")
        return assistant_output,annotations,found_text
      except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()  # Prints the full traceback
        return None,None,None
