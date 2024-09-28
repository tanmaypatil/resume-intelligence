# resume-search-intelligence
Resume search using natural queries .  Demo application using openai RAG api and opensource VLM model to do resume analysis.

## Objective 
Objective of resume intelligence would be to support natural language query on a set of resumes .
It can be used to do comparative analysis of resumes .
Let us say , that we have 4 or 5 resumes of prospective software engineers
Some of the query , which it should allow you to fire are 
1. Does any of the candidates have team management experience ? 
2. Who has more experience in java and docker in set of resumes ?

## Approaches
Here i use RAG approaches 
1. RAG - with openai
   openai has assistant api , which has option of storing the vector representation of document and searching against the same .
   Refer here for documentation [File Search](https://platform.openai.com/docs/assistants/tools/file-search)
2. RAG - with opensource colpali
   This is approach of using VLM . I plan to use Byaldi which internally uses colpali
   Refer to notebook , which has sample code [chat with pdf using byaldi
   ](https://github.com/AnswerDotAI/byaldi/blob/main/examples/chat_with_your_pdf.ipynb)

## Using openai file search 
This is a straightforward approach .I use openai apis to create a vector store and add all pdf documents to vector store . post that create a assistant and attach vector store to assistant 

Refer to this code in file_search api : 
```
    def search(vector_store_names: List[str], user_input : str):
    assistant_output = []
    """Search inside the openai vector store """
    # Set ranking options, including a score threshold (hypothetical)
    logging.info(f"vector search search prompt is {user_input}")
    logging.info(f"vector search , store names is {vector_store_names}")
    try:
        instructions = """
          You are an assistant specializing in scanning and analyzing technology resumes. Your goal is to identify key technical skills, experience, and alignment with job descriptions.
          1. **Technical Skills**: Focus on relevant programming languages, frameworks, tools, and certifications (e.g., Python, Java, AWS, Docker). Highlight these clearly.
          2. **Job Match**: Compare the resume with provided job descriptions. Focus on matching key technologies and job experience, and note areas where the candidate doesn’t meet the requirements.
          3. **Projects & Experience**: Prioritize large-scale projects or leadership roles in tech teams. Identify open-source contributions or significant technical achievements.
          """

        # Create an assistant with file search enabled
        assistant = client.beta.assistants.create(
            name="File Chat Assistant",
            instructions= instructions,
            model="gpt-4o",
            tools=[{"type": "file_search", "file_search": { "max_num_results" : 3 ,"ranking_options" : { "score_threshold": 0. }}}],
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
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            # Retrieve and display the assistant's response
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages.data:
                if message.role == "assistant":
                    if len(message.content) > 0 :
                      print(f"Assistant: {message.content[0].text.value}")
                      assistant_output.append(message.content[0].text.value)
                      break

            # Retrieve and display the run step details
            run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)
            for step in run_steps.data:
                if step.type == "tool_calls":
                    for tool_call in step.step_details.tool_calls:
                        if tool_call.type == "file_search":
                            run_step = client.beta.threads.runs.steps.retrieve (
                                thread_id=thread.id,
                                run_id=run.id,
                                step_id=step.id,
                                include=["step_details.tool_calls[*].file_search.results[*].content"]
                            )
                            logging.info("\nFile Search Results:")
                            logging.info(pretty_print_pydantic(run_step.step_details.tool_calls[0].file_search.results))
                            # Print field names (keys) using .model_fields.keys()
                            #logging.info(f"\nModel Fields (Keys): {run_step.step_details.tool_calls[0].file_search.results[0].model_fields.keys()}")
                            if (run_step.step_details.tool_calls[0].file_search.results 
                              and run_step.step_details.tool_calls[0].file_search.results[0].content
                              and len(run_step.step_details.tool_calls[0].file_search.results[0].content) > 0 ):
                              text = run_step.step_details.tool_calls[0].file_search.results[0].content[0].text
                              logging.info(f"Chunk 30 characters {text[0:30]}")

        logging.info(f"output is {assistant_output}")
        return assistant_output
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()  # Prints the full traceback
```

