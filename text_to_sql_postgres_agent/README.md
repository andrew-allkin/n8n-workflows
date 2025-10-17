# Text-to-SQL Agent for PostgreSQL

A complete AI-powered natural language database query system built with n8n workflow automation. Ask questions in plain English, and the agent automatically discovers your database structure, generates accurate SQL queries, and presents results with beautiful formatting and optional visualizations.

---

## 🎯 What It Does

- **Natural Language Queries:** Ask questions like "Show me the top 5 best-selling products"
- **Automatic Schema Discovery:** Agent discovers tables and relationships automatically
- **Intelligent SQL Generation:** Translates questions into accurate SELECT queries
- **Beautiful Results:** Formatted responses with emojis, bold text, and structured sections
- **Visual Charts:** Create bar charts, line graphs, and pie charts on demand via QuickChart
- **Conversational Memory:** Maintains context across 15 messages

### Example Queries
```
"Which customers have spent more than $500?"
"Show me monthly revenue trends and create a chart"
"What are the top 5 best-selling products?"
"List all orders from California customers"
```

---

## 📊 Database Schema

The PostgreSQL database contains sample e-commerce data:

| Table | Records | Description |
|-------|---------|-------------|
| **customers** | 25 | Customer information (name, email, phone, location) |
| **products** | 25 | Product catalog (name, category, price, stock, SKU) |
| **orders** | 28 | Order headers (date, total, status, payment method) |
| **order_items** | 57 | Individual line items in each order |

**Relationships:**
```
customers (customer_id) ←─ orders (customer_id)
                              ├─ order_items (order_id)
products (product_id) ←────── order_items (product_id)
```

---

## 🏗️ Architecture

### n8n Workflow
- **ID:** `zp9dO4iTVnEd2FeP`
- **Name:** Text-to-SQL Agent for Postgres
- **Status:** Active
- **Updated:** October 17, 2025

### Workflow Nodes (10 Total)

#### Core Components
1. **Chat Trigger** - Receives user messages via webhook (ID: `46d771e0-b43f-427f-89db-eeae13573a3c`)
2. **AI Agent** - Orchestrates the entire workflow with strict rules
3. **OpenAI Chat Model** - Uses GPT-4 (temperature: 0.2 for consistency)
4. **Postgres Chat Memory** - Maintains conversation context (15 messages)

#### Database Tools (Required)
5. **list_all_tables** - Discovers available tables in public schema
6. **get_table_schema_details** - Retrieves detailed column information
7. **execute_final_sql_query** - Executes constructed SELECT queries

#### Helper Tools (Optional)
8. **get_distinct_column_values** - Checks unique values in columns
9. **get_table_row_count** - Counts records for context
10. **QuickChart** - Creates visualizations (bar, line, pie charts)

---

## 🚀 Setup Instructions

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- n8n instance (local or cloud)
- OpenAI API key

### Step 1: Start PostgreSQL Database

```bash
cd text_to_sql_postgres_agent
docker-compose up -d
```

This starts PostgreSQL with:
- **Host:** localhost
- **Port:** 5432
- **Database:** test
- **User:** admin
- **Password:** adminpassword

### Step 2: Install Python Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Load Database

```bash
python setup_database.py
```

This script:
- Creates all 4 tables with proper schema
- Loads data from CSV files in `data/` folder
- Sets up foreign key relationships
- Verifies data integrity
- Displays sample query result

### Step 4: Configure n8n Workflow

#### Docker Network (Pre-configured)

Both n8n and PostgreSQL containers are already connected via the `backend-net` network in the docker-compose file, so they can communicate using service names.

**Connection Settings:**
- **Host in n8n:** Use `postgres-db` (the service name)
- **Port:** `5432`
- **From your local machine:** Use `localhost:5432`

No manual network configuration is needed! 🎉

#### Configure Credentials in n8n

This workflow requires **two types of credentials**: OpenAI API for the AI agent and PostgreSQL for database access.

**1. Configure OpenAI API Credentials**

The workflow uses GPT-4 to translate natural language into SQL queries.

