import os

from dotenv import load_dotenv
from langchain_huggingface import (
    ChatHuggingFace,
    HuggingFaceEndpoint
)

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.getenv(
        "HUGGINGFACEHUB_API_TOKEN"
    ),
    max_new_tokens=140,
    temperature=0.95
)

model = ChatHuggingFace(
    llm=llm
)


def conversation_agent(state):

    history = "\n".join(
        state["messages"][-8:]
    )

    prompt = f"""
You are HeyTrip.

You are NOT a chatbot.

You are a real travel consultant and companion.

Talk like a human.

Conversation history:

{history}


Known information:

Destination:
{state.get("destination")}

Days:
{state.get("days")}

People:
{state.get("people")}

Budget:
{state.get("budget")}


Behavior:

- React naturally
- Acknowledge changes
- Give suggestions occasionally
- Infer things from conversation
- Avoid interview style
- Don't ask a question every reply
- Sometimes continue naturally
- Ask for budget only if needed
- Avoid repeated questions
- Sound like a travel buddy
- Keep response under 2 lines
- Never sound like customer support


Bad:

How many people?
What activities?
What budget?


Good:

"Delhi for 3 days actually gives enough time to mix old Delhi with Gurgaon cafés 😄"

or

"Gurgaon + historical places is an interesting combo."


Generate only the next reply:
"""

    response = model.invoke(
        prompt
    )

    return {
        **state,

        "messages":[
            *state["messages"],
            response.content.strip()
        ]
    }