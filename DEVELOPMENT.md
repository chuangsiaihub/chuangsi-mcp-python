### 初始化

uv init . -p 3.12

### 安装依赖

uv add "mcp[cli]"
uv add "chuangsiai-sdk"

### 进入虚拟环境

source .venv/bin/activate

### 开发运行

mcp dev main.py
uv run main.py

### 在线调试

npx @modelcontextprotocol/inspector uv
