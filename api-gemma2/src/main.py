import torch
from fastapi import FastAPI
from transformers import pipeline

app = FastAPI(root_path="/api")
pipe = pipeline(
    "text-generation",
    model="../model",
    model_kwargs={"torch_dtype": torch.bfloat16},
)
messages = [
    {
        "role": "user",
        "content": "マシーンラーニングについての詩を書いてください。",
    },
]
outputs = pipe(messages, return_full_text=False, max_new_tokens=256)
assistant_response = outputs[0]["generated_text"].strip()


@app.get("/")
async def root():
    return {"message": assistant_response}
