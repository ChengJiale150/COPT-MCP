from typing import List, Dict, Any
import struct, requests

def get_embedding(embedding_config: Dict[str, Any], text: str, dim: int = 128) -> bytes:
    """
    获取文本的embedding
    """
    def serialize_f32(vector: List[float]) -> bytes:
        """
        将浮点数列表转换为字节串
        """
        return struct.pack("%sf" % len(vector), *vector)
    
    url = embedding_config.get("url")
    api_key = embedding_config.get("api_key")
    
    # 检查必要的配置是否存在
    if not url:
        raise ValueError("embedding.url configuration is not set or is None")
    if not api_key:
        raise ValueError("embedding.api_key configuration is not set or is None")
    
    payload = {
        "model": "Qwen/Qwen3-Embedding-8B",
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

contact_format = '''
### {name}

#### 详细描述
{description}

#### 代码示例
```
{code}
```

---
'''

def contact_result(name: str, description: str, code: str) -> str:
    """
    将API文档格式化
    """
    return contact_format.format(name=name, description=description, code=code)

def get_reranker(reranker_config: Dict[str, Any], query: str, documents: List[str], top_k: int) -> List[int]:
    """
    获取文本的重排序结果
    """
    url = reranker_config.get("url")
    api_key = reranker_config.get("api_key")
    model = reranker_config.get("model")

    if not url:
        raise ValueError("reranker.url configuration is not set or is None")
    if not api_key:
        raise ValueError("reranker.api_key configuration is not set or is None")
    if not model:
        raise ValueError("reranker.model configuration is not set or is None")

    payload = {
        "query": query,
        "documents": documents,
        "return_documents": False,
        "model": model,
        "top_n": top_k
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    return [item['index'] for item in response.json()['results']]
