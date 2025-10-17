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

You need to set up Google OAuth2 credentials in n8n:

1. Go to **Settings** > **Credentials** in your n8n instance
2. Click **Create New Credential**
3. Select **Google OAuth2 API**
4. Follow these steps:
   - Create a project in [Google Cloud Console](https://console.cloud.google.com/)
   - Enable the **Gmail API** for your project
   - Create OAuth 2.0 credentials (Client ID and Client Secret)
   - Add authorized redirect URIs (your n8n OAuth callback URL)
   - Copy the Client ID and Client Secret to n8n
   - Authorize access to your Gmail account

For detailed instructions, refer to the [n8n Google credentials documentation](https://docs.n8n.io/integrations/builtin/credentials/google/).

### 2. Import the Workflow

1. Copy the contents of `Gmail Date Range Delete.json`
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

