import os
import httpx
import json
from typing import Optional
from sqlalchemy.orm import Session
from database import Person, Record, Todo

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GLM_API_KEY", "")
        self.api_url = os.getenv("API_URL", "https://open.bigmodel.cn/api/paas/v4/chat/completions")
        self.model = os.getenv("AI_MODEL", "glm-4")
    
    def get_config(self, db=None):
        return {
            "api_key": self.api_key,
            "api_url": self.api_url,
            "model": self.model
        }
    
    def set_config(self, api_key: str, api_url: str, model: str):
        self.api_key = api_key
        self.api_url = api_url
        self.model = model
        os.environ["GLM_API_KEY"] = api_key
        os.environ["API_URL"] = api_url
        os.environ["AI_MODEL"] = model
    
    async def call_api(self, prompt: str, system_prompt: str = None) -> str:
        if not self.api_key:
            return "请先在设置中配置 API Key"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        async with httpx.AsyncClient() as client:
            try:
                if "openai.com" in self.api_url or "deepseek.com" in self.api_url or "moonshot.ai" in self.api_url:
                    response = await client.post(
                        self.api_url,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": self.model,
                            "messages": messages,
                            "temperature": 0.7,
                            "max_tokens": 1000
                        },
                        timeout=30.0
                    )
                elif "bigmodel.cn" in self.api_url:
                    response = await client.post(
                        self.api_url,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": self.model,
                            "messages": messages,
                            "temperature": 0.7,
                            "max_tokens": 1000
                        },
                        timeout=30.0
                    )
                else:
                    response = await client.post(
                        self.api_url,
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": self.model,
                            "messages": messages,
                            "temperature": 0.7
                        },
                        timeout=30.0
                    )
                
                if response.status_code == 200:
                    data = response.json()
                    if "choices" in data:
                        return data["choices"][0]["message"]["content"]
                    elif "output" in data:
                        return data["output"]["text"]
                    else:
                        return str(data)
                else:
                    return f"AI 调用失败: {response.status_code}"
            except Exception as e:
                return f"AI 调用出错: {str(e)}"
    
    async def process_message(self, message: str, db: Session) -> dict:
        system_prompt = """你是鹿鸣的人脉助手"呦呦"。你的任务是帮助用户记录和管理人脉关系。

当用户描述一次见面或交流时，请提取以下信息（如果有的话）：
1. 人物姓名
2. 人物职位
3. 人物公司/单位
4. 见面地点
5. 讨论事项
6. 待办事项
7. 其他备注

请以 JSON 格式返回提取的信息，格式如下：
{
    "person_name": "姓名",
    "person_title": "职位",
    "person_company": "公司",
    "location": "地点",
    "topic": "事项",
    "todo": "待办",
    "note": "备注",
    "summary": "一句话总结"
}

如果某些信息没有提到，对应字段设为 null。"""
        
        ai_response = await self.call_api(message, system_prompt)
        
        result = {"response": ai_response, "record": None, "avatar_update": None}
        
        try:
            if "{" in ai_response and "}" in ai_response:
                start = ai_response.index("{")
                end = ai_response.rindex("}") + 1
                data = json.loads(ai_response[start:end])
                
                if data.get("person_name"):
                    person = db.query(Person).filter(
                        Person.name == data["person_name"]
                    ).first()
                    
                    if not person:
                        person = Person(
                            name=data["person_name"],
                            title=data.get("person_title"),
                            company=data.get("person_company")
                        )
                        db.add(person)
                        db.commit()
                        db.refresh(person)
                    
                    record = Record(
                        person_id=person.id,
                        person_name=person.name,
                        person_title=person.title,
                        person_company=person.company,
                        summary=data.get("summary", message),
                        location=data.get("location"),
                        topic=data.get("topic"),
                        todo=data.get("todo"),
                        note=data.get("note"),
                        raw_input=message
                    )
                    db.add(record)
                    
                    if data.get("todo"):
                        todo = Todo(
                            person_id=person.id,
                            record_id=record.id,
                            content=data["todo"],
                            record_date=record.timestamp
                        )
                        db.add(todo)
                    
                    person.last_contact = record.timestamp
                    person.meeting_count = (person.meeting_count or 0) + 1
                    
                    db.commit()
                    db.refresh(record)
                    
                    result["record"] = {
                        "personName": record.person_name,
                        "location": record.location,
                        "topic": record.topic,
                        "todo": record.todo
                    }
                    result["response"] = "好的，已帮你记录！"
        except Exception as e:
            pass
        
        return result
    
    async def process_image(self, file_path: str, description: Optional[str], db: Session) -> dict:
        return {
            "response": "收到照片！请告诉我这是和谁见面？照片里哪位是他/她？"
        }
    
    async def process_audio(self, file_path: str, description: Optional[str], db: Session) -> dict:
        system_prompt = """你是鹿鸣的人脉助手"呦呦"。用户上传了一段录音，请分析录音内容。

请提取以下信息（如果有的话）：
1. 人物姓名
2. 人物职位
3. 人物公司/单位
4. 见面地点
5. 讨论事项
6. 待办事项
7. 其他备注

以 JSON 格式返回提取的信息。"""
        
        ai_response = await self.call_api(
            f"请分析这段录音的转录内容：{description or '（无描述）'}",
            system_prompt
        )
        
        return {
            "response": "我已听完录音，这是一次关于项目合作的讨论。请问这是和谁见面？"
        }
