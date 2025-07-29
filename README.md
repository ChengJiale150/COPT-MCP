<div align="center">

<!-- omit in toc -->

# COPT-MCP 🚀

<strong>基于杉树科技开发的COPT求解器的MCP服务，提供专门为大语言模型设计的文档和示例</strong>

*由 [ChengJiale150](https://github.com/ChengJiale150) 开发*

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![COPT](https://img.shields.io/badge/COPT-7.2.9+-green.svg)](https://www.cardopt.com/solver)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.10.6+-orange.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](./docs/README_EN.md) | 中文

</div>

---

## 📖 目录

- [项目简介](#-项目简介)
- [功能一览](#-功能一览)
- [安装与使用](#-安装与使用)
- [详细介绍](#-详细介绍)
- [贡献指南](#-贡献指南)
- [致谢](#-致谢)
- [联系我们](#-联系我们)

## 🎯 项目简介

COPT-MCP 是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的服务，为支持MCP的客户端提供COPT求解器的相关接口的详细文档与示例，旨在实现COPT求解器的文档AI化适配，降低模型幻觉，提高大模型使用COPT求解器的准确性。

### 为什么需要COPT-MCP

COPT求解器是一款针对大规模优化问题的高效数学规划求解器，支持线多种优化问题，是解决复杂运筹规划问题的不二之选。然而，COPT求解器的相关信息在公开场合较少，导致大模型在调用COPT求解器时，容易出现幻觉，影响使用体验。直接输入COPT的官方文档，也会因为文档过长，远超模型上下文长度上限，而且过多的无关文档内容也会影响模型理解，导致上下文迷失。

COPT-MCP旨在为大模型提供COPT求解器的相关接口的最小可行文档与示例，通过精心组织与选取文档内容，实现COPT求解器的文档AI化适配，输出最小必要信息，降低模型幻觉，提高大模型使用COPT求解器相关接口的准确性。

### COPT-MCP的优势

- 🔧 **多类型支持**: 支持多种规划问题与编程语言
- 📚 **丰富的示例库**: 提供详细的代码示例和API说明
- 📖 **学术引用支持**: 提供Word和BibTeX格式的引用模板
- 🔌 **MCP协议**: 标准化的AI助手集成接口，支持多种大模型与客户端
- 🚀 **轻量化部署**: 无需安装额外软件，仅需Python虚拟环境
- 📝 **中文文档**: 完整的中文文档和示例说明

## ✨ 功能一览

| 类型   | 名称            | 描述                     |
|:----:|:-------------:|:----------------------:|
| Tool | get_citation  | 获取COPT的引用格式            |
| Tool | get_reference | 获取COPT的指定语言接口对应问题的参考示例 |
| Tool | get_api_doc   | 根据查询指令召回最相似的API文档      |

## 🛠️ 安装与使用

### 环境要求

- Python 3.12+
- FastMCP
- uv （推荐，用于版本管理）

### 安装步骤

1. **克隆项目**
   
```bash
git clone https://github.com/ChengJiale150/COPT-MCP.git
cd COPT-MCP
```

2. **安装依赖**
   
```bash
pip install uv
uv sync
```

3. **运行MCP服务**

```bash
uv run server.py
```

### 在客户端中集成

在支持MCP的客户端配置文件中添加：

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

## 🔧 详细介绍

COPT-MCP提供两个核心工具，帮助AI助手更好地为用户提供优化求解服务。

### 获取引用格式

**工具名称**: `get_citation`

**功能**: 获取COPT求解器的学术引用格式，支持Word和BibTeX格式。

**参数**:

- `citation_type` (str): 引用类型
  - `"word"`: 适用于Word文档的引用格式
  - `"bibtex"`: 适用于BibTeX文件的引用格式

**返回**: 对应格式的引用文本

**使用示例**:

```python
# 获取Word格式引用
word_citation = get_citation("word")
# 返回: [1] D. Ge, Q. Huangfu, Z. Wang, J. Wu and Y. Ye. Cardinal Optimizer (COPT) user guide. https://guide.coap.online/copt/en-doc, 2023.

# 获取BibTeX格式引用
bibtex_citation = get_citation("bibtex")
# 返回: @misc{copt, author={Dongdong Ge and Qi Huangfu and Zizhuo Wang and Jian Wu and Yinyu Ye}, title={Cardinal {O}ptimizer {(COPT)} user guide}, howpublished={https://guide.coap.online/copt/en-doc}, year=2023}
```

### 获取参考示例

**工具名称**: `get_reference`

**功能**: 获取指定问题类型和编程语言的参考示例代码，包含详细的数学建模说明和代码注释。

**参数**:

- `problem_type` (str): 求解问题类型
  - `"LP"`: 线性规划 (Linear Programming)
  - `"MIP"`: 混合整数规划 (Mixed Integer Programming)
  - `"SOCP"`: 二阶锥规划 (Second-Order Cone Programming)
- `language` (str): API接口语言
  - `"Python"`: Python接口 (目前唯一支持的语言)

**返回**: 包含数学定义、代码示例和详细注释的Markdown格式文档

**使用示例**:

```python
# 获取线性规划Python示例
lp_example = get_reference("LP", "Python")

# 获取混合整数规划Python示例
mip_example = get_reference("MIP", "Python")

# 获取二阶锥规划Python示例
socp_example = get_reference("SOCP", "Python")
```

## 📚 使用示例

### 示例1: 获取学术引用

当用户需要在其学术论文中引用COPT求解器时，AI助手可以调用：

```python
# 获取Word格式引用
citation = get_citation("word")
print("请在您的论文中使用以下引用格式：")
print(citation)
```

### 示例2: 解决线性规划问题

当用户需要解决线性规划问题时，AI助手可以：

1. 首先获取参考示例：
   
   ```python
   example = get_reference("LP", "Python")
   print("以下是线性规划问题的完整解决方案：")
   print(example)
   ```

2. 根据用户的具体问题，基于示例代码进行定制化修改

### 示例3: 解决混合整数规划问题

对于需要整数决策变量的问题：

```python
# 获取MIP示例
mip_example = get_reference("MIP", "Python")
print("混合整数规划问题解决方案：")
print(mip_example)
```

## 🎯 支持的问题类型

### 1. 线性规划 (LP)

- **适用场景**: 生产计划、资源分配、运输优化等
- **特点**: 所有变量为连续变量，目标函数和约束条件均为线性
- **示例**: 生产与库存计划优化

### 2. 混合整数规划 (MIP)

- **适用场景**: 设施选址、调度问题、投资组合优化等
- **特点**: 包含连续变量和整数变量
- **示例**: 0-1背包问题、设施选址问题

### 3. 二阶锥规划 (SOCP)

- **适用场景**: 投资组合优化、信号处理、机器学习等
- **特点**: 包含二阶锥约束，可处理非线性优化问题
- **示例**: 投资组合风险优化

## 🤝 贡献指南

我们欢迎社区贡献！如果您想为COPT-MCP项目做出贡献，请：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

### 贡献类型

- 🐛 Bug修复
- ✨ 新功能开发
- 📚 文档改进
- 🧪 测试用例添加
- 🌍 国际化支持

## 🔗 相关链接

- [COPT官网](https://www.coap.online/copt)
- [COPT用户指南](https://guide.coap.online/copt/en-doc)
- [FastMCP文档](https://gofastmcp.com)
- [MCP协议规范](https://modelcontextprotocol.io/)

## 📞 联系我们

- 杉树科技官网: https://www.coap.online/
- 技术支持: support@coap.online
- GitHub Issues: [提交问题](https://github.com/your-username/COPT-MCP/issues)

---

<div align="center">

**如果这个项目对您有帮助，请给我们一个 ⭐️**

Made with ❤️ by [ChengJiale150](https://github.com/ChengJiale150)

</div>
