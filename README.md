<div align="center">

<!-- omit in toc -->

# COPT-MCP 🚀

<strong>基于杉数科技开发的COPT求解器的MCP服务，提供专门为大语言模型设计的文档和示例</strong>

*由 [ChengJiale150](https://github.com/ChengJiale150) 开发*

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![COPT](https://img.shields.io/badge/COPT-7.2.9+-green.svg)](https://www.cardopt.com/solver)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.10.6+-orange.svg)](https://github.com/jlowin/fastmcp)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-v0.4.0-blue.svg)](https://github.com/ChengJiale150/COPT-MCP)

[English](./international/README_EN.md) | 中文

</div>

---

## 📖 目录

- [项目简介](#-项目简介)
- [功能一览](#-功能一览)
- [安装与使用](#-安装与使用)
- [详细介绍](#-详细介绍)
- [贡献指南](#-贡献指南)
- [更新日志](#-更新日志)
- [致谢](#-致谢)
- [联系我们](#-联系我们)

## 🎯 项目简介

COPT-MCP 是一个基于 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 的服务，为支持MCP的客户端提供COPT求解器的相关接口的详细文档与示例，旨在实现COPT求解器的文档AI化适配，降低模型幻觉，提高大模型使用COPT求解器的准确性。

### 为什么需要COPT-MCP

COPT求解器是一款针对大规模优化问题的高效数学规划求解器，支持多种优化问题，是解决复杂运筹规划问题的不二之选。然而，COPT求解器的相关信息在公开场合较少，导致大模型在调用COPT求解器时，容易出现幻觉，影响使用体验。直接输入COPT的官方文档，也会因为文档过长，远超模型上下文长度上限，而且过多的无关文档内容也会影响模型理解，导致上下文迷失。

COPT-MCP旨在为大模型提供COPT求解器的相关接口的最小可行文档与示例，通过精心组织与选取文档内容，实现COPT求解器的文档AI化适配，输出最小必要信息，降低模型幻觉，提高大模型使用COPT求解器相关接口的准确性。

### COPT-MCP的优势

- 🔧 **多类型支持**: 支持多种规划问题与编程语言
- 📚 **丰富的示例库**: 提供详细的代码示例和API说明
- 📖 **学术引用支持**: 提供Word和BibTeX格式的引用模板
- 🔌 **MCP协议**: 通过MCP协议方便与各类大模型与Agent嵌入集成
- 🚀 **轻量化部署**: 无需安装额外软件，仅需Python虚拟环境
- 📝 **中文文档**: 完整的中文文档和示例说明

## ✨ 功能一览

| 类型   | 名称            | 描述                     |
|:----:|:-------------:|:----------------------:|
| Tool | get_citation  | 获取COPT的引用格式            |
| Tool | get_reference | 获取COPT的指定语言接口对应问题的参考示例 |
| Tool | get_api_doc   | 根据查询指令返回最相似的API文档      |

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

3. **配置环境变量**

在config.json文件中配置模型的必要的API_KEY,这里默认使用的是[硅基流动](https://cloud.siliconflow.cn/i/5JAHVbNN)的相关模型

```
"embedding": {
    "url": "https://api.siliconflow.cn/v1/embeddings",
    "api_key": "<your api key>"
},
"reranker": {
    "url": "https://api.siliconflow.cn/v1/rerank",
    "api_key": "<your api key>"
}
```

4. **运行MCP服务**

```bash
uv run fastmcp run server.py
```

### 在客户端中集成

你可以使用FastMCP自动集成该MCP服务,具体详见[MCP集成文档](https://gofastmcp.com/integrations/anthropic),这里以使用FastMCP在Cursor中集成为例：

```bash
fastmcp install cursor server.py
```

或者也可以在支持MCP的客户端配置文件中手动添加：

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

其他配置详见[详细配置指引](./docs/detail_install.md)

## 🔧 详细介绍

COPT-MCP提供三个核心工具，帮助AI助手更好地为用户提供优化求解服务。

### 获取引用格式

**工具名称**: `get_citation`

**功能**: 获取COPT求解器的学术引用格式，支持Word和BibTeX格式。

**参数**:

- `citation_type` (str): 引用类型
  - `"word"`: 适用于Word文档的引用格式
  - `"bibtex"`: 适用于BibTeX文件的引用格式

**返回**: 对应格式的引用文本

**使用说明**:

- 当用户需要在其学术论文中引用COPT求解器时，AI助手可以调用`get_citation`工具，并传入`"word"`或`"bibtex"`参数，获取对应格式的引用文本。
- 引用对应的格式文本位于`resource/citation`文件夹中，可以自行查看并修改。

### 获取参考示例

**工具名称**: `get_reference`

**功能**: 获取指定问题类型和编程语言的参考示例代码，包含详细的数学建模说明和代码注释。

**参数**:

- `problem_type` (str): 求解问题类型(目前仅支持以下类型)
  - `"LP"`: 线性规划 (Linear Programming)
  - `"MIP"`: 混合整数规划 (Mixed Integer Programming)
  - `"SOCP"`: 二阶锥规划 (Second-Order Cone Programming)
  - `"NLP"`: 非线性规划 (Nonlinear Programming)
- `language` (str): API接口语言(目前仅支持以下类型)
  - `"Python"`: Python接口

**返回**: 包含数学定义、代码示例和详细注释的Markdown格式文档

**使用说明**:

- 当用户需要解决COPT求解器相关问题时，AI助手会优先调用`get_reference`工具，并传入`problem_type`和`language`参数，获取对应问题的参考示例,利用大模型良好的Few Shot理解能力,降低模型幻觉,提高模型使用COPT求解器的准确性。
- 参考示例代码位于`resource/example/{problem_type}/{language}.md`文件中，可以自行查看并修改,也可以根据需要添加更多示例。

### 获取API文档

**工具名称**: `get_api_doc`

**功能**: 根据查询指令返回最相似的API文档信息

**参数**:

- `instructions` (str): 查询指令,支持自然语言描述与代码片段的查询,参考的查询指令如下：
  - `"name"`: 查询API名称,如"Model.addConstr()"/"Envr()"
  - `"description"`: 查询需求描述,如"使用矩阵建模添加一组线性约束"
- `language` (str): API接口语言(目前仅支持以下类型)
  - `"Python"`: Python接口
- `domain` (str): 查询指令对应的字段,目前支持的领域如下：
  - `"name"`: 查询API名称
  - `"description"`: 查询API描述
- `recall_num`(int): 查询召回数量,默认为10,最大为25
- `return_num`(int): 重排序后最终返回数量,默认为3,最大为8

**返回**: 包含API名称、描述、示例代码的Markdown格式文档

**使用说明**:

- 当大模型不清楚COPT求解器的相关API时，会优先调用`get_api_doc`工具，并传入`instructions`、`language`、`domain`和`recall_num`参数，获取对应API的文档。
- 数据来源为COPT求解器的官方文档，通过嵌入模型召回最相似的API文档，并经过重排序返回给大模型。
- 数据存储在`resource/api_doc/{language}`文件夹中，分别存储为JSON格式(原始数据,用于用户查看)与db格式(用于模型查询)。
- 由于API文档数量较多，目前尚不完善,已完成的API文档详见`resource/api_doc/{language}`文件夹中的TODO.md,后续会持续更新,欢迎大家贡献更多API文档。

## 🤝 贡献指南

我们欢迎社区贡献！如果您想为COPT-MCP项目做出贡献，请：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

### 贡献类型

- 🐛 Bug修复
- 📝 旧功能完善
- ✨ 新功能开发
- 📚 文档改进
- 🧪 测试用例添加
- 🌍 国际化支持

## 📝 更新日志

下述日志仅记录版本大更新记录的概要,具体信息详见[更新日志](./docs/update_info.md)

### 最新信息

- **v0.4.0**(2025-08-10) 添加非线性规划(NLP)的参考示例,完善了MCP类型注释

### 历史信息

- **v0.1.0**(2025-07-29) 初始版本,完成COPT-MCP的快速集成与使用
- **v0.2.0**(2025-07-31) 完善了Python的API接口的全部文档,`get_api_doc`添加了重排序功能
- **v0.3.0**(2025-08-04) 修改了文档结构,添加了详尽的MCP安装支持
- **v0.4.0**(2025-08-10) 添加非线性规划(NLP)的参考示例,完善了MCP类型注释

## 🤗 致谢

本项目的成立与完成离不开下述诸位的无私帮助,没有他们就没有COPT-MCP的诞生,在此表示衷心的感谢：

- [杉数科技](https://www.cardopt.com/): 感谢杉数科技开发了COPT求解器,并提供了详尽的官方文档,没有COPT求解器就没有COPT-MCP的诞生
- [FastMCP](https://gofastmcp.com/): 感谢FastMCP的开发者们,没有FastMCP就没有COPT-MCP的快速集成
- [Claude Code](https://github.com/anthropics/claude-code): 感谢Claude Code, TA是我使用过的最强大的AI编程助手,没有TA就没有COPT-MCP的快速开发
- [Cursor](https://www.cursor.com/): 感谢Cursor, TA才是本篇README的第一作者,没有TA就没有COPT-MCP文档的快速完成

此外,还要感谢杉数COPT求解器交流2群(QQ群号:142636109)的各位大佬,大家的讨论给了我很多启发,让我对COPT求解器有了更深入的理解,在此表示衷心的感谢。

最后,感谢各位使用COPT-MCP,如果有什么问题或者建议,欢迎随时联系我,我会尽快回复。

## 📞 联系我们

- 个人邮箱: cjl3473383542@163.com
- 学校邮箱: 2023110603@stu.sufe.edu.cn (两种邮箱均可)
- GitHub Issues: [提交问题](https://github.com/ChengJiale150/COPT-MCP/issues)

### 相关链接

- [COPT求解器](https://www.cardopt.com/solver)
- [COPT文档](https://pub.shanshu.ai/cardinalsite_v2/video/20250623/copt-userguide_cn.pdf)
- [FastMCP](https://gofastmcp.com)
- [MCP协议](https://modelcontextprotocol.io/)

---

<div align="center">

**如果这个项目对您有帮助，请给我们一个 ⭐️**

Made with ❤️ by [ChengJiale150](https://github.com/ChengJiale150)

</div>
