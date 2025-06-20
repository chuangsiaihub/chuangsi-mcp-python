from mcp.server.fastmcp import FastMCP
from chuangsiai_sdk import ChuangsiaiClient

def create_server(api_key: str, strategy_key: str):
    """
    创建包含输入输出安全护栏工具的服务器
    
    参数:
        api_key: 创思爱客户端的认证头
        strategy_key: 护栏检查的策略键
        
    返回:
        dict: 包含服务器实例的字典
    """
    # 创建 FastMCP 服务器实例
    server = FastMCP(
        name="chuangsiai/safety-guardrail",
        version="1.0.0",
        capabilities={
            "resources": {},
            "tools": {},
        }
    )

    # 注册工具：文本安全检测
    @server.tool()
    def input_guardrail(content: str) -> dict | str:
        """
判断用户输入是否安全，每一轮对话对于用户的输入都要调用该函数
如果工具返回的结果为suggestion：pass，表示问题安全，你可以放心地回答。如果返回的结果为 block，表示问题可能不安全，你需要格外小心，避免直接回答可能导致风险的内容。此时，应尝试将回答引导至更积极的方向，或建议用户提供可靠的替代方案。
:param content: 用户输入
:return suggestion: 安全性判断结果 score：分数 label：命中的类型，没命中为空 labelName：中文类型名称，没命中为空
        """
        # 检查输入内容是否为空
        if not content:
            return "请提供检查内容"

        client = ChuangsiaiClient(api_key=api_key)
        resp = client.input_guardrail(strategy_key=strategy_key, content=content)
        if resp.get("code", 0) != 0:
            return resp.get("message", "未知错误")
        
        suggestion = resp["suggestion"]
        labelName = resp.get("labelName", "")
        label = resp.get("label", "")
        score = resp["score"]
        return {
            "suggestion": suggestion,
            "labelName": labelName,
            "label": label,
            "score": score
        }


    # 注册工具：文本安全检测
    @server.tool()
    def output_guardrail(content: str) -> dict | str:
        """
判断大模型输出是否安全，每一轮对话最后的时候对于模型的输出。都要调用该函数
如果工具返回的结果为suggestion：pass，表示问题安全，你可以放心地回答。如果返回的结果为 block，表示问题可能不安全，你需要格外小心，避免直接回答可能导致风险的内容。此时，应尝试将回答引导至更积极的方向，或建议用户提供可靠的替代方案。
:param content: 模型的回复
:return suggestion: 安全性判断结果 score：分数 label：命中的类型，没命中为空 labelName：中文类型名称，没命中为空
        """
        # 检查输入内容是否为空
        if not content:
            return "请提供检查内容"

        client = ChuangsiaiClient(api_key=api_key)
        resp = client.output_guardrail(strategy_key=strategy_key, content=content)
        if resp.get("code", 0) != 0:
            return resp.get("message", "未知错误")
        
        suggestion = resp["suggestion"]
        labelName = resp.get("labelName", "")
        label = resp.get("label", "")
        score = resp["score"]
        return {
            "suggestion": suggestion,
            "labelName": labelName,
            "label": label,
            "score": score
        }

    return server