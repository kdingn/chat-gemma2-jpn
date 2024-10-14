# Gemma 2 API Server
This repository contains a Dockerfile for creating an API server that utilizes the [Gemma 2 JPN Model](https://huggingface.co/google/gemma-2-2b-jpn-it). The server provides an easy-to-use interface for interacting with the Gemma 2 model.

## Prerequisites
Before building the API server, please complete the following steps:
1. Accept the Terms of Use for the Gemma 2 Model on the [Hugging Face model page](https://huggingface.co/google/gemma-2-2b-jpn-it).
2. Generate a Hugging Face access token on the [settings page](https://huggingface.co/settings/tokens).
3. Edit the token permissions to include access to the Gemma 2 JPN Model in the Repositories section.
4. Create a file named .env.secret in the root directory of this project and add your Hugging Face access token as follows:
    ```text
    HF_TOKEN="hf_your_access_token"
    ```
    Replace `hf_your_access_token` with your actual Hugging Face access token.

## Building and Running the Container
To build and run the API server container, follow these steps:
1. Build the Docker image:
```sh
docker build -t api-gemma2 .
```
2. Run the container:
```sh
docker run -d -p 8000:8000 -v $PWD/src:/app/src api-gemma2
```

Note: The build process, which includes downloading the Gemma 2 Model and setting up the Python environment, may take approximately 10 minutes or longer.

## Usage
Once the container is running, you can access the API server at http://localhost:8000.
Additionally, you can view the automatically generated API documentation by navigating to:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Refer to these documentation pages for available endpoints and usage instructions.