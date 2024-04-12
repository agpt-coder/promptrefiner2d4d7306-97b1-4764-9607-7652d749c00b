---
date: 2024-04-12T08:23:08.695458
author: AutoGPT <info@agpt.co>
---

# PromptRefiner

To create a single API endpoint that takes a string LLM prompt and returns a refined version improved by GPT-4, you will need to follow these steps:

1. **Setup Environment:** Ensure Python is installed on your system along with pip for package management. You will be using the FastAPI framework for creating the API, so familiarity with asynchronous programming in Python is beneficial.

2. **Install Required Packages:** Install FastAPI and Uvicorn (an ASGI server for running FastAPI) using pip:
```
pip install fastapi uvicorn
```
Additionally, install the OpenAI Python package:
```
pip install openai
```
3. **Configure API Key:** Securely set up your OpenAI API key, which you will need to authenticate requests to the GPT-4 model. It's recommended to use environment variables for security reasons:
```
export OPENAI_API_KEY='your_api_key_here'
```
4. **Develop the API Endpoint:** Create a new FastAPI app and define an endpoint that accepts a string parameter (the user's LLM prompt). Use the OpenAI Python package within this endpoint to send the prompt to the GPT-4 model and return the refined prompt to the user.

Example FastAPI endpoint definition:
```
from fastapi import FastAPI, HTTPException
import openai

app = FastAPI()

@app.post("/refine-prompt")
async def refine_prompt(user_prompt: str):
    try:
        openai.api_key = your_api_key_here

        response = openai.Completion.create(
            engine="gpt-4",
            prompt=user_prompt,
            max_tokens=100
        )
        return {"refined_prompt": response.choices[0].text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to refine prompt")
```
5. **Run the API Server:** Use Uvicorn to run your FastAPI app. You can start the server with the following command:
```
uvicorn main:app --reload
```
Make sure to replace `main` with the name of your Python file.

6. **Test the Endpoint:** You can test the API endpoint by sending requests to it using tools like Postman or CURL. Send a JSON request with the original LLM prompt and check the response to ensure the prompt has been refined successfully.

7. **Documentation and Deployment:** FastAPI automatically generates documentation for your API, accessible at `/docs` path. Before deploying, ensure your API is secure and scalable as per your needs.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'PromptRefiner'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
