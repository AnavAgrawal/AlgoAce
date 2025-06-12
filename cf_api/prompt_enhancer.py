import os
import openai
from openai import OpenAI
client = OpenAI()

openai.api_key = os.getenv("OPENAI_API_KEY")

def enhance_query(user_query: str) -> str:

    system_prompt = (
        "You are a query rewriting assistant for a competitive programming tool. "
        "The goal is to rewrite user queries so that they include concrete terms that match problem metadata stored in a database. "
        "The database retrieves problems based on word overlap with the query — so include exact terms like problem 'tags' (e.g. 'greedy', 'dp', 'graphs'), "
        "verdicts (e.g. 'WRONG_ANSWER', 'OK', 'RUNTIME_ERROR'), difficulty 'ratings' (e.g. 800, 1000, 1700), or specific problem names if known. "
        "You do NOT have access to the user's past submissions, but you must guess the user's intent and include as many relevant keywords as possible "
        "to help the system match the query to relevant problems."
        "Your output should be in the following format:\n\n"
        "Retrieval terms: <insert keywords for retrieval>\n"
        "User query: <natural language query reformulated for the LLM>\n\n"
        "Make sure the retrieval terms are rich in specific tokens, and the user query is clear and helpful for the LLM."
        )   


    messages = [
        {"role": "developer", "content": system_prompt},
        {"role": "user", "content": user_query},
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"Error enhancing query: {e}")
        return user_query  # fallback to original query


# Example usage
if __name__ == "__main__":
    query = input("Enter your query: ")
    enhanced = enhance_query(query)
    print("\nEnhanced Query:")
    print(enhanced)
