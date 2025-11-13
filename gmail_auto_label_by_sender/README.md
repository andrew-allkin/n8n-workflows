# Gmail Auto-Label by Sender (Regex Pattern Matching)

This n8n workflow automatically monitors your Gmail inbox and applies labels to incoming emails based on regex pattern matching against the sender's email address. All sender-to-label mappings are stored in PostgreSQL and can be easily updated by modifying an Excel file and re-running the setup script.

## Overview

When a new email arrives in your Gmail inbox, this workflow:
1. Captures the sender's email address
2. Queries a PostgreSQL database for regex pattern mappings
3. Matches the sender's email against all patterns (case-insensitive)
4. Automatically applies the corresponding Gmail label if a match is found
5. Skips labeling if no pattern matches

This is useful for automatically organizing emails from specific domains, companies, or sender patterns without manual intervention.

## Workflow Structure

The workflow consists of 6 nodes:

1. **Gmail Trigger** - Monitors Gmail inbox and triggers when new email is received
2. **Get Label Patterns** - Queries PostgreSQL database for all sender pattern mappings
3. **Match Sender Pattern** - Python code that matches sender email against regex patterns
4. **Label Found?** - IF node that checks whether a matching pattern was found
5. **Add Gmail Label** - Applies the matched label to the email (if match found)
6. **No Label Match** - NoOp node for emails that don't match any pattern

## Prerequisites

Before using this workflow, you need:

- An active n8n instance (self-hosted or cloud)
- Docker and Docker Compose installed (for PostgreSQL)
- A Gmail account
- Python 3.x installed (for database setup script)
- Gmail labels already created in your Gmail account

## Database Configuration

This workflow uses the shared PostgreSQL database defined in the root `docker-compose.yaml`:

- **Database Name:** `n8n_workflows_data`
- **Host:** `postgres-db` (inside Docker network) or `localhost` (external access)
- **Port:** `5432`
- **User:** `admin`
- **Password:** `adminpassword`

## Setup Instructions

### 1. Start the PostgreSQL Database

From the repository root directory:

```bash
docker-compose up -d
```

This will start both n8n and PostgreSQL services.

### 2. Set Up Python Environment

Navigate to the workflow directory and create a virtual environment:

```bash
cd gmail_auto_label_by_sender
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Your Email-to-Label Mappings

Edit the `email_labels.xlsx` file with your desired mappings:

- **Column A (Label):** The Gmail label to apply (must already exist in Gmail)
- **Column B (Email contains):** The regex pattern to match in sender's email

**Example mappings:**

| Label | Email contains |
|-------|----------------|
| Crossfit | peakgyms |
| Discovery | discovery |
| EasyEquities | easyequities |
| Investec | investec |
| Medical | @healthcareprovider\\.com$ |

**Regex Pattern Examples:**

- `investec` - Matches any email containing "investec" (e.g., alerts@investec.com, support@investec.co.za)
- `@company\\.com$` - Matches emails from exact domain "company.com"
- `^noreply@` - Matches any email starting with "noreply@"
- `.*newsletter.*@` - Matches emails with "newsletter" in the username part

### 4. Populate the Database

Run the setup script to create the table and insert your mappings:

```bash
python setup_database.py
```

**Output should look like:**

```
Dropping existing table if exists...
Creating sender_label_mapping table...
Reading email_labels.xlsx...
Inserting sender-label mappings...
  Added: 'peakgyms' -> 'Crossfit'
  Added: 'discovery' -> 'Discovery'
  Added: 'easyequities' -> 'EasyEquities'
  ...

Setup complete! 10 mappings inserted.
```

**Note:** You can update the Excel file at any time and re-run this script. It will drop and recreate the table with your updated mappings.

### 5. Configure Gmail Credentials

This workflow requires **Gmail OAuth2** credentials to monitor your inbox and apply labels.

#### Step-by-Step Credential Setup:

**A. Create Google Cloud Project & Enable Gmail API**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** > **Library**
4. Search for "Gmail API" and click **Enable**

**B. Create OAuth 2.0 Credentials**

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - User Type: **External** (or Internal if using Google Workspace)
   - Add your email as a test user
   - Required scopes: Add Gmail API scopes
4. For Application type, select **Web application**
5. Add authorized redirect URIs:
   - `http://localhost:5678/rest/oauth2-credential/callback` (for local n8n)
   - Or your n8n instance URL + `/rest/oauth2-credential/callback`
