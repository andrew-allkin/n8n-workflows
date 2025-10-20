# AGENTS.md - Critical Guidelines for AI Agents

**IMPORTANT: All AI agents MUST follow these rules when making changes or suggesting ideas for this repository.**

---

## Project Overview

This is an **n8n-workflows** repository that serves as a centralized collection of all n8n workflow projects. Each workflow represents a complete, self-contained automation solution with its own dedicated folder containing all necessary files, documentation, and setup scripts.

---

## Project Structure Rules

### Folder Organization
- **Each workflow/project MUST be in its own dedicated folder**
- Folder names should be descriptive and use snake_case (e.g., `text_to_sql_postgres_agent`, `ai_reading_recommender`)
- All project-related files MUST be contained within the project's folder

### Documentation Rules (STRICTLY ENFORCED)
- **ONLY ONE `README.md` file per project folder**
- **NO other markdown files allowed** (no `SETUP.md`, `GUIDE.md`, `SUMMARY.md`, etc.)
- **NO separate documentation files** for setup, configuration, or summaries
- All documentation, setup instructions, usage guides, and summaries MUST be consolidated into the single `README.md` file
- **Exception:** System and user prompts for AI nodes (see AI Prompt Files section below)
- The `README.md` must be comprehensive and include:
  - Project overview
  - Prerequisites (including required n8n credentials)
  - Setup instructions
  - Database setup (if applicable)
  - Usage instructions
  - Workflow description
  - Any other relevant information

### Git Configuration Rules
- **ONLY ONE `.gitignore` file is allowed in the root directory of the repository**
- **NO project-specific `.gitignore` files** are allowed in individual project folders
- All ignore patterns for the entire repository must be defined in the root `.gitignore`

---

## Database Configuration

### Single PostgreSQL Database
- **Database Name:** `n8n_workflows_data`
- **Host:** `postgres-db` (inside Docker network) or `localhost` (external access)
- **Port:** `5432`
- **User:** `admin`
- **Password:** `adminpassword`

### Database Connection Rules
- **ALWAYS use hardcoded database connection details** as specified above
- **ALWAYS reference the connection details from the docker-compose.yaml file**
- **NEVER use environment variables or configuration files for database credentials**
- All projects share the same PostgreSQL instance but may use different schemas or tables

### Database Setup Scripts
- If a project requires PostgreSQL, **ALWAYS create a `setup_database.py` script** in the project folder
- **CRITICAL: The setup script MUST be MINIMAL**
- The setup script must ONLY contain:
  - Database connection code using hardcoded credentials
  - SQL statements to create tables
  - SQL statements to insert necessary data
- The setup script must NOT include:
  - Database existence checks
  - Connection validation logic
  - Complex error handling
  - Any other non-essential code
- **NO .sql files allowed** - all table creation and data insertion must be done in the Python script
- Use simple, direct SQL execution with psycopg2 or similar libraries
- Include basic print statements to show setup progress

**Example connection string:**
```python
# For scripts running outside Docker
host="localhost"
# For scripts running inside Docker
host="postgres-db"

database="n8n_workflows_data"
user="admin"
password="adminpassword"
port="5432"
```

---

## Python Scripts Requirements

### Virtual Environment (MANDATORY)
- If ANY Python scripts are required for the project:
  - **ALWAYS create a virtual environment (`venv`) in the project folder**
  - **ALWAYS include a `requirements.txt` file** with all dependencies and versions
  - The venv folder should be named `venv` (lowercase)

### Requirements File
- Must include all dependencies with version pinning where appropriate
- Common dependencies:
  ```
  psycopg2-binary==2.9.9  # For PostgreSQL
  pandas==2.1.4           # For data manipulation
  numpy==1.26.4           # For numerical operations
  ```

---

## n8n Workflow Management

### MCP Server Usage (CRITICAL)
- **ALWAYS use the n8n MCP (Model Context Protocol) server** when:
  - Creating new workflows
  - Editing existing workflows
  - Improving or debugging workflows
  - Understanding workflow structure
  - Validating workflow configurations
- The MCP server provides tools for workflow validation, node information, and template management
- Never manually edit workflow JSON without using MCP tools to validate

### Code Node Requirements
- **ALWAYS use Python as the language for all Code nodes in n8n workflows**
- Never use JavaScript for Code nodes
- This ensures consistency across all workflows in the repository

### Workflow JSON Files
- **ALWAYS store a copy of the workflow JSON** in a file within the project folder
- The JSON file should be named `n8n_workflow.json` or descriptively (e.g., `gmail_delete_emails_workflow.json`)
- Keep the JSON file updated whenever the workflow is modified in n8n
- The JSON file serves as:
  - Backup of the workflow
  - Version control reference
  - Import template for others

---

## AI Prompt Files (MANDATORY FOR AI NODES)

### System and User Prompt Documentation
- **ALWAYS create a markdown file** containing the system prompt and user prompt for:
  - AI Tool Calling Agent nodes
  - AI Chat Model nodes
  - Any node that uses AI/LLM functionality with custom prompts
- The markdown file must be named descriptively (e.g., `agent_system_prompt.md`, `chat_model_prompts.md`)
- The content in the markdown file **MUST exactly match** what is configured in the corresponding n8n node
- This serves as:
  - Version control for prompt engineering
  - Easy editing and review of prompts outside of n8n
  - Documentation of prompt logic and reasoning
  - Backup of prompt configurations

