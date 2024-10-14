import os

from dotenv import load_dotenv
from huggingface_hub import login
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv("../.env.public")
load_dotenv("../.env.secret")
hf_token = os.environ["HF_TOKEN"]
model_name = os.environ["MODEL_NAME"]
model_dir = os.environ["MODEL_DIR"]


def download_and_save_model():
    login(token=hf_token, add_to_git_credential=True)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    model.save_pretrained(model_dir)
    tokenizer.save_pretrained(model_dir)


if __name__ == "__main__":
    download_and_save_model()
