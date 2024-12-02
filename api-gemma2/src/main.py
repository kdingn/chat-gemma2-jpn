import torch
from pydantic import BaseModel
from fastapi import FastAPI
from transformers import pipeline, TextIteratorStreamer
from fastapi.responses import StreamingResponse
from threading import Thread


app = FastAPI(root_path="/api-gemma2")
pipe = pipeline(
    "text-generation",
    model="../model",
    model_kwargs={"torch_dtype": torch.bfloat16},
)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    def generate(pipe, messages, streamer):
        pipe(
            messages,
            return_full_text=False,
            max_new_tokens=256,
            streamer=streamer,
        )

    def stream_response(streamer):
        for text in streamer:
            yield text

    messages = [
        {
            "role": "user",
            "content": request.message,
        },
    ]

    streamer = TextIteratorStreamer(
        pipe.tokenizer, skip_prompt=True, skip_special_tokens=True
    )

    thread = Thread(target=generate, args=(pipe, messages, streamer))
    thread.start()

    return StreamingResponse(
        stream_response(streamer), media_type="text/plain"
    )
