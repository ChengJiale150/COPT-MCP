<div align="center">

<!-- omit in toc -->

**ATTENTION: The English version is translated by AI, The original version is [Chinese Version](../README.md)**

# COPT-MCP 🚀

**An MCP service for the COPT solver developed by Shanshu Technology, providing documentation and examples designed for large language models.**

*Developed by [ChengJiale150](https://github.com/ChengJiale150)*

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![COPT](https://img.shields.io/badge/COPT-7.2.9+-green.svg)](https://www.cardopt.com/solver)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.10.6+-orange.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](../LICENSE)
[![Version](https://img.shields.io/badge/version-v0.3.0-blue.svg)](https://github.com/ChengJiale150/COPT-MCP)

English | [中文](../README.md)

</div>

---

## 📖 Table of Contents

- [Project Introduction](#-project-introduction)
- [Features](#-features)
- [Installation and Usage](#-installation-and-usage)
- [Detailed Introduction](#-detailed-introduction)
- [Contribution Guide](#-contribution-guide)
- [Changelog](#-changelog)
- [Acknowledgements](#-acknowledgements)
- [Contact Us](#-contact-us)

## 🎯 Project Introduction

COPT-MCP is a service based on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), providing detailed documentation and examples of COPT solver interfaces for MCP-supported clients. It aims to adapt the COPT solver's documentation for AI, reducing model hallucinations and improving the accuracy of large models when using the COPT solver.

### Why COPT-MCP?

The COPT solver is an efficient mathematical programming solver for large-scale optimization problems, supporting various problem types, making it an excellent choice for solving complex operations research problems. However, there is limited public information about the COPT solver, which can lead to hallucinations when large models attempt to use it, affecting the user experience. Directly inputting the official COPT documentation is also problematic due to its length, which often exceeds the context length limits of models. Furthermore, excessive irrelevant content can impair the model's understanding and lead to context loss.

COPT-MCP aims to provide large models with minimal viable documentation and examples for the COPT solver's interfaces. By carefully organizing and selecting content, it adapts the documentation for AI, outputting only the necessary information to reduce model hallucinations and enhance the accuracy of large models when using the COPT solver's interfaces.

### Advantages of COPT-MCP

- 🔧 **Multi-type Support**: Supports various optimization problems and programming languages.
- 📚 **Rich Example Library**: Provides detailed code examples and API descriptions.
- 📖 **Academic Citation Support**: Offers citation templates in Word and BibTeX formats.
- 🔌 **MCP Protocol**: Facilitates easy integration with various large models and Agents via the MCP protocol.
- 🚀 **Lightweight Deployment**: No need to install extra software; only a Python virtual environment is required.
- 📝 **English Documentation**: Complete English documentation and example descriptions.

## ✨ Features

| Type   | Name            | Description                                                 |
|:----:|:-------------:|:-----------------------------------------------------------:|
| Tool | get_citation  | Get the citation format for COPT.                           |
| Tool | get_reference | Get reference examples for a specified problem and language. |
| Tool | get_api_doc   | Return the most similar API documentation based on a query. |

## 🛠️ Installation and Usage

### Requirements

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

    In the `config.json` file, configure the necessary `API_KEY` for the model. By default, it uses models from [SiliconFlow](https://cloud.siliconflow.cn/i/5JAHVbNN).

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

### Integration with Clients

You can use FastMCP to automatically integrate this MCP service. For details, see the [MCP Integration Documentation](https://gofastmcp.com/integrations/anthropic). Here is an example of integrating with Cursor using FastMCP:

```bash
fastmcp install cursor server.py
```

Alternatively, you can add it manually to the configuration file of an MCP-supported client:

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

For other configurations, see the [Detailed Installation Guide](./docs/detail_install_EN.md).

## 🔧 Detailed Introduction

COPT-MCP provides three core tools to help AI assistants better serve users with optimization solving.

### Get Citation Format

**Tool Name**: `get_citation`

**Functionality**: Gets the academic citation format for the COPT solver, supporting Word and BibTeX formats.

**Parameters**:

- `citation_type` (str): The type of citation.
  - `"word"`: Citation format suitable for Word documents.
  - `"bibtex"`: Citation format suitable for BibTeX files.

**Returns**: The citation text in the corresponding format.

**Usage**:

- When a user needs to cite the COPT solver in their academic paper, the AI assistant can call the `get_citation` tool, passing `"word"` or `"bibtex"` as the parameter to get the corresponding citation text.
- The citation text files are located in the `resource/citation` folder and can be viewed and modified.

### Get Reference Example

**Tool Name**: `get_reference`

**Functionality**: Gets reference code examples for a specified problem type and programming language, including detailed mathematical modeling descriptions and code comments.

**Parameters**:

- `problem_type` (str): The type of problem to be solved (currently supports the following).
  - `"LP"`: Linear Programming
  - `"MIP"`: Mixed Integer Programming
  - `"SOCP"`: Second-Order Cone Programming
- `language` (str): The API interface language (currently supports the following).
  - `"Python"`: Python interface

**Returns**: A Markdown document containing mathematical definitions, code examples, and detailed comments.

**Usage**:

- When a user needs to solve a problem with the COPT solver, the AI assistant should first call the `get_reference` tool, passing the `problem_type` and `language` parameters to get a relevant example. This leverages the large model's Few-Shot learning capabilities to reduce hallucinations and improve accuracy.
- The reference example code is located in `resource/example/{problem_type}/{language}.md` and can be customized or expanded with more examples.

### Get API Documentation

**Tool Name**: `get_api_doc`

**Functionality**: Returns the most similar API documentation based on a query.

**Parameters**:

- `instructions` (str): A query, which can be a natural language description or a code snippet. Examples:
  - `"name"`: Query by API name, e.g., "Model.addConstr()" or "Envr()".
  - `"description"`: Query by a description of needs, e.g., "Add a set of linear constraints using matrix modeling".
- `language` (str): The API interface language (currently supports "Python").
- `domain` (str): The field corresponding to the query.
  - `"name"`: Query by API name.
  - `"description"`: Query by API description.
- `recall_num` (int): The number of documents to retrieve, default is 10, max is 25.
- `return_num` (int): The final number of documents to return after reranking, default is 3, max is 8.

**Returns**: A Markdown document containing the API name, description, and example code.

**Usage**:

- When a large model is unsure about a COPT solver API, it should first call `get_api_doc` with the `instructions`, `language`, `domain`, and `recall_num` parameters to fetch the relevant documentation.
- The data source is the official COPT solver documentation. An embedding model retrieves the most similar documents, which are then reranked before being returned to the large model.
- The data is stored in the `resource/api_doc/{language}` folder, in both JSON format (for user viewing) and a `.db` file (for model querying).
- The API documentation is not yet complete due to the large number of APIs. Completed documentation can be found in the `TODO.md` file in the `resource/api_doc/{language}` folder. Contributions are welcome.

## 🤝 Contribution Guide

We welcome community contributions! If you would like to contribute to the COPT-MCP project, please:

1.  Fork this repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

### Contribution Types

- 🐛 Bug fixes
- 📝 Improvements to existing features
- ✨ New feature development
- 📚 Documentation improvements
- 🧪 Adding test cases
- 🌍 Internationalization support

## 📝 Changelog

### Latest Information

- **v0.3.0** (2025-08-04) Modified the documentation structure and added detailed MCP installation support.

### History

- **v0.1.0** (2025-07-29) Initial version, completed the rapid integration and use of COPT-MCP.
- **v0.2.0** (2025-07-31) Completed all Python API documentation, added reranking function to `get_api_doc`.
- **v0.3.0** (2025-08-04) Modified the documentation structure and added detailed MCP installation support.

## 🤗 Acknowledgements

The creation and completion of this project would not have been possible without the selfless help of the following individuals and organizations. I express my sincere gratitude to them:

- [Shanshu Technology](https://www.cardopt.com/): Thanks to Shanshu Technology for developing the COPT solver and providing detailed official documentation. Without the COPT solver, COPT-MCP would not exist.
- [FastMCP](https://gofastmcp.com/): Thanks to the developers of FastMCP. Without FastMCP, the rapid integration of COPT-MCP would not have been possible.
- [Claude Code](https://github.com/anthropics/claude-code): Thanks to Claude Code, the most powerful AI programming assistant I have ever used. Without it, the rapid development of COPT-MCP would not have been possible.
- [Cursor](https://www.cursor.com/): Thanks to Cursor, the true primary author of this README. Without it, the rapid completion of the COPT-MCP documentation would not have been possible.

Additionally, I would like to thank the experts in the Shanshu COPT Solver Exchange Group 2 (QQ Group: 142636109). Your discussions gave me many inspirations and a deeper understanding of the COPT solver.

Finally, thank you for using COPT-MCP. If you have any questions or suggestions, please feel free to contact me.

## 📞 Contact Us

- **Personal Email**: cjl3473383542@163.com
- **University Email**: 2023110603@stu.sufe.edu.cn (Both are fine)
- **GitHub Issues**: [Submit an issue](https://github.com/ChengJiale150/COPT-MCP/issues)

### Related Links

- [COPT Solver](https://www.cardopt.com/solver)
- [COPT Documentation (Chinese)](https://pub.shanshu.ai/cardinalsite_v2/video/20250623/copt-userguide_cn.pdf)
- [FastMCP](https://gofastmcp.com)
- [MCP Protocol](https://modelcontextprotocol.io/)

---

<div align="center">

**If this project is helpful to you, please give us a ⭐️**

Made with ❤️ by [ChengJiale150](https://github.com/ChengJiale150)

</div>
