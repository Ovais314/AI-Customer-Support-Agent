from services.llm_service import llm


class IntentService:

    @staticmethod
    def classify(question: str):
        prompt = f"""
        You are an intent classification AI.

        Your task is to classify the user's question.

        Rules:

        - Return SUPPORT if the user is asking for help related to a company's:
        - products
        - services
        - orders
        - payments
        - refunds
        - account
        - login
        - subscription
        - technical issues
        - customer support

        - Return GENERAL if the question is unrelated to customer support.

        Return ONLY one word.

        SUPPORT
        or
        GENERAL

        User Question:
        {question}
        """

        response = llm.invoke(prompt)

        return response.content.strip().upper()