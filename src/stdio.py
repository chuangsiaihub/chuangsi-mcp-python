import os
from .server import create_server  

def stdio_server():
    print('正在启动（STDIO）服务器...')
    # 获取环境变量
    env = os.environ
    api_key = env.get('API_KEY','')
    strategy_key = env.get('STRATEGY_KEY','')
    
    # # 检查必要的环境变量
    # if not api_key or not strategy_key:
    #     raise ValueError("API_KEY 和 STRATEGY_KEY 环境变量必须设置")
    
    # 同步调用，无需 await
    server_instance = create_server(api_key, strategy_key)
    server_instance.run(transport="stdio")

