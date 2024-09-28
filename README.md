# resume-search-intelligence
Resume search natural queries .  I use openai RAG vector store to index and store resume.

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