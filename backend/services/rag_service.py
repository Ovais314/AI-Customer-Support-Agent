from services.llm_service import llm
from services.vector_service import vector_store
from services.database_service import (
    save_conversation,
    get_conversation_history,
)
from services.ticket_service import TicketService
from services.intent_service import IntentService

CONFIDENCE_THRESHOLD = 0.90


def ask_question(
    session_id: str,
    question: str
):

    # Get previous conversation
    history = get_conversation_history(session_id)

    conversation_history = ""

    for q, a in history:
        conversation_history += f"User: {q}\n"
        conversation_history += f"Assistant: {a}\n\n"

    results = vector_store.similarity_search_with_score(
        query=question,
        k=3
    )

    best_score = results[0][1]

    if best_score > CONFIDENCE_THRESHOLD:

        intent = IntentService.classify(question)

        if intent == "GENERAL":

            answer = (
                "I'm here to assist with questions related to our company's "
                "products and services. I couldn't find that information in "
                "our knowledge base."
            )

            save_conversation(
                session_id=session_id,
                question=question,
                answer=answer
            )

            return {
                "answer": answer,
                "sources": [],
                "ticket_created": False,
                "ticket_id": None
            }

        ticket = TicketService.create_ticket(
            session_id=session_id,
            issue=question
        )

        ticket_id = ticket["ticket_id"]
        ticket_created = ticket["created"]

        if ticket_created:
            answer = (
                "I couldn't find that information in the knowledge base.\n\n"
                "A support ticket has been created for you.\n"
                f"Ticket ID: #{ticket_id}"
            )
        else:
            answer = (
                "I couldn't find that information in the knowledge base.\n\n"
                "An existing support ticket is already open for this issue.\n"
                f"Ticket ID: #{ticket_id}"
            )

        save_conversation(
            session_id=session_id,
            question=question,
            answer=answer
        )

        return {
            "answer": answer,
            "sources": [],
            "ticket_created": ticket_created,
            "ticket_id": ticket_id
        }

    sources = []

    for doc, score in results:
        source = {
            "document": doc.metadata.get("source", "Unknown"),
            "page": doc.metadata.get("page_label", doc.metadata.get("page", "N/A"))
        }

        if source not in sources:
            sources.append(source)

    context = "\n\n".join(
        [doc.page_content for doc, score in results]
    )

    prompt = f"""
You are an enterprise AI customer support assistant.

The Knowledge Base is the PRIMARY source of truth.

Use the Conversation History ONLY to understand follow-up questions,
pronouns, and references such as:
- it
- they
- those
- he
- she
- that

Never use the Conversation History to replace or override information
found in the Knowledge Base.

If the Knowledge Base contains the answer, always answer using the
Knowledge Base.

If the Knowledge Base does NOT contain the answer, but the user is asking
a follow-up question that can be answered from the Conversation History,
use the Conversation History.

If neither the Knowledge Base nor the Conversation History contains the
answer, reply exactly:

"I couldn't find that information in the knowledge base."

------------------------
Conversation History
(Reference only)
------------------------

{conversation_history}

------------------------
Knowledge Base
(Source of Truth)
------------------------

{context}

------------------------
Current Question
------------------------

{question}

Answer:
"""

    response = llm.invoke(prompt)

    answer = response.content.strip()

    # If LLM could not answer, decide whether to create a support ticket
    
    fallback_detected = (
        "I couldn't find that information in the knowledge base"
        in answer
    )

    if fallback_detected:

        intent = IntentService.classify(question)

        if intent != "GENERAL":

            ticket = TicketService.create_ticket(
                session_id=session_id,
                issue=question
            )

            ticket_id = ticket["ticket_id"]
            ticket_created = ticket["created"]

            if ticket_created:
                answer = (
                    "I couldn't find that information in the knowledge base.\n\n"
                    "A support ticket has been created for you.\n"
                    f"Ticket ID: #{ticket_id}"
                )
            else:
                answer = (
                    "I couldn't find that information in the knowledge base.\n\n"
                    "An existing support ticket is already open for this issue.\n"
                    f"Ticket ID: #{ticket_id}"
                )

            save_conversation(
                session_id=session_id,
                question=question,
                answer=answer
            )
    
            return {
                "answer": answer,
                "sources": [],
                "ticket_created": ticket_created,
                "ticket_id": ticket_id
            }

    save_conversation(
        session_id=session_id,
        question=question,
        answer=answer
    )

    return {
        "answer": answer,
        "sources": sources,
        "ticket_created": False,
        "ticket_id": None
    }