**A. Get Your OpenAI API Key**

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click **Create new secret key**
4. Give it a name (e.g., "n8n text-to-sql")
5. Copy the key immediately (you won't be able to see it again)
6. **Important**: Ensure you have credits in your OpenAI account

**B. Add to n8n**

1. Open n8n at http://localhost:5678
2. Navigate to **Settings** > **Credentials** (or click the credentials icon)
3. Click **Add Credential** and search for **OpenAI API**
4. Enter your API key in the **API Key** field
5. (Optional) Set **Organization ID** if you have one
6. Give it a name (e.g., "OpenAI account") and click **Save**

**C. Assign to Workflow**

1. Import or open the Text-to-SQL workflow
2. Click on the **OpenAI Chat Model** node (red icon with "AI" label)
3. In the **Credentials** dropdown, select the OpenAI credential you just created
4. Save the workflow

**Troubleshooting OpenAI:**
- **"Incorrect API key"**: Verify you copied the full key without extra spaces
- **"You exceeded your current quota"**: Add payment method and credits at https://platform.openai.com/account/billing
- **"Rate limit exceeded"**: Your account has hit API rate limits - wait or upgrade your plan
- **"Model not found"**: Ensure your API key has access to GPT-4 (check your OpenAI account tier)

---

**2. Configure PostgreSQL Database Credentials**

The workflow needs access to your PostgreSQL database to execute queries.

**A. Database Connection Details**

Since both n8n and PostgreSQL run in Docker with the shared `backend-net` network:
- **Host**: `postgres-db` (the service name, NOT localhost)
- **Port**: `5432`
- **Database**: `test`
- **User**: `admin`
- **Password**: `adminpassword`

**B. Add to n8n**

1. In n8n, go to **Settings** > **Credentials**
2. Click **Add Credential** and search for **Postgres**
3. Enter the connection details:
   - **Host**: `postgres-db` ⚠️ **Critical**: Use the service name, not localhost or 127.0.0.1
   - **Port**: `5432`
   - **Database**: `test`
   - **User**: `admin`
   - **Password**: `adminpassword`
   - **SSL**: Leave disabled (not needed for local Docker network)
4. Click **Test** to verify connection
   - ✅ You should see "Connection successful"
   - ❌ If it fails, see troubleshooting below
5. Give it a name (e.g., "Postgres account") and click **Save**

**C. Assign to Workflow Nodes**

The workflow has **6 PostgreSQL nodes** that all need credentials:

1. Import or open the Text-to-SQL workflow
2. Update each of these nodes:
   - **list_all_tables** (green database icon)
   - **get_table_schema_details** (green database icon)
   - **execute_final_sql_query** (green database icon)
   - **get_distinct_column_values** (green database icon)
   - **get_table_row_count** (green database icon)
   - **Postgres Chat Memory** (green database icon)
3. For each node, click it and select your Postgres credential from the dropdown
4. Save the workflow

**Troubleshooting PostgreSQL:**
- **"Connection refused"**: 
  - Check PostgreSQL container is running: `docker ps | grep postgres-db`
  - Verify you used `postgres-db` as host (NOT `localhost`)
  - Ensure both containers are on backend-net: `docker network inspect n8n-workflows_backend-net`
- **"FATAL: password authentication failed"**: 
  - Double-check credentials match docker-compose.yaml
  - Default is `admin` / `adminpassword`
- **"Connection timeout"**: 
  - PostgreSQL container may still be starting - wait 10 seconds and retry
  - Check logs: `docker logs postgres-db`
- **"Database 'test' does not exist"**:
  - Run the setup script: `python setup_database.py`
  - Or create manually: `docker exec -it postgres-db psql -U admin -c "CREATE DATABASE test;"`

**Testing the Connection**

You can manually test the connection from within the n8n container:

```bash
# Test from n8n container
docker exec n8n psql -h postgres-db -p 5432 -U admin -d test -c "SELECT 1;"
```

If successful, you should see a result. If it fails, troubleshoot the network connection.

---

**3. Activate the Workflow**

After both credentials are configured and assigned to all nodes:

1. In the workflow editor, toggle the **Active** switch in the top-right corner
2. The switch should turn green
3. The workflow is now ready to receive chat messages

---

## 💬 Using the Chat Interface

### Option 1: Start the Web Server (Recommended)

```bash
python3 start_chat_ui.py
```

**What happens:**
- Server starts on available port (8000, 8001, 8080, etc.)
- Browser opens automatically to chat UI
- Webhook URL is pre-configured

**Features:**
- 🎨 Modern gradient purple design with smooth animations
- 📊 **Automatic image rendering** - Displays charts from QuickChart
- 💾 Persistent session history
- 📱 Responsive design for mobile and desktop
- ⚡ Real-time typing indicators

### Option 2: Use n8n's Built-in Chat UI

1. Click on "When chat message received" node
2. Copy the webhook URL
3. Open URL in browser to access n8n's default chat interface

### Webhook URL
```
http://localhost:5678/webhook/46d771e0-b43f-427f-89db-eeae13573a3c/chat
```

---

## 🎨 Response Formatting

The agent returns beautifully formatted responses with:

### Formatting Elements
- **Emojis:** 📊 💰 👤 📈 ✅ 🏆 for visual appeal
- **Bold text:** Emphasizes product names, key metrics, customer names
- **Sections:** Clear hierarchy with blank lines
- **Horizontal lines:** `---` separates major sections
- **Lists:** Numbered lists for rankings, bullet points for insights
- **Summary stats:** Total counts, averages, growth percentages

### Example Response
```
I found the top 5 best-selling products based on total quantity sold.

📊 **Top 5 Products:**

1. **Wireless Mouse** - 6 units sold
2. **Wireless Headphones** - 6 units sold
3. **Webcam Cover** - 6 units sold
4. **USB-C Cable** - 5 units sold
5. **Monitor 27inch** - 5 units sold

---

📈 **Summary:**
- **Total Units Sold:** 28 units
- **Average per Product:** 5.6 units

💡 **Key Insights:**
- The top 3 products are tied at 6 units each
- Accessories dominate the top 5
- Consistent sales performance

Would you like me to create a bar chart to visualize this?
```

---

## 📈 Visualization Support

### How It Works
1. **User requests visualization** (e.g., "create a chart of monthly revenue")
2. **AI Agent** queries database and gets data
3. **AI Agent calls QuickChart tool** with chart configuration
4. **QuickChart returns image URL** (`https://quickchart.io/chart?c={config}`)
5. **Agent includes image in response** using markdown: `![Chart](url)`
6. **Chat UI automatically renders** the image inline

### Supported Chart Types
- 📊 **Bar charts** - Category comparisons, rankings
- 📈 **Line charts** - Time series, trends over time
- 🥧 **Pie charts** - Proportions, percentage breakdowns
- 📉 **Scatter plots** - Correlations, distributions

### How to Request Charts
- **Direct:** "Show me X and create a chart"
- **Follow-up:** "Can you visualize this as a line chart?"
- **Accept offer:** Agent suggests visualization after showing data

---

## 🧠 How the Agent Works

The AI agent follows a **strict 6-step workflow** enforced by the system prompt:

### Step 1: Discover Tables (Required)
- Calls `list_all_tables` to see all available tables
- Identifies relevant tables for the question

### Step 2: Understand Schema (Required)
- Calls `get_table_schema_details` for each relevant table
- Studies columns, data types, primary keys, foreign keys
- May call multiple times for complex queries with JOINs

### Step 3: Optional Helper Tools (When Needed)
- `get_distinct_column_values`: Check what values exist in a column
- `get_table_row_count`: Understand dataset size

### Step 4: Construct Query
- Builds SQL SELECT statement using discovered schema
- Applies JOINs, WHERE, GROUP BY, ORDER BY, LIMIT clauses

### Step 5: Execute Query
- Runs SQL using `execute_final_sql_query`
- Receives results

### Step 6: Present Results
- Formats data with emojis, bold text, sections
- Provides insights and summaries
- Offers to create visualizations
- Suggests follow-up questions

---

## 💻 Direct Database Access

### Using psql
```bash
psql -h localhost -p 5432 -U admin -d test
# Password: adminpassword
```

### Using Python
```python
import psycopg2

conn = psycopg2.connect(
    host='localhost',  # use 'postgres-db' if running inside Docker network
    port=5432,
    database='test',
    user='admin',
    password='adminpassword'
)
```

---

## 📁 Project Structure

```
text_to_sql_postgres_agent/
├── README.md                 # This file - complete documentation
├── system_prompt.md          # AI agent instructions (used in n8n)
├── chat_ui.html              # Custom chat interface with image support
├── start_chat_ui.py          # Python server for chat UI
├── docker-compose.yaml       # PostgreSQL container configuration
├── requirements.txt          # Python dependencies
├── setup_database.py         # Database setup script
├── data/                     # CSV data files
│   ├── customers.csv         # Customer data
│   ├── products.csv          # Product catalog
│   ├── orders.csv            # Order records
│   └── order_items.csv       # Order line items
└── venv/                     # Python virtual environment
```

---

## 🛠️ Troubleshooting

### PostgreSQL Connection Issues

**Problem:** n8n can't connect to PostgreSQL

**Solutions:**
1. Verify PostgreSQL is running:
   ```bash
   docker ps
   ```

2. Check hostname in n8n credentials:
   - **Docker n8n (this setup):** Use `postgres-db` (pre-configured network)
   - **Local n8n:** Use `localhost`

3. Verify Docker network (both containers should be on backend-net):
   ```bash
   docker network inspect backend-net
   ```

4. Test connection manually:
   ```bash
   docker exec -it n8n psql -h postgres-db -p 5432 -U admin -d test
   ```

### Agent Not Following Steps

**Problem:** Agent skips schema discovery or makes incorrect queries

**Solution:**
- System prompt enforces workflow strictly
- Verify the "Text-to-SQL Agent" node has the full system prompt
- Check OpenAI API key is valid with sufficient credits
- Try rephrasing question to be more specific

### Workflow Not Responding

**Problem:** Chat interface doesn't respond

**Solutions:**
1. Ensure workflow is **Active** (toggle in top-right)
2. Check webhook URL is correct
3. View workflow execution logs in n8n for errors
4. Verify all tool nodes are connected to AI Agent node

### Chat UI Connection Issues

**Problem:** Chat UI can't connect to workflow

**Solutions:**
1. Check webhook URL in chat UI settings
2. Verify CORS settings in n8n (Settings → Security → Allowed Origins)
3. Check browser console (F12) for error messages
4. Test webhook with curl:
   ```bash
   curl -X POST http://localhost:5678/webhook/46d771e0-b43f-427f-89db-eeae13573a3c/chat \
     -H "Content-Type: application/json" \
     -d '{"chatInput": "test", "sessionId": "test123"}'
   ```

### Images Not Displaying

**Problem:** Charts not appearing in chat

**Solutions:**
1. Verify QuickChart tool is enabled in workflow
2. Check response format includes markdown: `![Chart](url)`
3. Test image URL directly in browser
4. Ask explicitly: "Show me revenue trends and create a chart"

### Server Port Already in Use

**Problem:** `start_chat_ui.py` fails with "Address already in use"

**Solution:**
The script automatically tries multiple ports (8000, 8001, 8080, 8888, 3000, 5000). If all are busy, stop other servers or specify a custom port.

---

## 🔒 Security Notes

- **Read-Only Queries:** Agent only generates SELECT statements
- **No Modifications:** INSERT, UPDATE, DELETE, DROP, ALTER are forbidden
- **Result Limits:** Default LIMIT 1000 rows prevents large result sets
- **Credential Storage:** Database credentials secured in n8n's credential store
- **Public Webhook:** Chat webhook is public by default - add authentication for production

---

## 📊 Sample Queries Reference

### Simple Queries
```sql
-- All customers
SELECT * FROM customers LIMIT 1000;

-- Products by category
SELECT * FROM products WHERE category = 'Electronics';

-- Recent orders
SELECT * FROM orders WHERE order_date >= CURRENT_DATE - INTERVAL '30 days';
```

### Join Queries
```sql
-- Orders with customer names
SELECT c.name, o.order_id, o.total_amount, o.status
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id;

-- Top selling products
SELECT p.product_name, SUM(oi.quantity) as total_sold
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_sold DESC
LIMIT 10;
```

### Aggregate Queries
```sql
-- Revenue by month
SELECT 
    DATE_TRUNC('month', order_date) as month,
    SUM(total_amount) as revenue
FROM orders
GROUP BY month
ORDER BY month;

-- Customer spending
SELECT 
    c.name,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_spent
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;
```

---

## 🎓 Key Features

### Intelligent Query Construction
- Automatic table discovery
- Schema-aware JOIN generation
- Foreign key relationship detection
- Type-aware filtering
- Performance-optimized queries

### Conversational Memory
- Remembers last 15 messages
- Context-aware follow-ups
- Session persistence
- Natural conversation flow

### Error Prevention
- Enforced workflow steps
- Schema validation
- Read-only operations
- Query size limits

### User Experience
- Beautiful formatted responses
- Visual charts on demand
- Clear insights and patterns
- Actionable next steps

---

## 📚 Learning Resources

- **n8n Documentation:** https://docs.n8n.io
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/
- **OpenAI API:** https://platform.openai.com/docs
- **QuickChart:** https://quickchart.io/documentation/

---

## 📝 Technical Notes

- **AI Model:** GPT-4 with temperature 0.2 for consistent SQL generation
- **Memory:** Postgres-backed conversation history (15 messages)
- **System Prompt:** ~18,000 tokens enforcing strict workflow rules
- **Query Validation:** All SQL queries validated for read-only operations
- **Complexity:** Handles complex multi-table JOINs and aggregations
- **Visualizations:** QuickChart integration for inline chart rendering

---

## 🎯 Best Practices

### For Users
1. Be specific in your questions
2. Start simple, then add complexity
3. Use follow-up questions to refine results
4. Request charts for trends and comparisons
5. Ask for insights and recommendations

### For Developers
1. Keep system prompt updated in n8n workflow
2. Monitor OpenAI API usage and costs
3. Regularly backup conversation history
4. Test with various query complexities
5. Review execution logs for errors

---

## 🚀 Quick Start Checklist

- [ ] Start PostgreSQL: `docker-compose up -d`
- [ ] Install Python dependencies: `pip install -r requirements.txt`
- [ ] Load database: `python setup_database.py`
- [ ] Configure n8n PostgreSQL credentials
- [ ] Configure n8n OpenAI credentials
- [ ] Activate workflow in n8n
- [ ] Start chat UI: `python3 start_chat_ui.py`
- [ ] Test with sample query

---

**Need help?** Check n8n workflow execution logs for detailed error messages, or review `system_prompt.md` to understand agent behavior.

---

*Last Updated: October 17, 2025*
*Workflow Version: v1*