### Emoji Restriction in AI Prompts (CRITICAL)
- **NEVER include emojis in system prompts** for OpenAI models
- **NEVER include emojis in system prompts** for AI Tool Calling Agent nodes
- **NEVER include emojis in user prompts** for AI Chat Model nodes
- Emojis can interfere with model performance and token counting
- Use plain text only for all AI prompts

**Example prompt file structure:**
```markdown
# Agent System Prompt

## System Instructions

You are a helpful assistant that...

## Task Description

Your task is to...

## Output Format

Please respond in the following format...

---

# User Prompt Template

{{user_input}}

Additional context: {{context}}
```

---

## n8n Credentials Documentation

### Required Credentials
- **ALWAYS specify in the `README.md`** which n8n credentials are required for the workflow
- Common credential types include:
  - **OpenAI API** - for AI/LLM integrations
  - **Google OAuth2** - for Gmail, Google Sheets, Google Drive, etc.
  - **Postgres** - for database connections
  - **HTTP Basic Auth / API Keys** - for various API integrations
  - **Webhook URLs** - for trigger configurations

### Credential Documentation Format
Include a dedicated section in the README.md like:

```markdown
## Required n8n Credentials

This workflow requires the following credentials to be configured in n8n:

1. **PostgreSQL** - Connection to the shared database
   - Host: postgres-db
   - Port: 5432
   - Database: n8n_workflows_data
   - User: admin
   - Password: adminpassword

2. **OpenAI API** - For AI agent functionality
   - API Key required

3. **Google OAuth2** - For Gmail access
   - OAuth2 credentials required
   - Scopes: gmail.readonly, gmail.modify
```

---

## Docker Compose Integration

### Main Docker Compose File
- The root `docker-compose.yaml` defines:
  - n8n service (port 5678)
  - PostgreSQL service (port 5432)
  - Shared backend network

### Project-Specific Docker Compose
- Individual projects MAY have their own `docker-compose.yaml` if they need additional services
- Project-specific compose files should complement, not replace, the root compose file
- Ensure network compatibility with the root `backend-net` network

---

## Checklist for New Projects

When creating a new workflow project, ensure:

- Project folder created with descriptive snake_case name
- Single `README.md` file with complete documentation
- No additional markdown files created (except AI prompt files)
- If AI nodes used: Prompt markdown files created and match n8n node configuration
- No emojis in any AI system or user prompts
- If PostgreSQL needed: MINIMAL `setup_database.py` script created (only table creation and data insertion)
- No .sql files (all database setup done in Python script)
- If Python needed: `venv` folder and `requirements.txt` file created
- All Code nodes in n8n workflow use Python (not JavaScript)
- Workflow JSON file (`n8n_workflow.json`) saved in the folder
- Required n8n credentials clearly documented in README.md
- Used n8n MCP server tools to validate workflow configuration
- All connection details match the docker-compose.yaml configuration
- No project-specific `.gitignore` file created (only root `.gitignore` allowed)

---

## Common Mistakes to Avoid

1. Creating multiple markdown files (SETUP.md, GUIDE.md, etc.) - Exception: AI prompt files
2. Using environment variables for database credentials
3. Creating Python scripts without a virtual environment
4. Missing requirements.txt file
5. Not documenting required n8n credentials
6. Not saving workflow JSON backup
7. Manually editing workflows without using MCP validation
8. Using different database names or credentials
9. Placing project files outside the project folder
10. Including emojis in AI system or user prompts
11. Not creating prompt markdown files for AI nodes
12. Creating project-specific `.gitignore` files
13. Creating .sql files for database setup (use Python script only)
14. Adding unnecessary checks and validation to setup_database.py script (keep it MINIMAL)
15. Using JavaScript in Code nodes instead of Python

---

## Best Practices

### Code Quality
- Write clean, well-commented code
- Use descriptive variable and function names
- Include error handling in Python scripts
- Add logging/print statements for debugging

### Documentation Quality
- Write clear, step-by-step instructions
- Include examples and sample outputs
- Document troubleshooting steps
- Keep documentation up-to-date with code changes
- Never use emojis in technical documentation

### Workflow Design
- Use descriptive node names in n8n
- Add notes to complex nodes
- Implement error handling in workflows
- Test workflows thoroughly before committing
- Keep AI prompts clean and emoji-free
- Always use Python for Code nodes (never JavaScript)
- Keep database setup scripts minimal and focused

### AI Prompt Engineering
- Store all prompts in dedicated markdown files
- Keep prompts version-controlled and documented
- Avoid emojis in all AI-related prompts
- Test prompts thoroughly before committing
- Use clear, concise language in prompts

---

## Reference Examples

Existing projects in this repository that follow these guidelines:
- `text_to_sql_postgres_agent/` - Text-to-SQL agent with PostgreSQL integration
- `ai_reading_recommender/` - AI-powered reading recommendation system
- `gmail_delete_emails/` - Gmail automation workflow

Refer to these projects as templates when creating new workflows.

---

**Remember: These rules are MANDATORY, not suggestions. Following them ensures consistency, maintainability, and ease of collaboration across all workflow projects.**
