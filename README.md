# n8n Workflows Repository

A collection of powerful n8n workflow automations with integrated Docker infrastructure for seamless deployment and execution.

## 📦 What's Inside

This repository contains ready-to-use n8n workflows along with a unified Docker Compose setup that provides:
- **n8n workflow automation platform** - Run workflows locally with full control
- **PostgreSQL database** - Shared database for workflows requiring data persistence
- **Pre-configured networking** - Containers can communicate seamlessly

## 📂 Workflows Included

### 1. Gmail Delete Emails
**Location:** `gmail_delete_emails/`

A workflow for bulk-deleting Gmail messages within a specific date range while preserving important labeled emails.

**Features:**
- Date range filtering
- Label-based protection
- Trash (not permanent delete)
- Manual trigger

**Use Case:** Clean up your inbox while protecting bank statements, medical records, and important correspondence.

[→ View detailed setup](./gmail_delete_emails/README.md)

---

### 2. Text-to-SQL Agent for PostgreSQL
**Location:** `text-to-sql-postgres-agent/`

An AI-powered natural language database query system that translates plain English questions into SQL queries.

**Features:**
- Natural language queries
- Automatic schema discovery
- Intelligent SQL generation
- Chart visualizations via QuickChart
- Conversational memory
- Beautiful formatted responses

**Use Case:** Query databases without writing SQL - "Show me the top 5 best-selling products" or "Create a chart of monthly revenue trends."

**Requires:** 
- OpenAI API key
- PostgreSQL database (uses the shared postgres-db container)

[→ View detailed setup](./text-to-sql-postgres-agent/README.md)

---

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Port 5678 (n8n) and 5432 (PostgreSQL) available

### Start the Infrastructure

```bash
# Clone the repository
git clone <repository-url>
cd n8n-workflows

# Start n8n and PostgreSQL
docker-compose up -d

# Access n8n
open http://localhost:5678
```

That's it! Both n8n and PostgreSQL are now running and connected.

## 🏗️ Infrastructure Setup

### Docker Compose Architecture

The `docker-compose.yaml` in the root directory manages two core services:

#### **n8n Container**
- **Image:** `docker.n8n.io/n8nio/n8n:latest`
- **Port:** 5678
- **Volume:** `n8n_data` - Persists workflows, credentials, and settings
- **Timezone:** Africa/Johannesburg (configurable)
- **Features:** Runners enabled for enhanced execution

#### **PostgreSQL Container**
- **Image:** `postgres:16`
- **Port:** 5432
- **Volume:** `n8n_workflows_postgres_data` - Persists database data
- **Database:** `test`
- **Credentials:** 
  - User: `admin`
  - Password: `adminpassword`

### Network Configuration

Both containers are connected via a **backend-net** bridge network, enabling them to communicate using service names:

```yaml
networks:
  backend-net:
    driver: bridge
```

**Why This Matters:**
- n8n can connect to PostgreSQL using hostname `postgres-db` instead of IP addresses
- No manual network configuration needed
- Simplified credential setup in n8n workflows
- Isolated network for security

### Creating PostgreSQL Credentials in n8n

When configuring workflows that need database access:

1. Open n8n at http://localhost:5678
2. Go to **Settings** → **Credentials**
3. Click **Create New Credential**
4. Select **Postgres**
5. Enter connection details:
   - **Host:** `postgres-db` (the service name - containers communicate via backend-net)
   - **Port:** `5432`
   - **Database:** `test`
   - **User:** `admin`
   - **Password:** `adminpassword`
6. Click **Test** to verify connection
7. **Save** the credential

The connection works because both containers share the `backend-net` network defined in docker-compose.

### Volume Persistence

All data is preserved across container restarts:
- **n8n_data:** Workflows, credentials, execution history, settings
- **n8n_workflows_postgres_data:** Complete PostgreSQL database

Volumes are explicitly named so they remain consistent regardless of directory location.

## 🔧 Managing the Infrastructure

### View Running Containers
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f n8n
docker-compose logs -f postgres-db
```

### Restart Services
```bash
# All services
docker-compose restart

# Specific service
docker-compose restart n8n
```

### Stop Services
```bash
docker-compose down
```

### Stop and Remove Volumes (⚠️ Deletes all data)
```bash
docker-compose down -v
```

### Verify Network Connection
```bash
# Check network details
docker network inspect n8n-workflows_backend-net

# Test connectivity from n8n to PostgreSQL
docker exec n8n ping postgres-db
```

## 📊 Accessing Services

| Service | URL | Purpose |
|---------|-----|---------|
| **n8n Web UI** | http://localhost:5678 | Workflow editor and management |
| **PostgreSQL** | localhost:5432 | Database access from local machine |

### Direct Database Access

From your local machine:
```bash
# Using psql
psql -h localhost -p 5432 -U admin -d test