6. Save and copy your **Client ID** and **Client Secret**

**C. Add Credentials in n8n**

1. Open n8n (http://localhost:5678)
2. Go to **Settings** > **Credentials** > **New**
3. Search for "Gmail OAuth2"
4. Enter:
   - **Client ID:** (from Google Cloud Console)
   - **Client Secret:** (from Google Cloud Console)
5. Click **Connect my account** and authorize access
6. Ensure the following scopes are granted:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.modify`
   - `https://www.googleapis.com/auth/gmail.labels`

**D. Add PostgreSQL Credentials in n8n**

1. In n8n, go to **Settings** > **Credentials** > **New**
2. Search for "Postgres"
3. Enter the database details:
   - **Host:** `postgres-db` (if n8n is in Docker) or `localhost` (if external)
   - **Port:** `5432`
   - **Database:** `n8n_workflows_data`
   - **User:** `admin`
   - **Password:** `adminpassword`
   - **SSL:** Disabled
4. Test the connection and save

### 6. Create Gmail Labels

Before importing the workflow, ensure all labels referenced in your Excel file already exist in Gmail:

1. Open Gmail
2. Go to Settings > Labels
3. Create any missing labels (e.g., "Crossfit", "Discovery", "Investec", etc.)

**Important:** Gmail label names are case-sensitive. Ensure they match exactly what's in your Excel file.

### 7. Import the Workflow

1. Copy the contents of `n8n_workflow.json`
2. In n8n, click **Add workflow** > **Import from File**
3. Paste the workflow JSON

### 8. Update Workflow Credentials

After importing, you need to assign your credentials to the workflow nodes:

1. Open the **Gmail Trigger** node:
   - Select your Gmail OAuth2 credential
   - Save the node

2. Open the **Get Label Patterns** node:
   - Select your PostgreSQL credential
   - Save the node

3. Open the **Add Gmail Label** node:
   - Select your Gmail OAuth2 credential
   - Save the node

### 9. Activate the Workflow

1. Click the toggle at the top of the workflow to activate it
2. The workflow will now monitor your inbox continuously
3. Every new email will be processed automatically

## How It Works

### Database Schema

The workflow uses a simple table structure:

```sql
CREATE TABLE sender_label_mapping (
    id SERIAL PRIMARY KEY,
    pattern VARCHAR(255) NOT NULL,
    gmail_label VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Regex Matching Logic

The Python Code node performs case-insensitive regex matching:

```python
import re

sender_email = email_data.get('from', {}).get('address', '')

for pattern_row in patterns:
    pattern = pattern_row.get('pattern', '')
    label = pattern_row.get('gmail_label', '')
    
    if re.search(pattern, sender_email, re.IGNORECASE):
        matched_label = label
        break
```

**Pattern Matching Order:**
- Patterns are evaluated in the order they appear in the database (by ID)
- The first matching pattern wins
- If you want more specific patterns to take precedence, add them to the Excel file first

### Example Scenarios

**Scenario 1: Domain-wide matching**
- Pattern: `@investec`
- Matches: `alerts@investec.com`, `support@investec.co.za`, `john.doe@investec-bank.com`
- Result: All emails from any Investec domain get labeled "Investec"

**Scenario 2: Exact domain matching**
- Pattern: `@company\\.com$`
- Matches: `info@company.com`, `support@company.com`
- Does NOT match: `info@company.co.uk`, `info@company.com.au`

**Scenario 3: Keyword in email**
- Pattern: `newsletter`
- Matches: `newsletter@site.com`, `no-reply.newsletter@marketing.com`

## Updating Mappings

To update your email-to-label mappings:

1. Edit the `email_labels.xlsx` file
2. Add, remove, or modify rows as needed
3. Re-run the setup script:

```bash
cd gmail_auto_label_by_sender
source venv/bin/activate
python setup_database.py
```

4. The workflow will automatically use the updated mappings for new emails
5. No need to restart the workflow or n8n

## Required n8n Credentials

This workflow requires the following credentials to be configured in n8n:

1. **Gmail OAuth2** - For monitoring inbox and applying labels
   - Scopes needed: `gmail.readonly`, `gmail.modify`, `gmail.labels`
   - Used by: Gmail Trigger node, Add Gmail Label node

2. **PostgreSQL** - Connection to the shared database
   - Host: postgres-db (or localhost)
   - Port: 5432
   - Database: n8n_workflows_data
   - User: admin
   - Password: adminpassword
   - Used by: Get Label Patterns node

## Troubleshooting

### Workflow Not Triggering

- **Issue:** Workflow doesn't respond to new emails
- **Solution:** 
  - Ensure the workflow is activated (toggle switch is ON)
  - Check that Gmail OAuth2 credentials are valid
  - Verify Gmail API is enabled in Google Cloud Console
  - Check n8n execution logs for errors

### Labels Not Being Applied

- **Issue:** Emails match patterns but labels aren't added
- **Solution:**
  - Ensure the labels exist in Gmail (create them manually first)
  - Check that label names in Excel exactly match Gmail labels (case-sensitive)
  - Verify Gmail OAuth2 has the `gmail.modify` scope
  - Check n8n execution logs for the specific email

### Pattern Not Matching

- **Issue:** Expected emails aren't getting labeled
- **Solution:**
  - Test your regex pattern using an online regex tester
  - Check the sender email format (use Gmail's "Show original" to see the exact from address)
  - Remember: matching is case-insensitive
  - Escape special regex characters (e.g., use `\\.` for a literal dot)

### Database Connection Errors

- **Issue:** "Get Label Patterns" node fails
- **Solution:**
  - Ensure PostgreSQL container is running: `docker-compose ps`
  - Verify database credentials in n8n match docker-compose.yaml
  - Check if the table exists: Run `setup_database.py` again
  - If n8n is external to Docker, use `localhost` as host

### Python Script Errors

- **Issue:** setup_database.py fails
- **Solution:**
  - Ensure virtual environment is activated
  - Verify all dependencies are installed: `pip install -r requirements.txt`
  - Check that PostgreSQL is running and accessible
  - Verify the `email_labels.xlsx` file exists and has data

## Performance Notes

- The workflow executes for EVERY incoming email
- Database query is lightweight (typically < 10ms)
- Regex matching is fast for reasonable pattern counts (< 100 patterns)
- No external API calls except to Gmail
- Workflow typically completes in under 1 second per email

## Security Considerations

- Database credentials are hardcoded for development/personal use
- For production, consider using environment variables
- Gmail OAuth2 tokens are stored securely by n8n
- Regex patterns are not sanitized - be careful with user input if allowing external pattern sources
- The workflow has full Gmail access - restrict n8n instance access appropriately

## Limitations

- Gmail labels must be pre-created manually
- Only matches against sender's email address (not subject, body, etc.)
- First matching pattern wins (no multi-label support)
- Requires n8n to be running continuously for real-time processing
- Gmail API has rate limits (typically not an issue for personal use)

## Advanced Customization

### Adding Multiple Labels

To apply multiple labels to a single email, modify the Python code to return an array of labels instead of a single match.

### Matching on Subject or Body

To match patterns against email subject or body, modify the Python code to include additional fields from the Gmail trigger output.

### Priority-Based Matching

Add a `priority` column to the database table and modify the SQL query to order by priority.

### Logging Matched Emails

Add a logging node after the "Add Gmail Label" node to track which emails were labeled.

## File Structure

```
gmail_auto_label_by_sender/
├── README.md                    # This file
├── n8n_workflow.json            # n8n workflow (import this)
├── email_labels.xlsx            # Your sender-to-label mappings
├── setup_database.py            # Database setup script
├── requirements.txt             # Python dependencies
└── venv/                        # Virtual environment (created by you)
```

## Support

For issues related to:
- **n8n platform:** See [n8n documentation](https://docs.n8n.io/)
- **Gmail API:** See [Gmail API documentation](https://developers.google.com/gmail/api)
- **PostgreSQL:** See [PostgreSQL documentation](https://www.postgresql.org/docs/)
- **Regex patterns:** Test at [regex101.com](https://regex101.com/)

## Future Enhancements

Potential improvements for this workflow:
- Web UI for managing patterns (instead of Excel file)
- Multi-label support (apply multiple labels per email)
- Pattern testing tool (dry-run mode)
- Email notification for unmatched senders
- Pattern usage statistics
- Automatic label creation if it doesn't exist


