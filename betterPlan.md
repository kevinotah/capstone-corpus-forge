# Project breakdown
Essentially, it is just a NotebookLM copy

## Layer 1
    - A website that enables users to:
        - Upload documents
        - Organize documents
        - Do interactive actions with them (browsing, removing, etc...)
    - Then, the user can pick what documents that the AI can use for the features.
    - Said features include:
        - Chat with AI about the documents
        - Flashcard creation
        - Create quiz with AI
    - If it is a code file, said features turn into analyzing the code and creating a review for the code.
    - Users are able to influence the tone of AI and its behavior through customized prompts and parameters.
    - Every time the application runs, the documents, metadata and more must stay alive and not deleted, and is only removed if the user said so.
    - App must also expose AI usage information. At minimum, show number of requests and tokens.


## Layer 2
    - Pick 1 of the 4 extra challenges to implement:
        - Instead of dumping the whole documents into AI, we use 2 different ways to find relevant information from the documents, and dump into AI later (This is NOT related from the feature where user selects documents, its the program selectively collect information from the selected document and pass it to AI, instead of putting the whole documents, which intensifies the tokens and stuff)
        - Prompt engineering: Iteratively improve prompts for a specific task.
        - Make visuals from the doccuments that the user uploads. User must be able to interact from it
        - Write tests for the app, and try breaking it. Make sure the system handles the errors gracefully. For example, what would happen if the file is empty or corrupted.

## Specifications
    - A web application, so it must have both frontend and backend, so it is not limited to just python lmao
    - Recommendations for backend: java, php, python or even fastapi for backend. Fastapi is most recommended?
    - We can use RAG - NoRAG from Lab15 to build around it.

# Planning
We will use Flask for backend. Jinja2 for templating and SQLite for database. File storage can be done inside the disk 
## Stage 1:
First we might want to implement file uploading, removing and selecting to pass on AI. No AI features just yet. We also HAVE to make sure that the file STAYS even if we refresh the page.