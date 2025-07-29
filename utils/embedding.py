from typing import List
import struct, requests
from utils.env import Env

def get_embedding(env: Env, text: str, dim: int = 128) -> bytes:
        def serialize_f32(vector: List[float]) -> bytes:
            return struct.pack("%sf" % len(vector), *vector)
        url = env["EMB_URL"]
        api_key = env["EMB_API_KEY"]
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
        return contact_format.format(name=name, description=description, code=code)