# Using Python
import psycopg2
conn = psycopg2.connect(
    host='localhost',
    port=5432,
    database='test',
    user='admin',
    password='adminpassword'
)
```

From within Docker containers:
```bash
# Execute psql inside n8n container
docker exec -it n8n psql -h postgres-db -p 5432 -U admin -d test
```

## 🗂️ Repository Structure

```
n8n-workflows/
├── README.md                          # This file - overview and setup
├── docker-compose.yaml                # Infrastructure definition
├── .gitignore                         # Git ignore rules
│
├── gmail_delete_emails/               # Gmail cleanup workflow
│   ├── Gmail Date Range Delete.json   # n8n workflow file
│   └── README.md                      # Workflow-specific documentation
│
└── text-to-sql-postgres-agent/        # AI SQL query agent
    ├── n8n_workflow.json              # n8n workflow file
    ├── README.md                      # Workflow-specific documentation
    ├── agent_system_prompt.md         # AI agent instructions
    ├── setup_database.py              # Database initialization script
    ├── requirements.txt               # Python dependencies
    ├── chat_ui.html                   # Custom chat interface
    ├── start_chat_ui.py               # Web server for chat UI
    ├── data/                          # Sample CSV data
    │   ├── customers.csv
    │   ├── products.csv
    │   ├── orders.csv
    │   └── order_items.csv
    └── venv/                          # Python virtual environment
```

## 🔐 Security Considerations

### Database Credentials
The default PostgreSQL credentials (`admin`/`adminpassword`) are for **development use only**. For production:

1. Change the credentials in `docker-compose.yaml`:
   ```yaml
   environment:
     POSTGRES_USER: your_secure_user
     POSTGRES_PASSWORD: your_secure_password
   ```

2. Update credentials in n8n workflows accordingly

### n8n Webhooks
- Workflow webhooks are public by default
- Add authentication for production use
- Configure CORS settings in n8n Security settings

### Network Exposure
- PostgreSQL port 5432 is exposed for local development
- Remove port mapping in production if only n8n needs access:
  ```yaml
  # Remove or comment out:
  # ports:
  #   - "5432:5432"
  ```

## 🛠️ Troubleshooting

### Port Conflicts

**Problem:** Port 5678 or 5432 already in use

**Solution:**
```bash
# Check what's using the port
lsof -i :5678
lsof -i :5432

# Change ports in docker-compose.yaml
ports:
  - "5679:5678"  # Use different external port
```

### Container Won't Start

**Problem:** Container exits immediately

**Solution:**
```bash
# View detailed logs
docker-compose logs n8n
docker-compose logs postgres-db

# Check for volume permission issues
docker volume inspect n8n_data
```

### PostgreSQL Connection Failed

**Problem:** n8n can't connect to PostgreSQL

**Solution:**
1. Verify both containers are running: `docker-compose ps`
2. Check they're on the same network: `docker network inspect n8n-workflows_backend-net`
3. Use `postgres-db` as hostname in n8n credentials (not `localhost`)
4. Test manually: `docker exec n8n ping postgres-db`

### Data Persistence Issues

**Problem:** Data lost after restart

**Solution:**
```bash
# Verify volumes exist
docker volume ls | grep n8n

# Check volume mounts
docker inspect n8n | grep -A 10 Mounts
docker inspect postgres-db | grep -A 10 Mounts
```

## 📝 Adding New Workflows

To add a new workflow to this repository:

1. **Create a folder** with a descriptive name
2. **Export workflow** from n8n as JSON and place in the folder
3. **Create a README.md** with:
   - Overview of what the workflow does
   - Setup requirements
   - Configuration steps
   - Usage instructions
4. **Update root README** (this file) to list the new workflow
5. If the workflow needs additional services, consider adding them to `docker-compose.yaml`

## 🔄 Updating n8n

To update to the latest n8n version:

```bash
# Pull latest image
docker-compose pull n8n

# Restart with new image
docker-compose up -d n8n
```

Your workflows and credentials are preserved in the `n8n_data` volume.

## 💡 Tips

- **Workflow Versions:** Export workflows regularly and commit to git
- **Credentials:** Never commit credentials to git - use n8n's credential store
- **Testing:** Use n8n's manual execution for testing before activation
- **Backups:** Regularly backup the `n8n_data` and `n8n_workflows_postgres_data` volumes
- **Logs:** Check logs when troubleshooting: `docker-compose logs -f`

## 📚 Resources

- [n8n Documentation](https://docs.n8n.io)
- [n8n Community Forum](https://community.n8n.io)
- [n8n Workflow Templates](https://n8n.io/workflows)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

## 🤝 Contributing

When contributing new workflows:
1. Ensure they work with the existing infrastructure
2. Provide comprehensive documentation
3. Include example data if applicable
4. Test import/export functionality

## 📄 License

Each workflow may have its own license. See individual workflow directories for details.

---

**Need Help?** Check the workflow-specific README files in each directory for detailed setup instructions and troubleshooting.

