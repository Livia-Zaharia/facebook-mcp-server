# Just_Facebook MCP Server

This project is a **Model Context Protocol (MCP)** server for automating and managing interactions on a **Facebook Page** using the Facebook Graph API. It provides tools to create posts, moderate comments, fetch post insights, and filter negative feedback — ready to plug into Claude or any other LLM-based agent.

> Originally developed from `@HagaiHen/facebook-mcp-server`, this version is intended for packaging and distribution via PyPI.

---

## 🤖 What Is This?

This MCP provides a suite of AI-callable tools that connect directly to a Facebook Page, abstracting common API operations as LLM-friendly functions.

### ✅ Benefits

- Empowers **social media managers** to automate moderation and analytics.
- Seamlessly integrates with **any Agent client**.
- Enables fine-grained control over Facebook content from natural language.

---

## 📦 Features

| Tool | Description |
|----------------------------------|---------------------------------------------------------------------|
| `post_to_facebook` | Create a new Facebook post with a message. |
| `reply_to_comment` | Reply to a specific comment on a post. |
| `get_page_posts` | Retrieve recent posts from the Page. |
| `get_post_comments` | Fetch comments on a given post. |
| `delete_post` | Delete a specific post by ID. |
| `delete_comment` | Delete a specific comment by ID. |
| `delete_comment_from_post` | Alias for deleting a comment from a specific post. |
| `filter_negative_comments` | Filter out comments with negative sentiment keywords. |
| `get_number_of_comments` | Count the number of comments on a post. |
| `get_number_of_likes` | Count the number of likes on a post. |
| `get_post_impressions` | Get total impressions on a post. |
| `get_post_impressions_unique` | Get number of unique users who saw the post. |
| `get_post_impressions_paid` | Get number of paid impressions on the post. |
| `get_post_impressions_organic` | Get number of organic impressions on the post. |
| `get_post_engaged_users` | Get number of users who engaged with the post. |
| `get_post_clicks` | Get number of clicks on the post. |
| `get_post_reactions_like_total` | Get total number of 'Like' reactions. |
| `get_post_top_commenters` | Get the top commenters on a post. |
| `post_image_to_facebook` | Post an image with a caption to the Facebook page. |
| `send_dm_to_user` | Send a direct message to a user. |
| `update_post` | Updates an existing post's message. |
| `schedule_post` | Schedule a post for future publication. |
| `get_page_fan_count` | Retrieve the total number of Page fans. |
| `get_post_share_count` | Get the number of shares on a post. |

---

## 🚀 Setup & Installation

### 1. Prerequisites

This project requires **Python 3.10+** and **uv** (a fast Python package manager).

To install `uv`, run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
### 2. Clone the Repository

### 3. 🛠️ Install Dependencies
Use the uv tool with pyproject.toml:
```bash
# Install all dependencies and create a virtual environment
uv sync

# For development (includes testing and linting tools)
uv sync --dev
```
### 4. Set Up Environment
Create a .env file in the root directory and add your Facebook Page credentials:

```env
FACEBOOK_ACCESS_TOKEN=your_facebook_page_access_token
FACEBOOK_PAGE_ID=your_page_id
```

**Getting Your Facebook Credentials**

  1. Log into Facebook for Developers

  2. Choose Developer as your use case.

  3. Create a new app.

  4. In the app dashboard, go to Customize Use Case and select all options.

  5. Navigate to Tools → Graph API Explorer.

  6. First create a User Access Token — make sure to:

        *Select all required permissions

        *Associate it with your app

  7. Then generate a Page Access Token (this will inherit the permissions).

  8. Save the Page Access Token and use it in the .env file.


To find your Page ID:

  Go to your Facebook Page → About → Scroll down to view the ID

### ⏰ Important: Facebook API Token Limitations

**Facebook access tokens have limited lifespans** and will expire, causing API calls to fail. Understanding these limitations is crucial for maintaining your MCP server.

#### **Token Types & Lifespans:**

| Token Type | Lifespan | Use Case |
|------------|----------|----------|
| **Short-lived User Token** | 1-2 hours | Testing only |
| **Long-lived User Token** | 60 days | Development |
| **Short-lived Page Token** | 1-2 hours | Testing only |
| **Long-lived Page Token** | 60 days | **Recommended for MCP** |
| **System User Token** | No expiration* | Production apps |

#### **When Tokens Expire:**
- ❌ All MCP tools will return `OAuthException` errors
- ❌ Error message: "Session has expired"
- ❌ Error codes: 190 (expired token) or 463 (session expired)

#### **Automatic Token Refresh:**
We provide a script to easily generate long-lived tokens (60 days):

```bash
uv run python scripts/refresh_facebook_token.py
```

This script will:
- ✅ Guide you through token generation
- ✅ Exchange short-lived for long-lived tokens
- ✅ Update your `.env` file automatically
- ✅ Validate the new token

#### **Best Practices:**
- 🔄 **Refresh tokens every 50 days** to avoid expiration
- 📅 **Set calendar reminders** for token renewal
- 🤖 **Use long-lived Page tokens** for development
- 🏢 **Consider System User tokens** for production

#### **Troubleshooting Token Issues:**
```bash
# Check if your token is expired
uv run python -c "
from just_facebook_mcp.manager import Manager
manager = Manager()
try:
    result = manager.get_page_fan_count()
    print('✅ Token is working')
except Exception as e:
    print(f'❌ Token error: {e}')
"
```

### 5. 🏃‍♂️ Running the Server
```bash
# Option 1: Using the script entry point (recommended)
uv run just_facebook_mcp

# Option 2: Run the Python module directly
uv run python -m just_facebook_mcp.server

# Option 3: Activate virtual environment first
source .venv/bin/activate
python -m just_facebook_mcp.server
```

### 🧩 Using with Claude Desktop
To integrate with Claude Desktop:

  1. Open Claude Desktop

  2. Go to Settings → Developer → Edit Config

Add the following to your MCP configuration:

**Option 1: Using the package entry point (recommended)**
```json
{
  "mcpServers": {
    "just_facebook_mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/just_facebook_mcp-server",
        "just_facebook_mcp"
      ]
    }
  }
}
```

**Option 2: Using Python module**
```json
{
  "mcpServers": {
    "just_facebook_mcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/absolute/path/to/just_facebook_mcp-server",
        "python",
        "-m",
        "just_facebook_mcp.server"
      ]
    }
  }
}
```

**Option 3: If installed via pip**
```json
{
  "mcpServers": {
    "just_facebook_mcp": {
      "command": "just_facebook_mcp"
    }
  }
}
```

Replace `/absolute/path/to/just_facebook_mcp-server` with your actual project path.

### 🔧 Development
**Running Tests**
```bash
uv run pytest
```
**Code Formatting**
```bash
uv run black .
```
**Type Checking**
```bash
uv run mypy .
```

### Install Development Dependencies
```bash
uv sync --dev
```

### ✅ You're Ready to Go!
Your Facebook MCP server is now configured and ready to power Claude Desktop! You can:

✨ Create posts through natural language

📊 Get analytics and insights

💬 Moderate comments automatically

🎯 Schedule content

📈 Track engagement metrics

### 🤝 Contributing
Contributions, issues, and feature requests are welcome!

📄 License
This project is licensed under the MIT License.
See the LICENSE file for details.