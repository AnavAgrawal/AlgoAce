import pathway as pw
from common.openaiapi_helper import openai_chat_completion


def prompt(index, embedded_query, user_query,language):

    @pw.udf
    def build_prompt(local_indexed_data, query,p_lang='Python'):
        docs_str = "\n".join(local_indexed_data)
        prompt = f'''You are a competitive programming coach. 
        I will give you the user code submissions and a list of all available problems.
        Answer the user query based on the given data.
        If user asks for any code, it should be in {p_lang}.\n
        Data: \n {docs_str} \nAnswer this query: {query}.'''

        return prompt

    query_context = embedded_query + index.get_nearest_items(
        embedded_query.vector, k=3, collapse_rows=True
    ).select(local_indexed_data_list=pw.this.doc).promise_universe_is_equal_to(embedded_query)
    
    prompt = query_context.select(
        prompt=build_prompt(pw.this.local_indexed_data_list, user_query,language)
    )

    return prompt.select(
        query_id=pw.this.id,    
        result=openai_chat_completion(pw.this.prompt),
    )
