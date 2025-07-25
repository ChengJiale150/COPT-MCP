from fastmcp import FastMCP

resource_path = "/Users/jiale.cheng/Documents/mcp/copt-mcp/resource"

mcp = FastMCP(name="COPT-MCP", 
              version="0.0.1",
              instructions='''这是COPT的MCP服务,你可以在使用COPT时调用这个服务''')

@mcp.tool()
def get_citation(citation_type: str) -> str:
    """
    获取COPT的参考引用格式
    
    Args:
        citation_type: 引用类型，包括：
            - "word": 适用于word文档
            - "bibtex": 适用于bibtex文件
    """
    if citation_type == "word":
        return open(f"{resource_path}/citation/word.txt", "r" ,encoding="utf-8").read()
    elif citation_type == "bibtex":
        return open(f"{resource_path}/citation/bibtex.txt", "r" ,encoding="utf-8").read()
    else:
        return "目前尚不支持该引用类型"

@mcp.tool()
def get_example(problem_type: str, language: str) -> str:
    """
    获取COPT的指定语言接口对应问题类型的示例,推荐在调用COPT解决对应问题前调用
    
    Args:
        problem_type: 求解问题类型，目前支持的问题类型如下：
            - "LP": 线性规划(LP)
            - "MIP": 混合整数规划(MIP)
        language: API接口语言，目前 支持的语言如下：
            - "Python": Python接口
    """
    try:
        return open(f"{resource_path}/example/{problem_type}/{language}.md", "r" ,encoding="utf-8").read()
    except FileNotFoundError:
        return "目前尚不支持该问题类型或语言"

if __name__ == "__main__":
    mcp.run(transport="stdio")