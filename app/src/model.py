from langchain_openai import ChatOpenAI


# 模型配置
dashscope_model = "qwen-max-latest"
dashscope_temperature=0.0 
dashscope_base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
dashscope_api_key=""

idea_model = "qwen2.5-72b-instruct"
idea_temperature=0.0 
idea_base_url=""
idea_api_key=""



# 工厂模式获取ChatOpenAI实例
def get_llm(type: str = 'dashscope', model: str = None, temperature: float = None):
    if type == "dashscope":
        return ChatOpenAI(
            model=dashscope_model if model is None else model,  
            # 若temperature = None 则取值dashscope_temperature，否则就取值 temperature
            temperature= dashscope_temperature if temperature is None else temperature,  
            base_url=dashscope_base_url,
            api_key=dashscope_api_key,
            default_headers={
                    'Connection': 'close'
                }
        )
    elif type == "idea":
        return ChatOpenAI(
            model=idea_model if model is None else model,  
            temperature=idea_temperature if temperature is None else temperature,  
            base_url=idea_base_url,
            api_key=idea_api_key,
            default_headers={
                    'Connection': 'close'
                }
        )

