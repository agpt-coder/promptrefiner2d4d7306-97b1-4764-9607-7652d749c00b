import logging
from contextlib import asynccontextmanager

import project.refine_prompt_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="PromptRefiner",
    lifespan=lifespan,
    description='To create a single API endpoint that takes a string LLM prompt and returns a refined version improved by GPT-4, you will need to follow these steps:\n\n1. **Setup Environment:** Ensure Python is installed on your system along with pip for package management. You will be using the FastAPI framework for creating the API, so familiarity with asynchronous programming in Python is beneficial.\n\n2. **Install Required Packages:** Install FastAPI and Uvicorn (an ASGI server for running FastAPI) using pip:\n```\npip install fastapi uvicorn\n```\nAdditionally, install the OpenAI Python package:\n```\npip install openai\n```\n3. **Configure API Key:** Securely set up your OpenAI API key, which you will need to authenticate requests to the GPT-4 model. It\'s recommended to use environment variables for security reasons:\n```\nexport OPENAI_API_KEY=\'your_api_key_here\'\n```\n4. **Develop the API Endpoint:** Create a new FastAPI app and define an endpoint that accepts a string parameter (the user\'s LLM prompt). Use the OpenAI Python package within this endpoint to send the prompt to the GPT-4 model and return the refined prompt to the user.\n\nExample FastAPI endpoint definition:\n```\nfrom fastapi import FastAPI, HTTPException\nimport openai\n\napp = FastAPI()\n\n@app.post("/refine-prompt")\nasync def refine_prompt(user_prompt: str):\n    try:\n        openai.api_key = your_api_key_here\n\n        response = openai.Completion.create(\n            engine="gpt-4",\n            prompt=user_prompt,\n            max_tokens=100\n        )\n        return {"refined_prompt": response.choices[0].text.strip()}\n    except Exception as e:\n        raise HTTPException(status_code=500, detail="Failed to refine prompt")\n```\n5. **Run the API Server:** Use Uvicorn to run your FastAPI app. You can start the server with the following command:\n```\nuvicorn main:app --reload\n```\nMake sure to replace `main` with the name of your Python file.\n\n6. **Test the Endpoint:** You can test the API endpoint by sending requests to it using tools like Postman or CURL. Send a JSON request with the original LLM prompt and check the response to ensure the prompt has been refined successfully.\n\n7. **Documentation and Deployment:** FastAPI automatically generates documentation for your API, accessible at `/docs` path. Before deploying, ensure your API is secure and scalable as per your needs.',
)


@app.post(
    "/refine-prompt", response_model=project.refine_prompt_service.RefinePromptResponse
)
async def api_post_refine_prompt(
    user_id: str, prompt_text: str
) -> project.refine_prompt_service.RefinePromptResponse | Response:
    """
    Refines a given text prompt using GPT-4 and returns the refined version.
    """
    try:
        res = project.refine_prompt_service.refine_prompt(user_id, prompt_text)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
