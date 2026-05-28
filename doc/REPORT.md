# Project Report

#### The Team members

* Names, epita email addresses, and GitHub usernames of all team members.
    - Vo Anh Duc: anh-duc.vo@epita.fr - voanhduc0105
    - Cindy Gangne Fotsing: cindy.gangne-fotsing@epita.fr -  cindy-fotsing
    - Ogbusuo Kevin Otah: kevin.ogbusuo@epita.fr - kevinotah

---

#### Initial Design

* initial architecture
    - Initially, we decided to go for a NotebookLM copy. However, after some more discussion, we realized that implementing such would take a long time and would not fit the time window, so we ended up with implementing enough features and minimum css. If more time we given then the looks and features would be more polished
* assumptions
    - We initially assumed the project to be very confusing, very difficult to implement since we have to "build an entire notebookLM copy from scratch". However, after being given answers from our questions, we were able to somehow navigate through the project
* technical choices
    - We decided to go for Flask of all things because it is fast and lightweight and versatile for a small project, and we also used Jinja2 for templating. File storage can be done inside the disk 
    - We also decided to use the alrready provided Rag - NoRag from lab 15 for easier implementation. Of course, modified and tailored to our needs.

---

#### Engineering Decisions

For each major decision:

* what alternatives were considered?
    
* why was this solution chosen?

- Technical choice: We also considered using FastAPI for backend, however, we soon switch to Flask since we had previous experience with that, so it might be faster to implement
- Model decision: We considered using NVDIA over Gemini for the model. However, we ended up using Gemini since it is somewhat faster and easier to get the API key.

---

#### Who Did What?

* Document how the project was originally divided among each team member.
* Document how responsibilities possibly evolved over time.

- Originally, we try to split our work with a checklist for more efficiency, and with clear roles. However, that quickly become chaotic as the checklist had too many works to do, and is too spread out. So we instead focus on what each person is good at, and do so. And so we got Kevin and Cindy to implement the non AI features and the backbones, and Duc to implement the AI features.

---

#### AI Collaboration

Document how AI tools were used.

* What tools were used for what purposes?
* How did AI influence design and implementation decisions?
* How did AI impact your learning and development process?
* How did you evaluate AI-generated suggestions?
* How did you detect and handle AI errors or limitations?

We mainly use Github Copilot for this, and some other external AI tools. Because the project was very complex, and we were given a small time window, we have to use AI smartly to aid us to implement, ie, explaination and implementing skeleton and barebones stuff for us to implement smoothly and easily. We also asked AI for clarification on whether something is well implemented, as well as bug checking. It definitely helps us understand a bit better on this subject, and speeds up the development process by a margin. We also try our best to read everything that the AI sent us, and fix whatever it did wrong. Whenever it starts to freak out and loop over and over again, we have to stop it mid way and ask it to redo it, with some reprompting / model change

---

#### Failures and Iterations

Document:

* what failed?
* what surprised you?
* what required redesign?

PDF files initially returned garbage to the AI because the retriever was reading raw bytes instead of extracting text. The app appeared to work but the AI responses were nonsensical — Gemini said it "cannot summarise encoded content", so we used a library - pypdf - to help us with this. We also observed how document content affects AI output quality. A test paper uploaded as a document completely broke the quiz generator because Gemini got confused between generating new questions and copying existing ones.
---

#### “When AI Failed or Was Wrong”

Document cases where AI-generated advice, code, or explanations were:

* incomplete
* misleading
* incorrect
* inefficient

The AI suggested a ChromaDB filter syntax that looked correct and matched the docs, but broke at runtime depending on the version installed. We were able to fix it by filtering results manually in Python instead.
The AI also did not tell Gemini to return pure JSON in the prompts, making Gemini to keep wrapping responses in markdown code fences which broke JSON.parse() on the frontend. We later fix it by implementing a replace strip.


---

#### Lessons Learned

Reflect on:

* technical growth
* workflow improvements
* Strengths and limitations of AI-assisted development

Technical growth: we learnt how RAG, flask and a lot of things work together. We also learnt how to use AI more effectively and to use it as a helper and not a shortcut

Workflow improvements: Always run tests, because who knows they might be able to help us spot bugs before going too far down the line. In our example, we ran tests with realistic documents early. Using a test paper actually helps us identify the problem quickly

Pros of AI assisted development: Helps us understand better on our AI code and implement things faster, especially when we don't have a deep enough foundation on these matters

Cons: The code may look correct but it may not be tested properly, and several bugs may exist. Also, one should not overuse the AI, as doing so might lead to having the AI doing the work for us. We only want to use AI as a tool.

