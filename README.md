<div align="center">

<!-- omit in toc -->

# COPT-MCP 🚀

<strong>基于杉树科技COPT求解器的MCP服务，为AI助手提供强大的数学优化求解能力</strong>

*由 [杉树科技](https://www.coap.online/) 开发*

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![COPT](https://img.shields.io/badge/COPT-7.2.9+-green.svg)](https://www.coap.online/copt)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.10.6+-orange.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English](./docs/README_EN.md) | 中文

</div>

---

## 📖 目录

- [项目简介](#-项目简介)
- [功能特性](#-功能特性)
- [安装与使用](#-安装与使用)
- [MCP工具介绍](#-mcp工具介绍)
  - [获取引用格式](#获取引用格式)
  - [获取参考示例](#获取参考示例)
- [使用示例](#-使用示例)
- [支持的问题类型](#-支持的问题类型)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

## 🎯 项目简介

COPT-MCP 是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的服务，为AI助手提供杉树科技 [COPT (Cardinal Optimizer)](https://www.coap.online/copt) 求解器的访问能力。COPT是一款高性能的数学优化求解器，支持线性规划(LP)、混合整数规划(MIP)、二阶锥规划(SOCP)等多种优化问题。

通过COPT-MCP服务，AI助手可以：

- 获取COPT的学术引用格式
- 查看各种优化问题的参考示例代码
- 为用户提供专业的数学优化解决方案

## ✨ 功能特性

- 🔧 **多问题类型支持**: 支持LP、MIP、SOCP等主流优化问题
- 📚 **丰富的示例库**: 提供详细的Python代码示例和数学建模说明
- 📖 **学术引用支持**: 提供Word和BibTeX格式的引用模板
- 🚀 **高性能求解**: 基于COPT求解器的强大算法能力
- 🔌 **MCP协议**: 标准化的AI助手集成接口
- 📝 **中文文档**: 完整的中文文档和示例说明

## 🛠️ 安装与使用

### 环境要求

- Python 3.11+
- COPT 7.2.9+
- FastMCP 2.10.6+

### 安装步骤

1. **克隆项目**
   
   ```bash
   git clone https://github.com/your-username/COPT-MCP.git
   cd COPT-MCP
   ```

2. **安装依赖**
   
   ```bash
   # 使用uv (推荐)
   uv sync
   ```

# 或使用pip

pip install -r requirements.txt

```
3. **配置COPT许可证**
确保您已获得COPT求解器的有效许可证。详情请访问 [COPT官网](https://www.coap.online/copt)。

4. **运行MCP服务**
```bash
python server.py
```

### 在AI助手中集成

在支持MCP的AI助手配置文件中添加：

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

## 🔧 MCP工具介绍

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

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

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

Made with ❤️ by [杉树科技](https://www.coap.online/)

</div>
