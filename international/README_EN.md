<div align="center">

<!-- omit in toc -->

**ATTENTION: The English version is translated by AI, The original version is [Chinese Version](../README.md)**

# COPT-MCP 🚀

**An MCP service for the COPT solver developed by Cardinal Operations, providing documents and examples specifically designed for large language models**

*Developed by [ChengJiale150](https://github.com/ChengJiale150)*

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![COPT](https://img.shields.io/badge/COPT-7.2.9+-green.svg)](https://www.cardopt.com/solver)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.10.6+-orange.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](../../LICENSE)
[![Version](https://img.shields.io/badge/version-v0.3.3-blue.svg)](https://github.com/ChengJiale150/COPT-MCP)

English | [中文](./../README.md)

</div>

---

## 📖 Table of Contents

- [Project Introduction](#-project-introduction)
- [Features](#-features)
- [Installation and Usage](#-installation-and-usage)
- [Detailed Introduction](#-detailed-introduction)
- [Contribution Guide](#-contribution-guide)
- [Update Log](#-update-log)
- [Acknowledgments](#-acknowledgments)
- [Contact Us](#-contact-us)

## 🎯 Project Introduction

COPT-MCP is a service based on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) that provides detailed documentation and examples for the COPT solver's interfaces to MCP-supported clients. It aims to adapt the COPT solver's documentation for AI, reduce model hallucinations, and improve the accuracy of large models using the COPT solver.

### Why COPT-MCP is Needed

The COPT solver is an efficient mathematical programming solver for large-scale optimization problems, supporting a variety of optimization problems. It is an excellent choice for solving complex operations research problems. However, there is limited public information about the COPT solver, which can lead to model hallucinations when large models try to use it, affecting the user experience. Directly inputting COPT's official documentation is also problematic because it is too long, far exceeding the context length limit of models, and excessive irrelevant content can interfere with the model's understanding, leading to context loss.

COPT-MCP aims to provide large models with the minimum viable documentation and examples for the COPT solver's interfaces. By carefully organizing and selecting the documentation content, it adapts the COPT solver's documentation for AI, outputs the minimum necessary information, reduces model hallucinations, and improves the accuracy of large models using the COPT solver's interfaces.

### Advantages of COPT-MCP

- 🔧 **Multi-type Support**: Supports various planning problems and programming languages.
- 📚 **Rich Example Library**: Provides detailed code examples and API descriptions.
- 📖 **Academic Citation Support**: Provides citation templates in Word and BibTeX formats.
- 🔌 **MCP Protocol**: Easily integrates with various large models and Agents via the MCP protocol.
- 🚀 **Lightweight Deployment**: No need to install extra software, only a Python virtual environment is required.
- 📝 **Chinese Documentation**: Complete Chinese documentation and example descriptions.

## ✨ Features

| Type | Name | Description |
|:----:|:-------------:|:----------------------:|
| Tool | `get_citation` | Get the citation format for COPT. |
| Tool | `get_reference` | Get reference examples for specified programming language interfaces corresponding to problems. |
| Tool | `get_api_doc` | Return the most similar API documentation based on a query. |

## 🛠️ Installation and Usage

### System Requirements

- Python 3.12+
- FastMCP
- uv (recommended for version management)

### Installation Steps

1.  **Clone the project**

    ```bash
    git clone https://github.com/ChengJiale150/COPT-MCP.git
    cd COPT-MCP
    ```

2.  **Install dependencies**

    ```bash
    pip install uv
    uv sync
    ```

3.  **Configure environment variables**

    Configure the necessary API_KEY for the model in the `config.json` file. By default, it uses models from [SiliconFlow](https://cloud.siliconflow.cn/i/5JAHVbNN).

    ```json
    "embedding": {
        "url": "https://api.siliconflow.cn/v1/embeddings",
        "api_key": "<your api key>"
    },
    "reranker": {
        "url": "https://api.siliconflow.cn/v1/rerank",
        "api_key": "<your api key>"
    }
    ```

4.  **Run the MCP service**

    ```bash
    uv run fastmcp run server.py
    ```

### Integration in a Client

You can use FastMCP to automatically integrate this MCP service. For details, see the [MCP integration documentation](https://gofastmcp.com/integrations/anthropic). Here is an example of integration in Cursor using FastMCP:

```bash
fastmcp install cursor server.py
```

Alternatively, you can manually add it to the configuration file of an MCP-supported client:

```json
{
  "mcpServers": {
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
  }
}
```

For other configurations, please refer to the [detailed configuration guide](./docs/detail_install_EN.md).

## 🔧 Detailed Introduction

COPT-MCP provides three core tools to help AI assistants better provide optimization solving services to users.

### Get Citation Format

**Tool Name**: `get_citation`

**Function**: Get the academic citation format for the COPT solver, supporting Word and BibTeX formats.

**Parameters**:

-   `citation_type` (str): Citation type
    -   `"word"`: Citation format for Word documents
    -   `"bibtex"`: Citation format for BibTeX files

**Returns**: Citation text in the corresponding format.

**Usage**:

-   When a user needs to cite the COPT solver in their academic paper, the AI assistant can call the `get_citation` tool with the `"word"` or `"bibtex"` parameter to get the citation text in the corresponding format.
-   The citation text for the corresponding format is located in the `resource/citation` folder, which you can view and modify yourself.

### Get Reference Example

**Tool Name**: `get_reference`

**Function**: Get reference example code for a specified problem type and programming language, including detailed mathematical modeling instructions and code comments.

**Parameters**:

-   `problem_type` (str): Type of problem to be solved (currently only the following types are supported)
    -   `"LP"`: Linear Programming
    -   `"MIP"`: Mixed Integer Programming
    -   `"SOCP"`: Second-Order Cone Programming
-   `language` (str): API interface language (currently only the following types are supported)
    -   `"Python"`: Python interface

**Returns**: A Markdown document containing mathematical definitions, code examples, and detailed comments.

**Usage**:

-   When a user needs to solve a problem related to the COPT solver, the AI assistant will first call the `get_reference` tool with the `problem_type` and `language` parameters to get a reference example for the corresponding problem. This leverages the large model's excellent Few-Shot learning ability to reduce model hallucinations and improve the model's accuracy in using the COPT solver.
-   The reference example code is located in the `resource/example/{problem_type}/{language}.md` file. You can view and modify it yourself, and add more examples as needed.

### Get API Documentation

**Tool Name**: `get_api_doc`

**Function**: Return the most similar API documentation based on a query.

**Parameters**:

-   `instructions` (str): Query instruction, supports natural language descriptions and code snippet queries. Reference query instructions are as follows:
    -   `"name"`: Query API name, such as "Model.addConstr()"/"Envr()"
    -   `"description"`: Query requirement description, such as "add a set of linear constraints using matrix modeling"
-   `language` (str): API interface language (currently only the following types are supported)
    -   `"Python"`: Python interface
-   `domain` (str): The field corresponding to the query instruction, the currently supported domains are as follows:
    -   `"name"`: Query API name
    -   `"description"`: Query API description
-   `recall_num` (int): Number of recalled items, default is 10, maximum is 25.
-   `return_num` (int): Final number of returned items after re-ranking, default is 3, maximum is 8.

**Returns**: A Markdown document containing the API name, description, and example code.

**Usage**:

-   When a large model is unclear about the relevant API of the COPT solver, it will first call the `get_api_doc` tool with the `instructions`, `language`, `domain`, and `recall_num` parameters to get the documentation for the corresponding API.
-   The data comes from the official documentation of the COPT solver. The most similar API documentation is recalled through an embedding model and returned to the large model after re-ranking.
-   The data is stored in the `resource/api_doc/{language}` folder, in JSON format (raw data for user viewing) and db format (for model querying).
-   Due to the large number of API documents, it is not yet complete. The completed API documents are detailed in the `TODO.md` file in the `resource/api_doc/{language}` folder. It will be continuously updated, and contributions of more API documents are welcome.

## 🤝 Contribution Guide

We welcome community contributions! If you would like to contribute to the COPT-MCP project, please:

1.  Fork this repository
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

### Types of Contributions

-   🐛 Bug fixes
-   📝 Improvements to existing features
-   ✨ New feature development
-   📚 Documentation improvements
-   🧪 Adding test cases
-   🌍 Internationalization support

## 📝 Update Log

The following log only records a summary of major version updates. For details, please see the [Update Log](./docs/update_info_EN.md).

### Latest Information

-   **v0.3.0** (2025-08-04) Modified the documentation structure and added detailed MCP installation support.

### Historical Information

-   **v0.1.0** (2025-07-29) Initial version, completed the rapid integration and use of COPT-MCP.
-   **v0.2.0** (2025-07-31) Completed all documentation for the Python API interface, and added a re-ranking function to `get_api_doc`.
-   **v0.3.0** (2025-08-04) Modified the documentation structure and added detailed MCP installation support.

## 🤗 Acknowledgments

The establishment and completion of this project would not have been possible without the selfless help of the following individuals and organizations. Without them, COPT-MCP would not exist. I would like to express my sincere thanks:

-   [Cardinal Operations](https://www.cardopt.com/): Thanks to Cardinal Operations for developing the COPT solver and providing detailed official documentation. Without the COPT solver, there would be no COPT-MCP.
-   [FastMCP](https://gofastmcp.com/): Thanks to the developers of FastMCP. Without FastMCP, there would be no rapid integration of COPT-MCP.
-   [Claude Code](https://github.com/anthropics/claude-code): Thanks to Claude Code, it is the most powerful AI programming assistant I have ever used. Without it, there would be no rapid development of COPT-MCP.
-   [Cursor](https://www.cursor.com/): Thanks to Cursor, it is the primary author of this README. Without it, the documentation for COPT-MCP would not have been completed so quickly.

In addition, I would also like to thank the experts in the Cardinal COPT Solver Exchange Group 2 (QQ group number: 142636109). Your discussions have given me a lot of inspiration and a deeper understanding of the COPT solver. I express my heartfelt thanks here.

Finally, thank you for using COPT-MCP. If you have any questions or suggestions, please feel free to contact me, and I will reply as soon as possible.

## 📞 Contact Us

-   Personal Email: cjl3473383542@163.com
-   University Email: 2023110603@stu.sufe.edu.cn (both are fine)
-   GitHub Issues: [Submit an issue](https://github.com/ChengJiale150/COPT-MCP/issues)

### Related Links

-   [COPT Solver](https://www.cardopt.com/solver)
-   [COPT Documentation](https://pub.shanshu.ai/cardinalsite_v2/video/20250623/copt-userguide_cn.pdf)
-   [FastMCP](https://gofastmcp.com)
-   [MCP Protocol](https://modelcontextprotocol.io/)

---

<div align="center">

**If this project is helpful to you, please give us a ⭐️**

Made with ❤️ by [ChengJiale150](https://github.com/ChengJiale150)

</div>
