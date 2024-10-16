#!/bin/bash

source .env.public
source .env.secret

mkdir -p "$1"
git lfs install
git clone https://USER:${HF_TOKEN}@huggingface.co/${MODEL_NAME} "$1"
unset HF_TOKEN
