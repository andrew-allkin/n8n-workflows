# AI Reading Recommender

An intelligent n8n workflow that discovers, evaluates, and recommends interesting reading material about AI topics. Simply click "Test workflow" in n8n, enter your topic of interest (or leave empty for general AI search), and get an AI-curated recommendation from multiple sources.

## Features

**Topic-Based Discovery**
- Enter a specific AI topic when running the workflow (e.g., "RAG", "AI agents", "transformers")
- Intelligent fallback to general AI topics if no topic is provided
- Dynamic search queries customized for each topic across all sources
- Easy-to-use interface - just click "Test workflow" and set your topic

**Multi-Source Discovery**
- Academic papers from arXiv
- Developer articles from Dev.to
- Community discussions from HackerNews
- Easily extensible to add more sources (Medium, Substack, RSS feeds, etc.)

**AI-Powered Selection**
- Uses OpenAI GPT-4o-mini to analyze and rank content
- Evaluates based on depth, novelty, practical value, and writing quality
- Selects the single most interesting piece each run

**Smart Tracking**
- PostgreSQL database stores recommendation history
- Automatic deduplication - never recommends the same article twice
- Track reading status, ratings, and personal notes

**On-Demand Execution**
- Run manually whenever you want a recommendation
- Set your topic in the "Set Topic Here" node
- Returns formatted recommendation immediately
- No webhook setup required

**Diverse Content**
- Not limited to recent articles - discovers gems from any time period
- Balances academic papers, tutorials, blog posts, and discussions
- Covers full spectrum from technical depth to practical applications

---

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ Manual Trigger (Click "Test workflow" button)                   │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Set Topic Here                                                   │
│ Edit the 'topic' field to specify your AI topic                 │
│ Leave empty for general AI search                               │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ Process Topic Input (Python)                                    │
│ - Handle topic parameter or use fallback                        │
│ - Build custom search queries for each source                   │
└────────────────┬────────────────────────────────────────────────┘
                 │
      ┌──────────┴──────────┬──────────────────┐
      │                     │                  │
      ▼                     ▼                  ▼
┌───────────┐      ┌──────────────┐      ┌──────────────┐
│ arXiv API │      │ Dev.to API   │      │ HackerNews   │
│ (Papers)  │      │ (Articles)   │      │ (Discussions)│
└─────┬─────┘      └──────┬───────┘      └──────┬───────┘
      │                    │                     │
      └──────────┬─────────┴──────────┬──────────┘
                 ▼                    
         ┌──────────────┐
         │ Merge Sources│
         └──────┬───────┘
                ▼
      ┌─────────────────┐
      │ Standardize Data│
      │ (Python)        │
      └────────┬─────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌──────────────┐  ┌──────────────────┐
│ Get Already  │  │ Filter Out       │
│ Read Articles│──>│ Already Read     │
│ (Postgres)   │  │ (Python)         │
└──────────────┘  └─────────┬────────┘
                            ▼
                  ┌──────────────────┐
                  │ AI Ranking       │
                  │ (OpenAI GPT-4o)  │
                  └─────────┬────────┘
                            ▼
                  ┌──────────────────┐
                  │ Extract Selection│
                  │ (Python)         │
                  └─────────┬────────┘
                            ▼
                  ┌──────────────────┐
                  │ Save to Database │
                  │ (Postgres)       │
                  └─────────┬────────┘
                            ▼
                  ┌──────────────────┐
                  │ Format Output    │
                  │ (Python)         │
                  └──────────────────┘
```

---

## Required n8n Credentials

The workflow requires 2 credentials to function:

### PostgreSQL Database (REQUIRED)

**Purpose:** Tracks articles you've been recommended to prevent duplicates.

**Credential Name in n8n:** `Postgres account`

**Setup Steps:**
1. In n8n, go to Credentials > Add Credential > Postgres
2. Fill in your database connection details (from docker-compose.yaml):
   - Host: localhost
   - Database: n8n_workflows_data
   - User: admin
   - Password: adminpassword
   - Port: 5432
   - SSL: Off
3. Click Save
4. Run the setup script: `python setup_database.py`

---

### OpenAI API (REQUIRED)

**Purpose:** AI-powered ranking and selection of articles.

**Credential Name in n8n:** `OpenAI account`

**Setup Steps:**
1. Get an API key from https://platform.openai.com/api-keys
2. In n8n, go to Credentials > Add Credential > OpenAi API
3. Paste your API key (format: sk-proj-...)
4. Click Save

**Cost Estimate:**
- Model: gpt-4o-mini (cheapest OpenAI model)
- Cost per run: ~$0.01-0.05
- Monthly cost for occasional use: ~$0.20-1.00

**Alternative (Free):** Replace the OpenAI node with Ollama (local, free):
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Download model
ollama pull llama3.2

# In workflow: Use "Ollama Chat Model" node instead of OpenAI
```

