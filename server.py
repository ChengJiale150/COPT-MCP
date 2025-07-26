from fastmcp import FastMCP
import os, struct, requests, sqlite3, sqlite_vec
from typing import List

current_dir = os.path.dirname(os.path.abspath(__file__))
resource_path = os.path.join(current_dir, "resource")
api_key = "sk-wqdksytnrhdarewmhqtxkrribdztclmzukyorzxxnncqnlcz"

mcp = FastMCP(name="COPT-MCP",  version="0.1.0",
              instructions='''这是由杉树科技研发的COPT的MCP服务，你可以使用这个服务来解决COPT的问题''')

@mcp.tool()
def get_citation(citation_type: str) -> str:
    """
    获取COPT的引用格式
    
    Args:
        citation_type: 引用类型，包括：
            - "word": 适用于word文档
            - "bibtex": 适用于bibtex文件
    """
    if citation_type not in {"word", "bibtex"}:
        return f"目前尚不支持引用类型为{citation_type}"
    
    try:
        return open(f"{resource_path}/citation/{citation_type}.txt", "r" ,encoding="utf-8").read()
    except FileNotFoundError:
        return "文件不存在"

@mcp.tool()
def get_reference(problem_type: str, language: str) -> str:
    """
    获取COPT的指定语言接口对应问题的参考示例,推荐在调用COPT解决对应问题前调用
    
    Args:
        problem_type: 求解问题类型，目前支持的问题类型如下：
            - "LP": 线性规划(LP)
            - "MIP": 混合整数规划(MIP)
            - "SOCP": 二阶锥规划(SOCP)
        language: API接口语言，目前支持的语言如下：
            - "Python": Python接口
    """

    if problem_type not in {"LP", "MIP", "SOCP"}:
        return f"目前尚不支持问题类型为{problem_type}"
    
    if language not in {"Python"}:
        return f"目前尚不支持语言为{language}"
    
    try:
        return open(f"{resource_path}/example/{problem_type}/{language}.md", "r" ,encoding="utf-8").read()
    except FileNotFoundError:
        return "文件不存在"

@mcp.tool()
def get_api_doc(instructions: str, language: str, domain: str,
                recall_num: int = 3) -> str:
    """
    根据查询指令召回最相似的API文档
    
    Args:
        instructions: 查询指令,支持自然语言描述与代码片段的查询,参考的查询指令如下：
            - "name": 查询API名称,如"Model.addConstr()"/"Envr()"
            - "description": 查询需求描述,如"使用矩阵建模添加一组线性约束"
            - "code": 相似的代码片段(可多行),如"model.addConstr(x + y <= 1)\nmodel.addConstr(x + y <= 2)"
        language: API接口语言,目前支持的语言如下：
            - "Python": Python接口
        domain: 查询指令对应的字段,目前支持的领域如下：
            - "name": 查询API名称
            - "description": 查询API描述
            - "code": 查询API代码示例
        recall_num: 查询召回数量,默认为3,最大为10
    """
    def get_embedding(text: str, dim: int = 128) -> bytes:
        def serialize_f32(vector: List[float]) -> bytes:
            return struct.pack("%sf" % len(vector), *vector)
        url = "https://api.siliconflow.cn/v1/embeddings"
        
        payload = {
            "model": "Qwen/Qwen3-Embedding-4B",
            "input": text,
            "encoding_format": "float",
            "dimensions": dim
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        return serialize_f32(response.json()["data"][0]["embedding"])
    
    def contact_result(name: str, description: str, code: str) -> str:
        return f'''
### {name}

#### 详细描述
{description}

#### 代码示例
```
{code}
```

---
'''

    dim_map = {
        "name": 64,
        "description": 512,
        "code": 512
    }

    if language not in {"Python"}:
        return f"目前尚不支持语言为{language}"
    if domain not in dim_map:
        return f"目前尚不支持字段为{domain}"
    if recall_num > 10 or recall_num < 1:
        return "召回数量必须在1到10之间"
    
    try:
        db = sqlite3.connect(f"{resource_path}/api_doc/{language}/vector.db")
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        rows = db.execute(
            f"""
            SELECT
                rowid,
                distance
            FROM {domain}_vec
            WHERE embedding MATCH ?
            ORDER BY distance
            LIMIT {recall_num}
            """,
            [get_embedding(instructions, dim_map[domain])],
        ).fetchall()
        result_id = ",".join([str(rowid) for rowid, _ in rows])
        result_recall = db.execute(f"SELECT name, description, code FROM api_doc WHERE rowid IN ({result_id})").fetchall()
        result = ""
        for name, description, code in result_recall:
            result += contact_result(name, description, code)
        return result

    except Exception as e:
        return f"发生错误: {e}"
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run(transport="stdio")