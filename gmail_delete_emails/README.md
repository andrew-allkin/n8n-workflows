# Gmail Date Range Delete Workflow

This n8n workflow allows you to bulk delete Gmail messages within a specific date range while preserving emails with important labels.

## Overview

The workflow retrieves and deletes Gmail messages that fall within a specified date range, automatically excluding emails tagged with specific labels (like bank statements, medical records, event information, etc.). This is useful for cleaning up your inbox while protecting important correspondence.

## Workflow Structure

The workflow consists of 5 nodes:

1. **Manual Trigger** - Initiates the workflow when you click "Test workflow"
2. **Set Date Parameters** - Defines the date range for deletion
3. **Get Gmail Messages** - Retrieves messages matching the criteria
4. **Check If Emails Exist** - Validates that emails were found before attempting deletion
5. **Delete Emails** - Moves matching emails to trash

## Prerequisites

Before using this workflow, you need:

- An active n8n instance (self-hosted or cloud)
- A Gmail account
- Gmail OAuth2 credentials configured in n8n

## Setup Instructions

### 1. Configure Gmail Credentials

This workflow requires **Gmail OAuth2** credentials to access your Gmail account and perform delete operations.

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
   - Select **External** user type (unless you have a Google Workspace)
   - Fill in app name, user support email, and developer contact
   - Add scopes: `https://www.googleapis.com/auth/gmail.modify` (or broader Gmail scopes)
   - Add your email as a test user
   - Save and continue
4. Back on the Credentials page, click **Create Credentials** > **OAuth client ID**
5. Select **Web application** as application type
6. Add authorized redirect URIs:
   - For local n8n: `http://localhost:5678/rest/oauth2-credential/callback`
   - For cloud n8n: `https://your-n8n-url.com/rest/oauth2-credential/callback`
7. Click **Create** and save your **Client ID** and **Client Secret**

**C. Configure in n8n**

1. Open n8n at http://localhost:5678
2. Go to **Settings** > **Credentials** (or click the credentials icon in the sidebar)
3. Click **Add Credential** and search for **Google OAuth2 API**
4. Enter your credentials:
   - **Client ID**: Paste from Google Cloud Console
   - **Client Secret**: Paste from Google Cloud Console
   - **Auth URI**: `https://accounts.google.com/o/oauth2/auth` (default)
   - **Token URI**: `https://oauth2.googleapis.com/token` (default)
   - **Scopes**: `https://www.googleapis.com/auth/gmail.modify` (or use the default)
5. Click **Connect my account** - this will open a Google authorization page
6. Select your Google account and grant permissions to n8n
7. Once authorized, you'll be redirected back to n8n
8. Give your credential a memorable name (e.g., "Gmail account") and click **Save**

**D. Verify Connection**

Your credential should now show as connected with a green checkmark. If you see a red warning, check that:
- The Gmail API is enabled in Google Cloud Console
- Your redirect URI matches exactly (including http/https)
- You've added your email as a test user if app is not published

**Troubleshooting:**
- **"Access blocked: This app's request is invalid"**: Check that your redirect URI in Google Cloud Console matches your n8n callback URL exactly
- **"Error 403: access_denied"**: Ensure Gmail API is enabled and your email is added as a test user
- **Token expired**: Re-authenticate by editing the credential and clicking "Connect my account" again

For more details, see the [official n8n Google credentials documentation](https://docs.n8n.io/integrations/builtin/credentials/google/).

### 2. Import the Workflow

1. Copy the contents of `n8n_workflow.json`
2. In n8n, click **Add workflow** > **Import from File** or **Import from URL**
3. Paste the workflow JSON

### 3. Update Credentials

After importing:

1. Open the **Get Gmail Messages** node
2. Select or create your Gmail OAuth2 credential
3. Open the **Delete Emails** node
4. Select the same Gmail OAuth2 credential

### 4. Configure Date Range

Open the **Set Date Parameters** node and modify the date values:

```
startDate: "2024-06-30"  // Start of date range (YYYY-MM-DD)
endDate: "2024-09-01"    // End of date range (YYYY-MM-DD)
```

**Important:** The workflow will delete emails received between these dates (inclusive).

### 5. Customize Label Filters (Optional)

The workflow is configured to **exclude** emails with the following labels:

- Crossfit
- Discovery
- EasyEquities
- Events 2025
- Gap Cover
- Genesis
- Investec
- Medical
- Online Orders
- Personal
- PPS Income Protection
- Sygnia
- TymeBank

To modify these exclusions:

1. Open the **Get Gmail Messages** node
2. Edit the **Query** field under **Filters**
3. The format is: `-label:LabelName` (the minus sign means "exclude")
4. Add or remove labels as needed

## How to Use

1. **Configure the date range** in the "Set Date Parameters" node
2. **Review the label filters** to ensure important emails are protected
3. Click **Test workflow** to execute
4. The workflow will:
   - Retrieve all messages in the date range (excluding labeled emails)
   - Check if any messages were found
   - Move matching messages to trash
   - Return the count of deleted messages

## Safety Features

- **Label Protection**: Emails with specific labels are automatically excluded
- **Date Range Validation**: Only emails within the specified range are affected
- **Existence Check**: The workflow verifies emails exist before attempting deletion
- **Trash (Not Permanent Delete)**: Emails are moved to trash, not permanently deleted, giving you a recovery window

## Important Notes

⚠️ **Warning**: This workflow will delete emails matching your criteria. Always:

1. **Test with a narrow date range first** (e.g., 1-2 days)
2. **Review your label filters** to ensure important emails are protected
3. **Check your Gmail trash** after execution to verify correct emails were deleted
4. Remember that Gmail keeps emails in trash for 30 days before permanent deletion

## Workflow Validation

The workflow has been validated and is working correctly:

- ✅ All nodes properly configured
- ✅ Connections valid
- ✅ Expressions validated
- ⚠️ Consider adding error handling for production use

## Gmail API Operations Used

- **Message: Get Many** - Retrieves messages based on filters
- **Message: Delete** - Moves messages to trash

## Troubleshooting

### No emails are being deleted

- Verify the date range is correct
- Check that you have emails in that date range without the excluded labels
- Ensure credentials are properly authenticated

### Authentication errors

- Re-authenticate your Gmail OAuth2 credentials
- Verify the Gmail API is enabled in Google Cloud Console
- Check that your OAuth consent screen is configured correctly

### Rate limiting

- Gmail API has rate limits; if deleting many emails, you may need to add delays
- Consider using the n8n "Wait" node or "SplitInBatches" node for large deletion jobs

## Resources

- [n8n Gmail Node Documentation](https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.gmail/)
- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Google OAuth2 Setup Guide](https://docs.n8n.io/integrations/builtin/credentials/google/)

## License

This workflow is provided as-is for personal or commercial use.

