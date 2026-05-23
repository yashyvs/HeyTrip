import json
import re
import os

from dotenv import load_dotenv
from pydantic import ValidationError

from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint
)

from models.trip_info import TripInfo

load_dotenv()


llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",

    task="text-generation",

    huggingfacehub_api_token=os.getenv(
        "HUGGINGFACEHUB_API_TOKEN"
    ),

    max_new_tokens=150,

    temperature=0.1
)

model = ChatHuggingFace(
    llm=llm
)


def extractor_agent(state):

    user_message = state["messages"][-1]

    prompt = f"""
Extract travel information.

Return ONLY JSON.

Allowed fields:

destination
people
days
budget

Examples:

Input:
Me and 4 friends want Goa

Output:
{{
    "destination":"Goa",
    "people":4
}}

Input:
Trip for 5 days

Output:
{{
    "days":5
}}

Message:
{user_message}
"""

    response = model.invoke(
        prompt
    )

    raw = response.content

    print("\nRAW:")
    print(raw)

    extracted = {}

    try:

        # remove markdown wrappers
        cleaned = re.sub(
            r"```json|```",
            "",
            raw
        ).strip()


        match = re.search(
            r"\{.*\}",
            cleaned,
            re.DOTALL
        )


        if match:

            data = json.loads(
                match.group()
            )


            validated = TripInfo(
                **data
            )


            extracted = (
                validated.model_dump(
                    exclude_none=True
                )
            )

    except (
        json.JSONDecodeError,
        ValidationError,
        Exception
    ) as e:

        print(
            "\nERROR:"
        )

        print(e)


    updated = {

        **state
    }

    updated.update(
        extracted
    )


    print(
        "\nSTATE:"
    )

    print(
        updated
    )


    return updated