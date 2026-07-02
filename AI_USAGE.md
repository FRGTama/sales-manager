# AI_USAGE.md

## 1. AI tools used

I used Opencode as an AI coding assistant during this project.

My main use of AI was to speed up repetitive implementation work after I had already decided the project direction, data model, and code structure. I gave AI specific instructions about the required Sale -> Agency -> Track Record flow, the layer separation I wanted, and the expected behavior for each API/UI feature.

I reviewed and adjusted the generated code before keeping it in the project.

## 2. What AI helped with

AI mainly helped generate repetitive code patterns, such as:

- Pydantic schema classes for create, update, and response payloads.
- FastAPI route handlers following the same CRUD-style pattern.
- Service methods that call repositories and return response schemas.
- Repository methods for common list, create, update, delete, and lookup operations.
- React form and table patterns that repeated across Sales, Agencies, and Track Records.
- Basic test-case drafts for API endpoints and frontend components.
- Documentation wording for setup instructions and AI usage notes.

I handled the main abstraction decisions myself, including:

- Choosing the core hierarchy: Sale -> Agency -> Track Record.
- Deciding to keep the project scoped as a demo instead of a full CRM.
- Separating backend logic into routes, schemas, repositories, services, models, and database setup.
- Deciding which relationships needed parent validation before creating child records.
- Deciding what dashboard statistics were necessary for the assignment.
- Reviewing whether generated code matched the source requirement.

## 3. Effective prompts used

Prompt 1:

```text
I have already decided the data model for this coding test:
Sale has many Agencies, and Agency has many Track Records.

Generate repetitive FastAPI boilerplate for this structure using separate
schemas, routes, services, and repositories. Keep the code simple and suitable
for a demo. Do not add authentication, permissions, or unrelated CRM features.
```

Why it helped:

This prompt kept AI focused on code generation for patterns I had already defined, instead of letting it redesign the project or add unnecessary scope.

Prompt 2:

```text
Given these existing route/service/repository patterns, generate the matching
CRUD-style code for Agencies and Track Records. Keep the same naming style,
validate parent IDs before creating child records, and return clear API errors
when the parent record does not exist.
```

Why it helped:

This prompt was useful for repeating the same structure across multiple entities while preserving the decisions I had already made about validation and layer separation.

Prompt 3:

```text
Review the generated code against this required demo flow:
create Sale -> create Agency assigned to Sale -> create Track Record assigned
to Agency -> view dashboard stats. Point out anything that is outside scope or
could break the relationship between records.
```

Why it helped:

This helped me use AI as a review assistant after implementation, especially for checking whether generated code stayed aligned with the assignment.

## 4. AI mistakes and debugging

AI was helpful for speed, but it still required manual control and debugging.

Some issues I had to catch or correct:

- AI sometimes suggested extra features such as authentication, role management, or advanced filtering. I removed those because they were outside the test scope.
- Some generated snippets placed too much logic in the route handlers. I moved that logic into services so the backend stayed easier to explain.
- Some repeated code did not invalidate all related frontend queries at first. I checked the flow manually and made sure dashboard stats refresh after changes that affect totals.
- AI-generated test ideas were broader than necessary. I reduced them to the behaviors most relevant to the assignment: linked record creation, invalid parent IDs, list endpoints, and dashboard totals.
- I had to compare generated field names with the requirement so that `sale_id`, `agency_id`, `sales`, `agencies`, and `track_records` stayed consistent.

My debugging process was to run the relevant tests, inspect the generated code, and manually verify the main demo path from backend to frontend.

## 5. Notes on AI usage

I used AI as a support tool for repetitive coding and review, not as the decision-maker for the project.

The important implementation decisions were made by me:

- I defined the entity relationships and the main workflow.
- I chose the backend layer structure.
- I decided which features were in scope and which were not.
- I reviewed generated code for correctness and consistency.
- I verified that the final project still matched the original assignment.

If I had more time, I would use AI in the same way: mostly for generating repetitive tests, checking edge cases, and improving documentation after the main technical decisions are already clear.
