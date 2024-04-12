import os

import openai
from pydantic import BaseModel


class RefinePromptResponse(BaseModel):
    """
    The response model for the refine prompt endpoint, detailing the original and the refined text.
    """

    original_text: str
    refined_text: str
    status_message: str


def refine_prompt(user_id: str, prompt_text: str) -> RefinePromptResponse:
    """
    Refines a given text prompt using GPT-4 and returns the refined version.

    Args:
        user_id (str): The unique identifier for the user sending the prompt.
        prompt_text (str): The original text prompt provided by the user to be refined.

    Returns:
        RefinePromptResponse: The response model for the refine prompt endpoint, detailing the original and the refined text.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_text,
            max_tokens=100,
            temperature=0.7,
        )  # TODO(autogpt): "Completion" is not exported from module "openai". reportPrivateImportUsage
        refined_text = (
            response["choices"][0]["text"].strip() if response["choices"] else ""
        )  # TODO(autogpt): "__getitem__" method not defined on type "Generator[Unknown | list[Unknown] | dict[Unknown, Unknown], None, None]". reportIndexIssue
        return RefinePromptResponse(
            original_text=prompt_text,
            refined_text=refined_text,
            status_message="Success"
            if refined_text
            else "Failure: No refined text generated.",
        )
    except Exception as e:
        return RefinePromptResponse(
            original_text=prompt_text,
            refined_text="",
            status_message=f"Failed to refine prompt due to: {str(e)}",
        )
