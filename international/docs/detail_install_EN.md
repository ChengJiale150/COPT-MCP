# Quick One-Click Configuration with FastMCP

Using FastMCP is the quickest way to configure COPT-MCP. It supports one-click configuration for mainstream clients (such as Claude Desktop, Claude Code, Cursor, etc.). For details, please refer to the Integrations section of the official FastMCP documentation, for example, [configuring COPT-MCP for Claude Code](https://gofastmcp.com/integrations/claude-code).

# Manual MCP Service Configuration

For other applications that do not support FastMCP's one-click configuration (such as TRAE, Cherry Studio, etc.), you can manually configure it using the corresponding JSON format. The reference format is as follows:

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

Now please follow the steps below for configuration:

## Step 1: Confirm Your File Path

First, we need to confirm the file path of the MCP server entry file `server.py` to replace `"your/path/to/COPT-MCP/server.py"` in the reference configuration above.

### Windows 11

...

### macOS

In `Finder`, locate the `server.py` file in the COPT-MCP folder, and press `option+command+c` to copy the file path. A reference path is as follows:

```bash
/Users/username/Documents/mcp/copt-mcp/server.py
```

Finally, replace the file path in the reference JSON format with the copied path. Here is an example:

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

Note: If you have already configured the corresponding API Key in `config.json` during the installation process, this step is not necessary and can be skipped.

If you configure the API Key according to the following steps, you also do not need to configure the corresponding API Key in `config.json`.

Please add the following content in `env`. Note that the `API_KEY` here is **shared** by the entire MCP and does not distinguish between embedding and reranking models:

```json
"env":{
    "API_KEY" : "<your API Key>"
}
```

## Step 3: Add the MCP Service in the Corresponding Client

Next, add the MCP service in the MCP configuration file of the corresponding client.

### Cursor

In the upper right corner of Cursor, open `Cursor Settings` (the ⚙ icon), select `Tool & Integrations`, and click `New MCP Server` in `MCP Tools`. This will take you to the `mcp.json` file. The example result is as follows:

```json
{
  "mcpServers": {
    ...(existing MCPs, if any)
  }
}
```

Add a `,` (comma) after the existing MCPs (if there are none, no need to add it), and then paste the completed JSON file. The final reference result is as follows:

```json
{
  "mcpServers": {
    ...(existing MCPs, if any),
    "COPT-MCP" : {
        ...(the specific content from above)
    }
  }
}
```

Finally, save and close the `mcp.json` file. Go back and check if an MCP service named `COPT-MCP` appears in `MCP Tools`. Wait for a moment, and if the yellow light turns green, it means the MCP service has started successfully.

## Step 4: Test if the MCP Tools are Running Correctly

Next, use the client's mode that supports MCP tool calls (such as Agent mode in Cursor) to test whether the MCP tools are running correctly.

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

Expected output: A reference example for the COPT Python interface for LP problems.

### get_api_doc

Test input:

```
Get API interface information for adding linear constraints in matrix form with the COPT Python interface
```

Expected output: API interface information for `Model.addMConstr()`.
