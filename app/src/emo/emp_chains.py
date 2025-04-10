from typing import AsyncGenerator, Optional, Sequence, Union, Dict, Any, List
from langchain_community.agent_toolkits.load_tools import load_tools,get_all_tool_names
from langchain.agents.format_scratchpad import format_to_openai_functions
from langchain.agents import initialize_agent
from langchain.prompts import MessagesPlaceholder
from langchain.agents import AgentType
from langchain.agents import tool
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField
from langchain_core.output_parsers import StrOutputParser
import asyncio
import json


# 替换为以下代码
import sys
import os
# 确保添加的是项目根目录
current_file = os.path.abspath(__file__)
src_dir = os.path.dirname(os.path.dirname(current_file))  # app/src 目录
app_dir = os.path.dirname(src_dir)  # app 目录
project_dir = os.path.dirname(app_dir)  # 项目根目录
sys.path.insert(0, project_dir)  # 将项目根目录添加到路径最前面
# 现在可以导入
from app.src.model import get_llm
from app.src.utils.oss_util import upload_to_oss
import sys
sys.path.append(".")  # 将当前目录添加到 Python 路径

from langchain_core.messages import HumanMessage


model = "qwen-vl-plus"
temperature=0.2
class EmoChains:
    def __init__(self, llm):
        self.llm = get_llm("dashscope", model=model, temperature=temperature)
        self.judge_emo_promt = ChatPromptTemplate.from_messages([
            ("system", open('app/src/emo/promots/情绪分析.md').read()),
            ("human", "{user_input}"),
        ])

    async def analyze_image_and_text(self, text: str, image_path: str) -> str:
        ACCESS_KEY_ID = ''
        ACCESS_KEY_SECRET = ''
        BUCKET_NAME = 'my-bucket-van'
        ENDPOINT = 'oss-cn-hangzhou.aliyuncs.com'
        
        # 上传图片到OSS
        upload_result = upload_to_oss(
            image_path,
            BUCKET_NAME,
            ACCESS_KEY_ID,
            ACCESS_KEY_SECRET,
            ENDPOINT
        )
        
        if upload_result['status'] != 'success':
            raise Exception("Failed to upload image to OSS")
        
        # 构建消息
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": text
                },
                {
                    "type": "image_url",
                    "image_url": {"url": upload_result['url']}
                }
            ]
        )
        
        # 使用 ChatOpenAI 的异步调用方法
        response = await self.llm.ainvoke([message])
        return response.content

    def analyze_image_and_text_sync(self, text: str, image_path: str) -> str:
        return asyncio.run(self.analyze_image_and_text(text, image_path))



if __name__ == "__main__":
    # 测试同步调用
    def test_sync():
        print("开始测试同步调用...")
        emo_chains = EmoChains(None)
        result = emo_chains.analyze_image_and_text_sync(
            text="这张图片里有什么？请详细描述一下。", 
            image_path="app/src/source/卡通少女.png"
        )
        print("同步调用结果:", result)

    # 测试异步调用
    async def test_async():
        print("开始测试异步调用...")
        emo_chains = EmoChains(None)
        result = await emo_chains.analyze_image_and_text(
            text="这张图片的风格是怎样的？给出详细分析。", 
            image_path="app/src/source/卡通少女.png"
        )
        print("异步调用结果:", result)

    # 运行测试
    print("=== 开始测试 EmoChains 多模态功能 ===")
    
    # 执行同步测试
    test_sync()
    
    # 执行异步测试
    asyncio.run(test_async())
    
    print("=== 测试完成 ===")