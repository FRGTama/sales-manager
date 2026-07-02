# AI_USAGE.md

## 1. AI tools used

I used Opencode as TUI coding assistant, ChatGPT for more general questions.
I Used Opencode mostly to generate repetitive code and boilerplates. After generating, i review and make changes.
I Also used Opencode to generated README.md

## 2. What AI helped with

Opencode helped generated the source code and classes where i have defined the attributes.

## 3. Effective prompts used

Prompt 1:

```text
CONTEXT: You are a coder generating code for a bigger project, your job is to do a small part in the code, following strictly the rules given, do not deviate, if you are unsure, ask the user for further instructions, do not make up answers.
GOAL:
In backend/app/schemas.py generate pydantic classes for the database schemas with the following definitions:
Sale: id, name (str), phone (str(10)), email (str), status (str, one of active/inactive/lead), created_at
Agency: id, name (str), address (str), area (str), sale_id (FK), created_at
TrackRecord: id, customer_name (str), expected_revenue (float), status (str: new/contacted/won/lost), notes (str|None), agency_id (FK), created_at
Relations:
1 Sale, N Agency.
1 Agency, N TrackRecords.
Cascade = True.
Constraints:
Sale.phone: MUST start with 0 and follows by 9 other digits.
Agency.area: MUST be one of Vietnam's 34 provinces (search online: Vietnam new province to get data)
In backend/app/repositories.py generate class for each entity with naming convention name+Repository, eg: SaleReposity. For Sale, Agency methods are:
1. lists_all(): use select to list all.
2. get_by_id(): use select + where a = b to get the object with id.
FORMAT:
Implement with clean code architecture, SOLID foundation.
```

Why it helped:

This generated the repetitive coding for schemas and repositories for the database, i just need to define the structure in text form and validate the AI's output.

Prompt 2:

```text
Based on the overview of the project, generate testcases for edgecases in backend/tests using pytest
```

Why it helped:

This helped me generated edgecases to use in CICD

## 4. AI mistakes and debugging

AI was helpful, but it still required manual control and debugging.

Some issues I had to catch or correct:
1. When generating the testcases, it missed some edge cases like Sale.phone not starting with 0
2. When generating the entity's schema, it constraint for Sale.phone by iterating a loop and i used regex matching to simplify
3. When generating schemas.py, it used abstract classes for each of the class then implement each concrete class, which is useless and redundant, so i deleted the abstract class and reformat to just use concrete classes. I think this is caused by me telling the AI to follow SOLID foundations.

## 5. Notes on AI usage

I used AI as a support tool for repetitive coding and review, not as the decision-maker for the project.

The important implementation decisions were made by me:

- I defined the entity relationships and the main workflow.
- I chose the backend layer structure.
- I decided which features were in scope and which were not.
- I reviewed generated code for correctness and consistency.
- I verified that the final project still matched the original assignment.

If I had more time, I would use AI in the same way: mostly for generating repetitive tests, checking edge cases, and improving documentation after the main technical decisions are already clear.