---

### No Credentials Needed

These sources are free and require no authentication:
- arXiv API - Academic papers
- Dev.to API - Developer articles  
- HackerNews API - Community discussions

---

## Database Setup

Run the Python setup script to create the database table:

```bash
cd ai_reading_recommender

# Activate virtual environment
source venv/bin/activate

# Run setup script
python setup_database.py
```

The script will:
- Connect to the PostgreSQL database
- Create the read_articles table
- Create all necessary indexes

**Configuration:**
The script uses the PostgreSQL credentials from the main docker-compose.yaml file:
- Database: n8n_workflows_data
- User: admin
- Password: adminpassword
- Host: localhost
- Port: 5432

---

## Quick Start

### 1. Set Up Database

```bash
cd ai_reading_recommender

# Activate virtual environment
source venv/bin/activate

# Run setup script
python setup_database.py
```

### 2. Import Workflow

1. Open your n8n instance
2. Go to Workflows > Import from File
3. Select `ai_reading_recommender/n8n_workflow.json`
4. Click Import

### 3. Configure Credentials

Set up two credentials in n8n:
1. **Postgres account** - Your database connection
2. **OpenAI account** - Your OpenAI API key

See the "Required n8n Credentials" section for details.

### 4. Test the Workflow

1. Open the workflow in n8n
2. Click on the "Set Topic Here" node
3. In the parameters, enter your desired topic in the "topic" field (or leave empty)
4. Click "Test workflow" button in the top right
5. View your AI-selected recommendation in the Format Recommendation node

---

## Usage

### Run the Workflow

1. **Open the workflow** in your n8n instance
2. **Click on the "Set Topic Here" node**
3. **Enter your topic** in the "topic" field:
   - Examples: "RAG retrieval augmented generation", "AI agents", "transformers", "prompt engineering"
   - Or leave empty for general AI search
4. **Click "Test workflow"** button (top right)
5. **Wait for results** - the workflow will search all sources, filter duplicates, and return your AI-selected recommendation
6. **View the output** in the "Format Recommendation" node

### Example Topics

**Specific AI Topics:**
- "RAG retrieval augmented generation"
- "AI agents"
- "transformers"
- "prompt engineering"
- "diffusion models"
- "fine-tuning LLMs"
- "multimodal AI"
- "vision transformers"

**General Search:**
- Leave the topic field empty
- The workflow will search for general AI, machine learning, and deep learning content

### Changing Topics Between Runs

To search for a different topic:
1. Click on the "Set Topic Here" node
2. Change the "topic" value
3. Click "Test workflow" again

---

## Configuration

### Customizing the Fallback Topics

Edit the Process Topic Input node's Python code to change the fallback behavior:

```python
# If no topic provided, select a general AI search
if not topic:
    topic = 'AI OR machine learning OR deep learning'
    search_mode = 'general'
```

You can change this to any default topic you prefer.

### Customizing Search Sources

#### arXiv Papers (Academic)
The search query is built dynamically from the topic:
```python
arxiv_query = f"cat:cs.AI OR cat:cs.LG AND ({topic})"
```

You can modify this in the Process Topic Input node.

#### Dev.to Articles (Developer Content)
The tag is extracted from the topic (spaces removed, max 20 chars):
```python
devto_tag = topic.lower().replace(' ', '').replace('ai', 'ai')[:20]
```

#### HackerNews (Discussions)
Uses the topic directly as the search query:
```python
hackernews_query = topic
```

### AI Ranking Customization

The AI prompt is stored in `ai_ranking_system_prompt.md`. To change how the AI evaluates articles, edit this file and update the AI Ranking node in n8n.

Current criteria:
- Depth of insight and technical content
- Practical value and applicability
- Novelty of perspective or approach
- Writing quality and clarity
- Relevance to current AI developments

---

## Viewing Recommendations

### Database Query

```sql
SELECT 
  title,
  url,
  source,
  content_type,
  date_recommended,
  notes as ai_reasoning,
  is_read
FROM read_articles
ORDER BY date_recommended DESC
LIMIT 10;
```

### Marking Articles as Read

After reading an article, update the database:

```sql
UPDATE read_articles
SET 
  is_read = TRUE,
  date_read = CURRENT_TIMESTAMP,
  rating = 4,
  notes = 'Great practical examples of RAG implementation'
WHERE url = 'https://example.com/article-url';
```

---

## Output Format

Each recommendation includes:

```
AI READING RECOMMENDATION

Title: [Article Title]

URL: [Direct Link]

Source: [arXiv/Dev.to/HackerNews] | Type: [paper/article]

Author: [Author Name]

Estimated Reading Time: [X] minutes

Published: [Publication Date]

Summary:
[Brief summary of the content]

Why This Was Selected:
[AI's reasoning for choosing this article]

---
Recommended on: [Date and Time]
```

