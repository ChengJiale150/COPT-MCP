import os
from dotenv import dotenv_values
from typing import Optional, Dict, Any

class Env:
    def __init__(self, env_file: str = "./.env"):
        """
        初始化环境变量配置
        :param env_file: .env文件路径，默认当前目录下的.env文件
        """
        self.env_vars: Dict[str, str] = dotenv_values(env_file)
        self._original_env: Dict[str, str] = os.environ.copy()  # 保存原始环境快照

    def activate(self, report:bool=False) -> None:
        """
        将配置的环境变量激活到系统环境
        - 保留原始环境变量（仅新增/覆盖配置中存在的变量）
        - 生成环境变量变更报告
        """
        changed_vars = {}
        
        for key, value in self.env_vars.items():
            if os.getenv(key) != value:
                changed_vars[key] = {
                    "from": os.getenv(key),
                    "to": value
                }
            os.environ[key] = value
        
        if changed_vars and report:
            print("[EnvConfig] 环境变量更新报告：")
            for var, changes in changed_vars.items():
                print(f"  {var}: {changes['from']} → {changes['to']}")

    def __getitem__(self, key: str) -> Optional[str]:
        """支持env_config['KEY']形式获取值"""
        return self.env_vars.get(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """支持env_config['KEY'] = value形式设置值（仅内存）"""
        self.env_vars[key] = str(value)  # 统一转换为字符串存储

    def restore(self) -> None:
        """
        恢复系统环境到初始化时的状态
        - 移除激活时新增的变量
        - 恢复激活时被覆盖的变量
        """
        # 删除新增的环境变量
        for key in set(os.environ) - set(self._original_env):
            del os.environ[key]
        
        # 恢复被修改的环境变量
        for key, value in self._original_env.items():
            if os.getenv(key) != value:
                os.environ[key] = value

    def get_config(self) -> Dict[str, str]:
        """获取当前内存中的完整配置"""
        return self.env_vars.copy()

    def __repr__(self) -> str:
        return f"EnvConfig(env_file='...', vars={list(self.env_vars.keys())})"