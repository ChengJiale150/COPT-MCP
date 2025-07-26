<div align="center">

<!-- omit in toc -->

# COPT-MCP 🚀

<strong>MCP service based on Cardinal Optimizer (COPT) solver, providing powerful mathematical optimization capabilities for AI assistants</strong>

*Developed by [Cardinal Operations](https://www.coap.online/)*

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![COPT](https://img.shields.io/badge/COPT-7.2.9+-green.svg)](https://www.coap.online/copt)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.10.6+-orange.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

English | [中文](README.md)

</div>

---

## 📖 Table of Contents

- [Project Introduction](#-project-introduction)
- [Features](#-features)
- [Installation & Usage](#-installation--usage)
- [MCP Tools](#-mcp-tools)
  - [Get Citation Format](#get-citation-format)
  - [Get Reference Examples](#get-reference-examples)
- [Usage Examples](#-usage-examples)
- [Supported Problem Types](#-supported-problem-types)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Project Introduction

COPT-MCP is a service based on the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) that provides AI assistants with access to the [COPT (Cardinal Optimizer)](https://www.coap.online/copt) solver developed by Cardinal Operations. COPT is a high-performance mathematical optimization solver that supports various optimization problems including Linear Programming (LP), Mixed Integer Programming (MIP), Second-Order Cone Programming (SOCP), and more.

Through the COPT-MCP service, AI assistants can:
- Obtain academic citation formats for COPT
- View reference example code for various optimization problems
- Provide users with professional mathematical optimization solutions

## ✨ Features

- 🔧 **Multiple Problem Types**: Supports LP, MIP, SOCP, and other mainstream optimization problems
- 📚 **Rich Example Library**: Provides detailed Python code examples and mathematical modeling explanations
- 📖 **Academic Citation Support**: Offers citation templates in Word and BibTeX formats
- 🚀 **High-Performance Solving**: Based on COPT solver's powerful algorithmic capabilities
- 🔌 **MCP Protocol**: Standardized AI assistant integration interface
- 📝 **Comprehensive Documentation**: Complete documentation and example explanations

## 🛠️ Installation & Usage

### Requirements

- Python 3.11+
- COPT 7.2.9+
- FastMCP 2.10.6+

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/your-username/COPT-MCP.git
cd COPT-MCP
```

2. **Install dependencies**
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

3. **Configure COPT license**
Ensure you have obtained a valid license for the COPT solver. For details, please visit the [COPT official website](https://www.coap.online/copt).

4. **Run the MCP service**
```bash
python server.py
```

### Integration with AI Assistants

Add the following to your MCP-enabled AI assistant configuration file:

```json
{
  "mcpServers": {
    "copt-mcp": {
      "command": "python",
      "args": ["/path/to/COPT-MCP/server.py"],
      "env": {
        "COPT_LICENSE": "/path/to/your/copt.lic"
      }
    }
  }
}
```

## 🔧 MCP Tools

COPT-MCP provides two core tools to help AI assistants better serve users with optimization solutions.

### Get Citation Format

**Tool Name**: `get_citation`

**Function**: Obtain academic citation formats for the COPT solver, supporting Word and BibTeX formats.

**Parameters**:
- `citation_type` (str): Citation type
  - `"word"`: Citation format suitable for Word documents
  - `"bibtex"`: Citation format suitable for BibTeX files

**Returns**: Citation text in the corresponding format

**Usage Example**:
```python
# Get Word format citation
word_citation = get_citation("word")
# Returns: [1] D. Ge, Q. Huangfu, Z. Wang, J. Wu and Y. Ye. Cardinal Optimizer (COPT) user guide. https://guide.coap.online/copt/en-doc, 2023.

# Get BibTeX format citation
bibtex_citation = get_citation("bibtex")
# Returns: @misc{copt, author={Dongdong Ge and Qi Huangfu and Zizhuo Wang and Jian Wu and Yinyu Ye}, title={Cardinal {O}ptimizer {(COPT)} user guide}, howpublished={https://guide.coap.online/copt/en-doc}, year=2023}
```

### Get Reference Examples

**Tool Name**: `get_reference`

**Function**: Obtain reference example code for specified problem types and programming languages, including detailed mathematical modeling explanations and code comments.

**Parameters**:
- `problem_type` (str): Optimization problem type
  - `"LP"`: Linear Programming
  - `"MIP"`: Mixed Integer Programming
  - `"SOCP"`: Second-Order Cone Programming
- `language` (str): API interface language
  - `"Python"`: Python interface (currently the only supported language)

**Returns**: Markdown format document containing mathematical definitions, code examples, and detailed comments

**Usage Example**:
```python
# Get Linear Programming Python example
lp_example = get_reference("LP", "Python")

# Get Mixed Integer Programming Python example
mip_example = get_reference("MIP", "Python")

# Get Second-Order Cone Programming Python example
socp_example = get_reference("SOCP", "Python")
```

## 📚 Usage Examples

### Example 1: Get Academic Citation

When users need to cite the COPT solver in their academic papers, AI assistants can call:

```python
# Get Word format citation
citation = get_citation("word")
print("Please use the following citation format in your paper:")
print(citation)
```

### Example 2: Solve Linear Programming Problems

When users need to solve linear programming problems, AI assistants can:

1. First, get the reference example:
```python
example = get_reference("LP", "Python")
print("Here is the complete solution for the linear programming problem:")
print(example)
```

2. Customize the example code based on the user's specific problem

### Example 3: Solve Mixed Integer Programming Problems

For problems requiring integer decision variables:

```python
# Get MIP example
mip_example = get_reference("MIP", "Python")
print("Mixed Integer Programming problem solution:")
print(mip_example)
```

## 🎯 Supported Problem Types

### 1. Linear Programming (LP)
- **Applications**: Production planning, resource allocation, transportation optimization, etc.
- **Characteristics**: All variables are continuous, objective function and constraints are linear
- **Examples**: Production and inventory planning optimization

### 2. Mixed Integer Programming (MIP)
- **Applications**: Facility location, scheduling problems, portfolio optimization, etc.
- **Characteristics**: Contains both continuous and integer variables
- **Examples**: 0-1 Knapsack problem, Facility location problem

### 3. Second-Order Cone Programming (SOCP)
- **Applications**: Portfolio optimization, signal processing, machine learning, etc.
- **Characteristics**: Contains second-order cone constraints, can handle nonlinear optimization problems
- **Examples**: Portfolio risk optimization

## 🤝 Contributing

We welcome community contributions! If you would like to contribute to the COPT-MCP project, please:

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Types
- 🐛 Bug fixes
- ✨ New feature development
- 📚 Documentation improvements
- 🧪 Test case additions
- 🌍 Internationalization support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Links

- [COPT Official Website](https://www.coap.online/copt)
- [COPT User Guide](https://guide.coap.online/copt/en-doc)
- [FastMCP Documentation](https://gofastmcp.com)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## 📞 Contact Us

- Cardinal Operations Website: https://www.coap.online/
- Technical Support: support@coap.online
- GitHub Issues: [Submit Issues](https://github.com/your-username/COPT-MCP/issues)

---

<div align="center">

**If this project helps you, please give us a ⭐️**

Made with ❤️ by [Cardinal Operations](https://www.coap.online/)

</div> 