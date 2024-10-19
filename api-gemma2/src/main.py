import torch
from fastapi import FastAPI
from transformers import pipeline

app = FastAPI(root_path="/api")
pipe = pipeline(
    "text-generation",
    model="../model",
    model_kwargs={"torch_dtype": torch.bfloat16},
)


@app.get("/")
async def root():
    return {"response": "Hello World!"}


@app.post("/chat")
async def chat(message):
    messages = [
        {
            "role": "user",
            "content": message,
        },
    ]
    outputs = pipe(messages, return_full_text=False, max_new_tokens=256)
    assistant_response = outputs[0]["generated_text"].strip()
    return {"response": assistant_response}