---

## Adding More Sources

The workflow is designed to be easily extensible. Here's how to add new content sources:

### Example: Adding Medium Articles

1. Add a new HTTP Request node:
   - Method: GET
   - URL: `https://medium.com/feed/tag/artificial-intelligence`

2. Connect it to the Merge All Sources node

3. Update the Standardize Data Format Python code to handle Medium's format

---

## Troubleshooting

### "No new articles found"

**Cause:** All discovered articles have already been recommended.

**Solutions:**
1. Wait for more content to be published
2. Try a different topic
3. Expand search queries
4. Manually clear old recommendations:
   ```sql
   DELETE FROM read_articles 
   WHERE date_recommended < CURRENT_DATE - INTERVAL '90 days';
   ```

### "OpenAI API error: Rate limit exceeded"

**Cause:** Too many API calls in a short time.

**Solutions:**
1. Check your OpenAI usage limits
2. Upgrade your OpenAI plan if needed
3. Reduce frequency of requests

### "Database connection failed"

**Cause:** PostgreSQL credentials are incorrect or database is not running.

**Solutions:**
1. Verify PostgreSQL is running: `docker ps`
2. Check credentials in n8n match docker-compose.yaml
3. Test connection: `psql -h localhost -U admin -d n8n_workflows_data`

### "Workflow returns no results"

**Cause:** API endpoints changed or network issues.

**Solutions:**
1. Test each source node individually
2. Check API endpoint URLs are still valid
3. Verify network connectivity
4. Check n8n logs for detailed errors

---

## Customization Ideas

### Add Email Notifications

1. Add a Gmail or Send Email node after Format Recommendation
2. Use the formatted message as email body
3. Send to yourself on each recommendation

### Add Slack Integration

1. Add a Slack node after Format Recommendation
2. Post to a dedicated reading channel
3. Team members can vote on recommendations

### Create a Reading List Web App

1. Add a Webhook node to query database
2. Create simple HTML page to display recommendations
3. Show articles with filters by source, content type, etc.

### Schedule Regular Recommendations

1. Replace Manual Trigger with Schedule Trigger node
2. Set schedule (e.g., weekly on Mondays at 9 AM)
3. Configure the "Set Topic Here" node with a default topic (or leave empty)
4. Get automatic recommendations on schedule

---

## Cost Analysis

### Monthly Cost Breakdown (Occasional Use)

| Service | Cost |
|---------|------|
| OpenAI API (GPT-4o-mini) | ~$0.20-1.00/month |
| arXiv API | Free |
| Dev.to API | Free |
| HackerNews API | Free |
| PostgreSQL (self-hosted) | Free |
| **Total** | **~$0.20-1.00/month** |

Extremely affordable for curated, AI-selected reading recommendations!

---

## Database Schema

### Table: read_articles

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| title | VARCHAR(500) | Article title |
| url | VARCHAR(1000) | Article URL (unique) |
| summary | TEXT | Brief summary/abstract |
| source | VARCHAR(200) | Content source (arXiv, Dev.to, etc.) |
| content_type | VARCHAR(50) | Type: paper, blog, tutorial, article |
| subtopic | VARCHAR(100) | Subtopic: llms, diffusion, agents, etc. |
| date_published | TIMESTAMP | When article was published |
| date_recommended | TIMESTAMP | When recommended by workflow |
| date_read | TIMESTAMP | When you read it |
| rating | INTEGER | Your rating (1-5) |
| notes | TEXT | Personal notes or AI reasoning |
| author | VARCHAR(200) | Author name |
| reading_time_minutes | INTEGER | Estimated reading time |
| is_read | BOOLEAN | Whether you've read it |
| created_at | TIMESTAMP | Record creation time |
| updated_at | TIMESTAMP | Record update time |

---

## Advanced Features

### Intelligent Filtering

The workflow includes smart deduplication that:
- Prevents recommending the same URL twice
- Logs all recommendations in database
- Allows you to manually add articles to your "already read" list

### Dynamic Topic Processing

The Process Topic Input node:
- Accepts any AI-related topic
- Builds custom search queries for each source
- Falls back to general AI search if no topic provided
- Handles edge cases like empty strings or whitespace

### All Code Nodes Use Python

Following best practices, all Code nodes in the workflow use Python instead of JavaScript for consistency.

---

## Project Files

- `n8n_workflow.json` - Complete workflow definition
- `ai_ranking_system_prompt.md` - AI system and user prompts
- `setup_database.py` - Database setup script
- `requirements.txt` - Python dependencies
- `venv/` - Virtual environment with dependencies
- `README.md` - This documentation file

---

## License

This workflow is provided as-is for personal and educational use. Feel free to modify and extend it to suit your needs.

---

**Happy Reading!**
