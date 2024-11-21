"""
title: Langfuse Filter Pipeline
author: open-webui
date: 2024-09-27
version: 1.4
license: MIT
description: A filter pipeline that uses Langfuse.
requirements: langfuse
"""

from typing import List, Optional
import os
import uuid
from copy import deepcopy

from utils.pipelines.main import get_last_assistant_message
from pydantic import BaseModel
from langfuse import Langfuse
from langfuse.api.resources.commons.errors.unauthorized_error import UnauthorizedError

import pprint

def get_last_assistant_message_obj(messages: List[dict]) -> dict:
    for message in reversed(messages):
        if message["role"] == "assistant":
            return message
    return {}

class Pipeline:
    class Valves(BaseModel):
        pipelines: List[str] = []
        priority: int = 0
        secret_key: str
        public_key: str
        host: str

    def __init__(self):
        self.type = "filter"
        self.name = "Langfuse Filter"
        self.valves = self.Valves(
            **{
                "pipelines": ["*"],
                "secret_key": os.getenv("LANGFUSE_SECRET_KEY", "your-secret-key-here"),
                "public_key": os.getenv("LANGFUSE_PUBLIC_KEY", "your-public-key-here"),
                "host": os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
            }
        )
        self.langfuse = None
        self.chat_generations = {}
        self.internal_chat_ids = {}  # 内部追跡用のマッピング

    async def on_startup(self):
        print(f"on_startup:{__name__}")
        self.set_langfuse()

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")
        if self.langfuse:
            self.langfuse.flush()

    async def on_valves_updated(self):
        self.set_langfuse()

    def set_langfuse(self):
        try:
            self.langfuse = Langfuse(
                secret_key=self.valves.secret_key,
                public_key=self.valves.public_key,
                host=self.valves.host,
                debug=False,
            )
            self.langfuse.auth_check()
        except UnauthorizedError:
            print(
                "Langfuse credentials incorrect. Please re-enter your Langfuse credentials in the pipeline settings."
            )
        except Exception as e:
            print(f"Langfuse error: {e} Please re-enter your Langfuse credentials in the pipeline settings.")

    async def inlet(self, body: dict, user: Optional[dict] = None) -> dict:
        print(f"-------")
        print(f"inlet:{__name__}")
        pprint.pprint(body)
        # API用のbodyをコピー
        api_body = deepcopy(body)
        
        # 内部追跡用のchat_idを生成または取得
        internal_chat_id = str(uuid.uuid4())
        self.internal_chat_ids[internal_chat_id] = body.get("chat_id")
        
        if self.langfuse:
            trace = self.langfuse.trace(
                name=f"filter:{__name__}",
                input=body,
                user_id=user["email"] if user else "anonymous",
                metadata={"user_name": user["name"] if user else "anonymous", "user_id": user["id"] if user else "anonymous"},
                session_id=internal_chat_id,
            )

            generation = trace.generation(
                name=internal_chat_id,
                model=body.get("model", "unknown"),
                input=body.get("messages", []),
                metadata={"interface": "open-webui"},
            )

            self.chat_generations[internal_chat_id] = generation
            print(trace.get_trace_url())

        # APIに送信するbodyからchat_idを削除
        if "chat_id" in api_body:
            del api_body["chat_id"]
        
        return api_body

    async def outlet(self, body: dict, user: Optional[dict] = None) -> dict:
        print(f"outlet:{__name__}")
        
        # 内部chat_idを見つける
        internal_chat_id = None
        for int_id, orig_id in self.internal_chat_ids.items():
            if orig_id == body.get("chat_id"):
                internal_chat_id = int_id
                break
                
        if internal_chat_id and internal_chat_id in self.chat_generations and self.langfuse:
            generation = self.chat_generations[internal_chat_id]
            assistant_message = get_last_assistant_message(body["messages"])
            
            usage = None
            assistant_message_obj = get_last_assistant_message_obj(body["messages"])
            if assistant_message_obj:
                info = assistant_message_obj.get("info", {})
                if isinstance(info, dict):
                    input_tokens = info.get("prompt_eval_count") or info.get("prompt_tokens")
                    output_tokens = info.get("eval_count") or info.get("completion_tokens")
                    if input_tokens is not None and output_tokens is not None:
                        usage = {
                            "input": input_tokens,
                            "output": output_tokens,
                            "unit": "TOKENS",
                        }

            # Update generation
            generation.end(
                output=assistant_message,
                metadata={"interface": "open-webui"},
                usage=usage,
            )

            # クリーンアップ
            del self.chat_generations[internal_chat_id]
            del self.internal_chat_ids[internal_chat_id]

        return body
