from tqdm import tqdm
import sqlite3, sqlite_vec, json
import struct, os, requests
from typing import List

current_dir = os.path.dirname(os.path.abspath(__file__))
resource_path = os.path.join(current_dir, "resource", 'api_doc')

db = sqlite3.connect(f"{resource_path}/Python/vector.db")
db.enable_load_extension(True)
sqlite_vec.load(db)

def get_embedding(text: str, dim: int = 128) -> bytes:
    def serialize_f32(vector: List[float]) -> bytes:
        return struct.pack("%sf" % len(vector), *vector)
    url = "https://api.siliconflow.cn/v1/embeddings"
    api_key = "sk-wqdksytnrhdarewmhqtxkrribdztclmzukyorzxxnncqnlcz"
    
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

# db.execute(f"CREATE VIRTUAL TABLE name_vec USING vec0(embedding float[64])")
# db.execute(f"CREATE VIRTUAL TABLE description_vec USING vec0(embedding float[512])")
# db.execute(f"CREATE VIRTUAL TABLE code_vec USING vec0(embedding float[512])")
# db.execute("CREATE TABLE api_doc (rowid INTEGER PRIMARY KEY, name TEXT, description TEXT, code TEXT)")

# raw_data = json.load(open(f"{resource_path}/Python/raw_data.json", "r", encoding="utf-8"))
# for item in tqdm(raw_data):
#     fetch = db.execute("SELECT * FROM api_doc WHERE rowid = ?", [item["rowid"]]).fetchone()
#     if fetch:
#         continue
#     db.execute(
#         "INSERT INTO api_doc(rowid, name, description, code) VALUES (?, ?, ?, ?)",
#         [item["rowid"], item["name"], item["description"], item["code"]]
#     )
#     db.execute(
#         "INSERT INTO name_vec(rowid, embedding) VALUES (?, ?)",
#         [item["rowid"], get_embedding(item["name"], 64)]
#     )
#     db.execute(
#         "INSERT INTO description_vec(rowid, embedding) VALUES (?, ?)",
#         [item["rowid"], get_embedding(item["description"], 512)]
#     )
#     db.execute(
#         "INSERT INTO code_vec(rowid, embedding) VALUES (?, ?)",
#         [item["rowid"], get_embedding(item["code"], 512)]
#     )
#     db.commit()


# items = [
#     'env = Envr()',
#     'model = env.createModel("coptprob")',
#     'env.close()',
#     """x = model.addVar()
# y = model.addVar(vtype=COPT.BINARY)
# z = model.addVar(-1.0, 1.0, 1.0, COPT.INTEGER, "z")""",
#     """x = model.addVars(1, 2, 3, vtype=COPT.INTEGER)
# tl = tuplelist([(0, 1), (1, 2)])
# y = model.addVars(tl, nameprefix="tl")""",
#     'model.addMVar((2, 3), lb=0.0, nameprefix="mx")'    
# ]

query = 'y = model.addVar(lb=0.2, ub=1.5, name="y")'

rows = db.execute(
    """
      SELECT
        rowid,
        distance
      FROM code_vec
      WHERE embedding MATCH ?
      ORDER BY distance
      LIMIT 3
    """,
    [get_embedding(query, 512)],
).fetchall()

result_id = ",".join([str(rowid) for rowid, _ in rows])
result_recall = db.execute(f"SELECT name, description, code FROM api_doc WHERE rowid IN ({result_id})").fetchall()


result = ""
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

for name, description, code in result_recall:
    result += contact_result(name, description, code)

print(result)

db.close()