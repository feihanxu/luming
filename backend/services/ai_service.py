import os
import httpx
import json
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from database import Person, Record, Todo

class AIService:
    def __init__(self):
        self.api_key = os.getenv("GLM_API_KEY", "")
        self.api_url = os.getenv("API_URL", "https://open.bigmodel.cn/api/paas/v4/chat/completions")
        self.model = os.getenv("AI_MODEL", "glm-4")
        self.conversation_state: Dict[str, Any] = {}
    
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
        system_prompt = """你是鹿鸣的人脉助手"呦呦"，性格活泼可爱，喜欢用"呀"、"呢"、"哦"等语气词。

你的任务是帮助用户记录人脉见面的信息。你需要通过自然对话收集以下信息：
- 人物姓名（必须）
- 见面地点
- 讨论事项
- 待办事项
- 其他备注

重要规则：
1. 如果用户只说了见了谁，要追问"在哪里见面呀？"或"聊了什么呢？"
2. 如果用户说了地点但没说内容，要追问"聊了什么呀？"
3. 收集到基本信息后，生成一个预览卡片让用户确认
4. 只有用户确认后才保存

返回格式必须是 JSON：
{
    "action": "ask" | "preview" | "saved",
    "response": "回复用户的话",
    "data": {
        "person_name": "姓名",
        "person_title": "职位",
        "person_company": "公司",
        "location": "地点",
        "topic": "事项",
        "todo": "待办",
        "note": "备注",
        "summary": "一句话总结"
    }
}

示例对话：
用户：今天见了张总
返回：{"action": "ask", "response": "好的呀，和张总见面了呢！在哪里见面的呀？聊了什么？", "data": {"person_name": "张总"}}

用户：在星巴克，聊了新项目合作
返回：{"action": "preview", "response": "我帮你整理了一下，看看对不对呀~", "data": {"person_name": "张总", "location": "星巴克", "topic": "新项目合作", "summary": "和张总在星巴克讨论新项目合作"}}"""
        
        ai_response = await self.call_api(message, system_prompt)
        
        result = {
            "response": ai_response,
            "action": "ask",
            "draft": None,
            "record": None
        }
        
        try:
            if "{" in ai_response and "}" in ai_response:
                start = ai_response.index("{")
                end = ai_response.rindex("}") + 1
                data = json.loads(ai_response[start:end])
                
                result["action"] = data.get("action", "ask")
                result["response"] = data.get("response", ai_response)
                
                if data.get("data"):
                    result["draft"] = data["data"]
                    
                    if result["action"] == "preview":
                        result["draft"]["id"] = f"draft_{int(__import__('time').time())}"
        
        except Exception as e:
            pass
        
        return result
    
    async def confirm_save(self, draft: dict, db: Session) -> dict:
        result = {"success": False, "record": None, "message": ""}
        
        try:
            person_name = draft.get("person_name")
            if not person_name:
                result["message"] = "缺少人物姓名"
                return result
            
            person = db.query(Person).filter(Person.name == person_name).first()
            
            if not person:
                person = Person(
                    name=person_name,
                    title=draft.get("person_title"),
                    company=draft.get("person_company")
                )
                db.add(person)
                db.commit()
                db.refresh(person)
            
            record = Record(
                person_id=person.id,
                person_name=person.name,
                person_title=person.title,
                person_company=person.company,
                summary=draft.get("summary", ""),
                location=draft.get("location"),
                topic=draft.get("topic"),
                todo=draft.get("todo"),
                note=draft.get("note"),
                raw_input=draft.get("raw_input", "")
            )
            db.add(record)
            
            if draft.get("todo"):
                todo = Todo(
                    person_id=person.id,
                    record_id=record.id,
                    content=draft["todo"],
                    record_date=record.timestamp
                )
                db.add(todo)
            
            person.last_contact = record.timestamp
            person.meeting_count = (person.meeting_count or 0) + 1
            
            db.commit()
            db.refresh(record)
            
            result["success"] = True
            result["record"] = {
                "id": record.id,
                "personName": record.person_name,
                "location": record.location,
                "topic": record.topic,
                "todo": record.todo,
                "summary": record.summary
            }
            result["message"] = "保存成功啦！"
            
        except Exception as e:
            result["message"] = f"保存失败: {str(e)}"
        
        return result
    
    async def process_image(self, file_path: str, description: Optional[str], db: Session) -> dict:
        return {
            "response": "收到照片啦！这是和谁见面呀？",
            "action": "ask",
            "draft": None
        }
    
    async def process_audio(self, file_path: str, description: Optional[str], db: Session) -> dict:
        return {
            "response": "我听完啦！让我帮你整理一下这次见面~",
            "action": "ask",
            "draft": None
        }
