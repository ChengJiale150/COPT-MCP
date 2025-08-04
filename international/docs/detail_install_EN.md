# Quick One-Click Configuration with FastMCP

Using FastMCP to configure COPT-MCP is the quickest way. It supports one-click configuration for mainstream clients (such as Claude Desktop, Claude Code, Cursor, etc.). For details, please refer to the Integrations section of the official FastMCP documentation, for example, [configuring COPT-MCP for Claude Code](https://gofastmcp.com/integrations/claude-code).

# Manual Configuration of MCP Service

For other applications that do not support FastMCP one-click configuration (such as TRAE, Cherry Studio, etc.), you can manually configure it using the corresponding JSON format. The reference format is as follows:

```json
"COPT-MCP": {
    "command": "uv",
    "args": [
        "run",
        "--with", "fastmcp",
        "--with", "requests",
        "--with", "sqlite_vec",
        "fastmcp", "run",
        "your/path/to/COPT-MCP/server.py"
    ],
    "env": {},
    "transport": "stdio"
}
```

Now, please follow the steps below for configuration:

## Step 1: Confirm Your File Path

First, we need to confirm the file path of the MCP server entry file `server.py` to replace `"your/path/to/COPT-MCP/server.py"` in the reference configuration above.

### Windows 11

In `File Explorer`, find the `server.py` file in the COPT-MCP folder and press the shortcut `ctrl+shift+C` to copy the file path. A reference path is as follows:

```bash
C:\Users\username\Desktop\MCP\COPT-MCP\server.py
```

At this point, you need to replace the `\` in the path with `\\`. The final path is as follows:

```bash
C:\\Users\\username\\Desktop\\MCP\\COPT-MCP\\server.py
```

Finally, replace the file path in the reference JSON format with the copied path. An example is as follows:

```json
"COPT-MCP": {
    "command": "uv",
    "args": [
        "run",
        "--with", "fastmcp",
        "--with", "requests",
        "--with", "sqlite_vec",
        "fastmcp", "run",
        "C:\\Users\\username\\Desktop\\MCP\\COPT-MCP\\server.py"
    ],
    "env": {},
    "transport": "stdio"
}
```

### MacOS

In `Finder`, find the `server.py` file in the COPT-MCP folder and press the shortcut `option+command+c` to copy the file path. A reference path is as follows:

```bash
/Users/username/Documents/mcp/copt-mcp/server.py
```

Finally, replace the file path in the reference JSON format with the copied path. An example is as follows:

```json
"COPT-MCP": {
    "command": "uv",
    "args": [
        "run",
        "--with", "fastmcp",
        "--with", "requests",
        "--with", "sqlite_vec",
        "fastmcp", "run",
        "/Users/username/Documents/mcp/copt-mcp/server.py"
    ],
    "env": {},
    "transport": "stdio"
}
```

## Step 2: Set Necessary Environment Variables

Note: If you have already configured the corresponding API Key in `config.json` during the installation process, this step is not necessary and you can skip it.

If you configure the API Key according to the steps below, you also do not need to configure the corresponding API Key in `config.json`.

Please add the following content to `env`. Note that the `API_KEY` here is **shared** by the entire MCP and does not distinguish between embedding and re-ranking models:

```json
"env": {
    "API_KEY": "<your API Key>"
}
```

## Step 3: Add the MCP Service in the Corresponding Client

Next, add the MCP service in the MCP configuration file of the corresponding client.

### Cursor

In the upper right corner of Cursor, open `Cursor Settings` (the ⚙ icon), select `Tool & Integrations`, and click `New MCP Server` in `MCP Tools`. This will take you to the `mcp.json` file. The example result is as follows:

```json
{
  "mcpServers": {
    ...(existing MCP, empty if none)
  }
}
```

Add a `,` (comma) after the existing MCP (if any), and paste the completed JSON file. The final reference result is as follows:

```json
{
  "mcpServers": {
    ...(existing MCP, empty if none),
    "COPT-MCP": {
        ...(the content from above)
    }
  }
}
```

Finally, save and close the `mcp.json` file. Go back to `MCP Tools` to see if an MCP service named `COPT-MCP` has appeared. Wait a moment, and if the yellow light turns green, it means the MCP service has started successfully.

### Cherry Studio

Open the settings button (the ⚙ icon) on the side of the application, select `MCP Settings`, click `Import from JSON` in `Add Server`, and enter the following content:

```json
{
  "mcpServers": {
    "COPT-MCP": {
        ...(the content from above)
    }
  }
}
```

Click confirm, open the corresponding MCP server, and check if the connection is successful.

### Trae

Open the AI function management button (the ⚙ icon) on the side of the application, select `MCP`, click `Import from JSON` in `Manual Add`, and enter the following content:

```json
{
  "mcpServers": {
    "COPT-MCP": {
        ...(the content from above)
    }
  }
}
```

Click confirm, open the corresponding MCP server, and check if the connection is successful.

### Cline

At the bottom of the conversation, open `Manager MCP Servers` (📚), click the settings button (⚙ icon), select `Installed`, and click `Configure MCP Servers`. This will take you to the `cline_mcp_settings.json` file. The example result is as follows:

```json
{
  "mcpServers": {
    ...(existing MCP, empty if none)
  }
}
```

Add a `,` (comma) after the existing MCP (if any), and paste the completed JSON file. The final reference result is as follows:

```json
{
  "mcpServers": {
    ...(existing MCP, empty if none),
    "COPT-MCP": {
        ...(the content from above)
    }
  }
}
```

Finally, save and close the `cline_mcp_settings.json` file. Go back to see if an MCP service named `COPT-MCP` has appeared. Start it and wait a moment. If the light turns green, it means the MCP service has started successfully.

## Step 4: Test if the MCP Tool is Working Properly

Next, use the client's mode that supports MCP tool calls (such as Agent mode in Cursor) to test if the MCP tool is working properly.

### get_citation

Test input:

```
Get the reference citation format for COPT in Word
```

Expected output: COPT's Word format citation information.

### get_reference

Test input:

```
Get a reference example for solving a linear programming (LP) problem with the COPT Python interface
```

Expected output: A reference example for COPT's Python interface for LP problems.

### get_api_doc

Test input:

```
Get API interface information for adding linear constraints in matrix form with the COPT Python interface
```

Expected output: API interface information related to `Model.addMConstr()`.
