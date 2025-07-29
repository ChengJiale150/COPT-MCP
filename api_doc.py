from tqdm import tqdm
import sqlite3, sqlite_vec, json
import os
from concurrent.futures import ThreadPoolExecutor
from utils.embedding import get_embedding
from utils.env import Env

current_dir = os.path.dirname(os.path.abspath(__file__))
resource_path = os.path.join(current_dir, "resource", 'api_doc')
env = Env()
with open(os.path.join(current_dir, "config.json"), "r", encoding="utf-8") as f:
    config = json.load(f)
dim_map = config["dim_map"]

def create_api_doc_table(db):
    db.execute(f"CREATE VIRTUAL TABLE name_vec USING vec0(embedding float[{dim_map['name']}])")
    db.execute(f"CREATE VIRTUAL TABLE description_vec USING vec0(embedding float[{dim_map['description']}])")
    db.execute(f"CREATE VIRTUAL TABLE code_vec USING vec0(embedding float[{dim_map['code']}])")
    db.execute("CREATE TABLE api_doc (rowid INTEGER PRIMARY KEY, name TEXT, description TEXT, code TEXT)")

def insert_api_doc(db, item):
    # 并发获取所有 embedding
    with ThreadPoolExecutor(max_workers=3) as executor:
        name_future = executor.submit(get_embedding, env, item["name"], dim_map["name"])
        description_future = executor.submit(get_embedding, env, item["description"], dim_map["description"])
        code_future = executor.submit(get_embedding, env, item["code"], dim_map["code"])
        
        # 等待所有 embedding 完成
        name_embedding = name_future.result()
        description_embedding = description_future.result()
        code_embedding = code_future.result()
    
    # 串行插入数据库（保证数据一致性）
    db.execute(
        "INSERT INTO api_doc(rowid, name, description, code) VALUES (?, ?, ?, ?)",
        [item["rowid"], item["name"], item["description"], item["code"]]
    )
    db.execute(
        "INSERT INTO name_vec(rowid, embedding) VALUES (?, ?)",
        [item["rowid"], name_embedding]
    )
    db.execute(
        "INSERT INTO description_vec(rowid, embedding) VALUES (?, ?)",
        [item["rowid"], description_embedding]
    )
    db.execute(
        "INSERT INTO code_vec(rowid, embedding) VALUES (?, ?)",
        [item["rowid"], code_embedding]
    )
    db.commit()


if __name__ == "__main__":
    language = "Python"
    env.activate()
    db = sqlite3.connect(f"{resource_path}/{language}/vector.db")
    db.enable_load_extension(True)
    sqlite_vec.load(db)
    # 检查是否存在表
    if not db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_doc'").fetchone():
        create_api_doc_table(db)
        print("表创建成功")
    else:
        print("表已存在")
    
    raw_data = json.load(open(f"{resource_path}/{language}/raw_data.json", "r", encoding="utf-8"))
    
    for item in tqdm(raw_data):
        fetch = db.execute("SELECT * FROM api_doc WHERE rowid = ?", [item["rowid"]]).fetchone()
        if fetch:
            continue
        insert_api_doc(db, item)
    
    db.close()