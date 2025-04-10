import os
import sys
from pathlib import Path

def setup_project_env():
    # 查找项目根目录 (包含.env文件的目录)
    current = Path(__file__).resolve()
    while current != current.parent:
        if (current / '.env').exists():
            # 将项目根目录添加到sys.path
            sys.path.insert(0, str(current))
            return
        current = current.parent
    raise FileNotFoundError("找不到项目根目录(.env文件不存在)")

setup_project_env()