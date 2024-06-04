import pathway as pw
from common.openaiapi_helper import openai_chat_completion


def prompt(index, embedded_query, user_query,language):

    @pw.udf
    def build_prompt(local_indexed_data, query,p_lang='Python'):
        docs_str = "\n".join(local_indexed_data)
        prompt = f'''You are a competitive programming coach. 
        I will give you the user code submissions and a list of all available problems after "Data:".
        The data lines with verdict are the user code submissions. 
        The other lines are the available problems on codeforces.
        Answer the user query after looking at the user code submissions and the questions he got a wrong answer in.
        The problems you analyze and suggest should be similar in rating to the highest rated problems that the user has attempted.
        The answer should also explain how you arrived at the answer looking at the user code submissions if necessary.
        Example query : "What problems should I practice next?"
        Ideal Answer : "Looking at your submissions, you solve questions rated around 1500 and you are facing difficulty in implementing binary search. 
        So here are some binary search problems you can practice: [Links to Binary search problems]."
        Example query : "How to implement dynamic programming?"
        Ideal Answer : "Here's an implementation of dynamic programming. [Dynamic Programming Code].
        If user asks for any code, it should be in {p_lang}.\n
        Data: \n {docs_str} \nAnswer this query: {query}.'''

        return prompt

    query_context = embedded_query + index.get_nearest_items(
        embedded_query.vector, k=5, collapse_rows=True
    ).select(local_indexed_data_list=pw.this.doc).promise_universe_is_equal_to(embedded_query)
    
    prompt = query_context.select(
        prompt=build_prompt(pw.this.local_indexed_data_list, user_query,language)
    )

    return prompt.select(
        query_id=pw.this.id,    
        result=openai_chat_completion(pw.this.prompt),
    )
