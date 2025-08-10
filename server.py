from fastmcp import FastMCP
import os, sqlite3, sqlite_vec, json
from utils.embedding import get_embedding, contact_result, get_reranker
from typing import Annotated
from pydantic import Field

current_dir = os.path.dirname(os.path.abspath(__file__))
resource_path = os.path.join(current_dir, "resource")
with open(os.path.join(current_dir, "config.json"), "r", encoding="utf-8") as f:
    config = json.load(f)


mcp = FastMCP(name="COPT-MCP",  version="0.2.0",
              instructions='''这是由杉树科技研发的COPT的MCP服务，你可以使用这个服务来解决COPT的问题''',
              dependencies=[
                  "fastmcp",
                  "sqlite_vec",
                  "requests"
              ])

@mcp.tool()
def get_citation(
    citation_type: Annotated[str, Field(description="引用类型")]
    ) -> str:
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
def get_reference(
    problem_type: Annotated[str, Field(description="求解问题类型")],
    language: Annotated[str, Field(description="API接口语言")]
    ) -> str:
    """
    获取COPT的指定语言接口对应问题的参考示例,推荐在调用COPT解决对应问题前调用
    
    Args:
        problem_type: 求解问题类型，目前支持的问题类型如下：
            - "LP": 线性规划(LP)
            - "MIP": 混合整数规划(MIP)
            - "SOCP": 二阶锥规划(SOCP)
            - "NLP": 非线性规划(NLP)
        language: API接口语言，目前支持的语言如下：
            - "Python": Python接口
    """

    if problem_type not in {"LP", "MIP", "SOCP", "NLP"}:
        return f"目前尚不支持问题类型为{problem_type}"
    
    if language not in {"Python"}:
        return f"目前尚不支持语言为{language}"
    
    try:
        return open(f"{resource_path}/example/{problem_type}/{language}.md", "r" ,encoding="utf-8").read()
    except FileNotFoundError:
        return "文件不存在"

@mcp.tool()
def get_api_doc(
    instructions: Annotated[str, Field(description="查询指令,支持自然语言描述与代码片段的查询")],
    language: Annotated[str, Field(description="API接口语言")],
    domain: Annotated[str, Field(description="查询指令对应的字段")],
    recall_num: Annotated[int, Field(description="查询召回数量", ge=1, le=25)],
    return_num: Annotated[int, Field(description="重排序后最终返回数量", ge=1, le=8)]
    ) -> str:
    """
    根据查询指令召回并排序最相似的API文档,在你不清楚COPT的相关API用法时,可以调用此工具
    
    Args:
        instructions: 查询指令,支持自然语言描述与代码片段的查询,参考的查询指令如下：
            - "name": 查询API名称,如"Model.addConstr()"/"Envr()"
            - "description": 查询需求描述,如"使用矩阵建模添加一组线性约束"
        language: API接口语言,目前支持的语言如下：
            - "Python": Python接口
        domain: 查询指令对应的字段,目前支持的领域如下：
            - "name": 查询API名称
            - "description": 查询API描述
        recall_num: 查询召回数量,默认为10,最大为25
        return_num: 重排序后最终返回数量,默认为3,最大为8
    
    Hints:
        - 在能够明确API名称时，优先选择"name"字段
        - 在希望精准查询特定API时，推荐选择"name"字段
        - 在希望根据需求描述模糊查询时，推荐选择"description"字段
    """
    dim_map = config["dim_map"]

    if language not in {"Python"}:
        return f"目前尚不支持语言为{language}"
    if domain not in dim_map:
        return f"目前尚不支持字段为{domain}"
    if recall_num > 25 or recall_num < 1:
        return "召回数量必须在1到25之间"
    if return_num > 8 or return_num < 1:
        return "重排序后最终返回数量必须在1到8之间"
    
    try:
        # 加载数据库
        db = sqlite3.connect(f"{resource_path}/api_doc/{language}/vector.db")
        db.enable_load_extension(True)
        sqlite_vec.load(db)
        # 召回
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
            [get_embedding(config["embedding"], instructions, dim_map[domain])],
        ).fetchall()
        result_id = ",".join([str(rowid) for rowid, _ in rows])
        result_recall = db.execute(f"""
                                   SELECT name, description, code 
                                   FROM api_doc 
                                   WHERE rowid IN ({result_id})
                                   """).fetchall()
        # 重排序
        if domain == "description":
            result_idx = get_reranker(config["reranker"], instructions, [description for _, description, _ in result_recall], return_num)
        else:
            result_idx = get_reranker(config["reranker"], instructions, [name for name, _, _ in result_recall], return_num)
        reranker_result = [result_recall[idx] for idx in result_idx]
        # 返回格式化后的结果
        return "\n".join([contact_result(name, description, code) 
                          for name, description, code in reranker_result])

    except Exception as e:
        return f"发生错误: {e}"
    finally:
        db.close()

if __name__ == "__main__":
    mcp.run(transport="stdio")