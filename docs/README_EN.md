<div align="center">

<!-- omit in toc -->

**ATTENTION: The English version is translated by AI, The original version is [Chinese Version](../README.md)**

# COPT-MCP 🚀

<strong>MCP service based on COPT solver developed by Cardinal Operations, providing documentation and examples specifically designed for large language models</strong>

*Developed by [ChengJiale150](https://github.com/ChengJiale150)*

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![COPT](https://img.shields.io/badge/COPT-7.2.9+-green.svg)](https://www.cardopt.com/solver)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.10.6+-orange.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](../LICENSE)

English | [中文](../README.md)

</div>

---

## 📖 Table of Contents

- [Project Introduction](#-project-introduction)
- [Feature Overview](#-feature-overview)
- [Installation & Usage](#-installation--usage)
- [Detailed Introduction](#-detailed-introduction)
- [Contributing](#-contributing)
- [Changelog](#-changelog)
- [Acknowledgments](#-acknowledgments)
- [Contact Us](#-contact-us)

## 🎯 Project Introduction

COPT-MCP is a service based on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) that provides detailed documentation and examples of COPT solver-related interfaces for MCP-enabled clients. It aims to achieve AI-adapted documentation for the COPT solver, reduce model hallucinations, and improve the accuracy of large models using the COPT solver.

### Why COPT-MCP is Needed

The COPT solver is an efficient mathematical programming solver for large-scale optimization problems, supporting various optimization problems and is the ideal choice for solving complex operational planning problems. However, information about the COPT solver is scarce in public forums, leading to frequent hallucinations when large models call the COPT solver, affecting user experience. Directly inputting COPT's official documentation can also cause issues due to document length exceeding model context limits, and excessive irrelevant content can affect model understanding, leading to context confusion.

COPT-MCP aims to provide large models with the minimum viable documentation and examples for COPT solver-related interfaces. Through carefully organized and selected documentation content, it achieves AI-adapted documentation for the COPT solver, outputs minimal necessary information, reduces model hallucinations, and improves the accuracy of large models using COPT solver-related interfaces.

### Advantages of COPT-MCP

- 🔧 **Multi-type Support**: Supports various programming problems and programming languages
- 📚 **Rich Example Library**: Provides detailed code examples and API documentation
- 📖 **Academic Citation Support**: Offers citation templates in Word and BibTeX formats
- 🔌 **MCP Protocol**: Easy integration with various large models and agents through MCP protocol
- 🚀 **Lightweight Deployment**: No additional software installation required, only Python virtual environment needed
- 📝 **Chinese Documentation**: Complete Chinese documentation and example explanations

## ✨ Feature Overview

| Type | Name | Description |
|:----:|:-------------:|:----------------------:|
| Tool | get_citation | Get COPT citation format |
| Tool | get_reference | Get reference examples for specified language interfaces and problem types |
| Tool | get_api_doc | Retrieve most similar API documentation based on query instructions |

## 🛠️ Installation & Usage

### Requirements

- Python 3.12+
- FastMCP
- uv (recommended for version management)

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/ChengJiale150/COPT-MCP.git
cd COPT-MCP
```

2. **Install dependencies**
```bash
pip install uv
uv sync
```

3. **Configure environment variables**

Configure EMB_URL and EMB_API_KEY in the .env file. The default uses [Silicon Flow](https://cloud.siliconflow.cn/i/5JAHVbNN)'s embedding model (Qwen3-Embedding-8B)

```
EMB_URL=https://api.siliconflow.cn/v1/embeddings
EMB_API_KEY=<your_api_key>
```

4. **Run MCP service**

```bash
uv run fastmcp run server.py
```

### Integration with Clients

You can use FastMCP to automatically integrate this MCP service. For details, see the [MCP Integration Documentation](https://gofastmcp.com/integrations/anthropic). Here's an example of using FastMCP to integrate with Cursor:

```bash
fastmcp install cursor server.py
```

Or you can manually add it to the configuration file of MCP-enabled clients:

```json
{
  "mcpServers": {
    "copt-mcp": {
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

## 🔧 Detailed Introduction

COPT-MCP provides three core tools to help AI assistants better serve users with optimization solutions.

### Get Citation Format

**Tool Name**: `get_citation`

**Function**: Get academic citation formats for the COPT solver, supporting Word and BibTeX formats.

**Parameters**:
- `citation_type` (str): Citation type
  - `"word"`: Citation format suitable for Word documents
  - `"bibtex"`: Citation format suitable for BibTeX files

**Returns**: Citation text in the corresponding format

**Usage Instructions**:

- When users need to cite the COPT solver in their academic papers, AI assistants can call the `get_citation` tool and pass `"word"` or `"bibtex"` parameters to get the corresponding citation format text.
- The citation format text is located in the `resource/citation` folder and can be viewed and modified as needed.

### Get Reference Examples

**Tool Name**: `get_reference`

**Function**: Get reference example code for specified problem types and programming languages, including detailed mathematical modeling explanations and code comments.

**Parameters**:

- `problem_type` (str): Problem type (currently only supports the following types)
  - `"LP"`: Linear Programming
  - `"MIP"`: Mixed Integer Programming
  - `"SOCP"`: Second-Order Cone Programming
- `language` (str): API interface language (currently only supports the following types)
  - `"Python"`: Python interface

**Returns**: Markdown format document containing mathematical definitions, code examples, and detailed comments

**Usage Instructions**:
- When users need to solve COPT solver-related problems, AI assistants will first call the `get_reference` tool and pass `problem_type` and `language` parameters to get reference examples for the corresponding problems. This leverages the large model's excellent Few Shot understanding capabilities to reduce model hallucinations and improve the accuracy of models using the COPT solver.
- Reference example code is located in `resource/example/{problem_type}/{language}.md` files and can be viewed and modified as needed. You can also add more examples as required.

### Get API Documentation

**Tool Name**: `get_api_doc`

**Function**: Retrieve most similar API documentation based on query instructions

**Parameters**:

- `instructions` (str): Query instructions, supporting natural language descriptions and code snippet queries. Reference query instructions include:
  - `"name"`: Query API names, such as "Model.addConstr()"/"Envr()"
  - `"description"`: Query requirement descriptions, such as "Use matrix modeling to add a set of linear constraints"
- `language` (str): API interface language (currently only supports the following types)
  - `"Python"`: Python interface
- `domain` (str): Field corresponding to query instructions, currently supported domains include:
  - `"name"`: Query API names
  - `"description"`: Query API descriptions
- `recall_num` (int): Number of query recalls, default is 3, maximum is 10

**Returns**: Markdown format document containing API names, descriptions, and example code

**Usage Instructions**:

- When large models are unclear about COPT solver-related APIs, they will first call the `get_api_doc` tool and pass `instructions`, `language`, `domain`, and `recall_num` parameters to get the corresponding API documentation.
- Data source is the official COPT solver documentation, which retrieves the most similar API documentation through embedding models and returns it to the large model.
- Data is stored in the `resource/api_doc/{language}` folder, stored in JSON format (raw data for user viewing) and db format (for model queries).
- Due to the large number of API documents, the current implementation is not yet complete. For completed API documentation, see TODO.md. It will be continuously updated, and everyone is welcome to contribute more API documentation.

## 🤝 Contributing

We welcome community contributions! If you would like to contribute to the COPT-MCP project, please:

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Types
- 🐛 Bug fixes
- 📝 Existing feature improvements
- ✨ New feature development
- 📚 Documentation improvements
- 🧪 Test case additions
- 🌍 Internationalization support

## 📝 Changelog

### Latest Information

- **v0.1.0** (2025-07-29) Initial version, completed rapid integration and usage of COPT-MCP

### Historical Information

- **v0.1.0** (2025-07-29) Initial version, completed rapid integration and usage of COPT-MCP

## 🤗 Acknowledgments

The establishment and completion of this project would not have been possible without the selfless help of the following individuals. Without them, COPT-MCP would not have been born. Here we express our sincere gratitude:

- [Cardinal Operations](https://www.cardopt.com/): Thank you to Cardinal Operations for developing the COPT solver and providing comprehensive official documentation. Without the COPT solver, COPT-MCP would not have been born.
- [FastMCP](https://gofastmcp.com/): Thank you to the FastMCP developers. Without FastMCP, there would be no rapid integration of COPT-MCP.
- [Claude Code](https://github.com/anthropics/claude-code): Thank you to Claude Code. TA is the most powerful AI programming assistant I have ever used. Without TA, there would be no rapid development of COPT-MCP.
- [Cursor](https://www.cursor.com/): Thank you to Cursor. TA is actually the first author of this README. Without TA, there would be no rapid completion of COPT-MCP documentation.

Additionally, I would like to thank all the experts in the Cardinal COPT Solver Discussion Group 2 (Group ID: 142636109). Your discussions have given me many insights and helped me gain a deeper understanding of the COPT solver. Here I express my sincere gratitude.

Finally, thank you to everyone using COPT-MCP. If you have any questions or suggestions, please feel free to contact me, and I will respond as soon as possible.

## 📞 Contact Us

- Personal Email: cjl3473383542@163.com
- School Email: 2023110603@stu.sufe.edu.cn  (both email addresses are acceptable)
- GitHub Issues: [Submit Issues](https://github.com/ChengJiale150/COPT-MCP/issues)

### Related Links

- [COPT Solver](https://www.cardopt.com/solver)
- [COPT Documentation](https://pub.shanshu.ai/cardinalsite_v2/video/20250623/copt-userguide_cn.pdf)
- [FastMCP](https://gofastmcp.com)
- [MCP Protocol](https://modelcontextprotocol.io/)

---

<div align="center">

**If this project helps you, please give us a ⭐️**

Made with ❤️ by [ChengJiale150](https://github.com/ChengJiale150)

</div>
