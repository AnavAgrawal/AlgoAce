import logging

import pathway as pw
from pathway.xpacks.llm.question_answering import SummaryQuestionAnswerer
from pathway.xpacks.llm.servers import QASummaryRestServer
from pydantic import BaseModel, ConfigDict, InstanceOf
from pathway.xpacks.llm import llms

from dotenv import load_dotenv
load_dotenv()


# To use advanced features with Pathway Scale, get your free license key from
# https://pathway.com/features and paste it below.
# To use Pathway Community, comment out the line below.
pw.set_license_key("demo-license-key-with-telemetry")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger("RAG-Logger")
file_handler = logging.FileHandler("rag_contexts_prompts.log")
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


class App(BaseModel):
    question_answerer: InstanceOf[SummaryQuestionAnswerer]
    host: str = "0.0.0.0"
    port: int = 8000

    with_cache: bool = True
    terminate_on_error: bool = False

    def run(self) -> None:
        server = QASummaryRestServer(self.host, self.port, self.question_answerer)
        server.run(
            with_cache=self.with_cache,
            terminate_on_error=self.terminate_on_error,
            cache_backend=pw.persistence.Backend.filesystem("Cache"),
        )

    model_config = ConfigDict(extra="forbid")

@pw.udf
def json_as_bytes(data):
    return str(data).encode("utf-8")

def json_encode(table):
    return table.with_columns(
        data=json_as_bytes(pw.this.data))

@pw.udf
def _prepare_RAG_response(
    response: str, docs: list[dict], return_context_docs: bool
) -> pw.Json:
    api_response: dict = {"response": response}
    if return_context_docs:
        api_response["context_docs"] = docs

    return pw.Json(api_response)

class TwoDocQuestionAnswerer(pw.xpacks.llm.question_answering.BaseRAGQuestionAnswerer):
    def __init__(self, *args, indexer_2=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.indexer_2 = indexer_2

    @pw.table_transformer
    def answer_query(self, pw_ai_queries: pw.Table) -> pw.Table:
        """Answer a question based on the available information."""

        pw_ai_results = pw_ai_queries + self.indexer.retrieve_query(
            pw_ai_queries.select(
                metadata_filter=pw.this.filters,
                filepath_globpattern=pw.cast(str | None, None),
                query=pw.this.prompt,
                k=self.search_topk//2,
            )
        ).select(
            docs=pw.this.result,
        )
        
        pw_ai_results += self.indexer_2.retrieve_query(
            pw_ai_queries.select(
                metadata_filter=pw.this.filters,
                filepath_globpattern=pw.cast(str | None, None),
                query=pw.this.prompt,
                k=self.search_topk//2,
            )
            ).select(
                docs_2=pw.this.result,
            )

        
        pw_ai_results += pw_ai_results.select(
            context=self.docs_to_context_transformer(pw.this.docs)+self.docs_to_context_transformer(pw.this.docs_2)
        )


        pw_ai_results += pw_ai_results.select(
            rag_prompt=self.prompt_udf(pw.this.context, pw.this.prompt)
        )

        # ✅ Log context and prompt before calling LLM
        @pw.udf
        def log_context_and_prompt(context, prompt):
            # logger.info("\n---\nContext:\n%s\n\nPrompt:\n%s\n\nRAG Prompt:\n%s\n---", context, prompt)
            logger.info("\n---\nPrompt:\n%s\n\nContext:\n%s\n---", prompt, context)
            return True  # dummy return

        pw_ai_results += pw_ai_results.select(
            _log=log_context_and_prompt(pw.this.context, pw.this.prompt)
        )

        pw_ai_results += pw_ai_results.select(
            response=self.llm(
                llms.prompt_chat_single_qa(pw.this.rag_prompt),
                model=pw.this.model,
            )
        )

        pw_ai_results = pw_ai_results.await_futures()

        pw_ai_results += pw_ai_results.select(
            result=_prepare_RAG_response(
                pw.this.response, pw.this.docs, pw.this.return_context_docs
            )
        )

        return pw_ai_results


if __name__ == "__main__":

    prompt_template = '''You are a competitive programming coach. 
        I will give you the user code submissions and a list of all available problems after "Data:".
        The data lines with verdict are the user code submissions. 
        The other lines are the available problems on codeforces.
        Answer the user query after looking at the user code submissions and the questions he got a wrong answer in.
        The problems you analyze and suggest should only be from the given data lines without verdict and should be similar in rating to the highest rated problems that the user has attempted.
        The answer should also explain how you arrived at the answer looking at the user code submissions if necessary. Keep your thinking short.
        Example query : "What problems should I practice next?"
        Ideal Answer : "Looking at your submissions, you solve questions rated around 1500 and you are facing difficulty in implementing binary search. 
        So here are some binary search problems you can practice: [Links to Binary search problems]."
        Example query : "How to implement dynamic programming?"
        Ideal Answer : "Here's an implementation of dynamic programming. [Dynamic Programming Code].\n
        Data: \n {context} \n{query} /think'''
        # Data: \n {context} \nAnswer this query: {query} /think'''
    

    sources = pw.io.jsonlines.read(
        "data",
        schema=pw.schema_from_dict(columns={"data": "str"}),
    )

    sources = json_encode(sources)

    sources_2 = pw.io.jsonlines.read(
        "data_2",
        schema=pw.schema_from_dict(columns={"data": "str"}),
    )

    sources_2 = json_encode(sources_2)

    # Local LLM
    # llm = pw.xpacks.llm.llms.LiteLLMChat(
    #     model="ollama/qwen3:4b",
    #     retry_strategy=pw.udfs.ExponentialBackoffRetryStrategy(
    #         max_retries=6
    #     ),
    #     cache_strategy=pw.udfs.DiskCache(),
    #     temperature=0,
    #     top_p=1,
    #     # format="json",  # only available in Ollama local deploy, not usable in Mistral API
    #     api_base="http://localhost:11434",
    #     # generation_kwargs={"num_ctx": 100},
    #     # num_ctx=100,
    # )

    llm = pw.xpacks.llm.llms.OpenAIChat(
        model="gpt-4.1",
        retry_strategy=pw.udfs.ExponentialBackoffRetryStrategy(
            max_retries=6
        ),
        cache_strategy=pw.udfs.DefaultCache(),
        temperature=0,
        capacity=8,
    )

    # Huggingface Embedding
    # embedding_model = "mixedbread-ai/mxbai-embed-large-v1"

    # embedder = pw.xpacks.llm.embedders.SentenceTransformerEmbedder(
    #     model=embedding_model,
    #     call_kwargs={"show_progress_bar": False},
    # )

    # OpenAI Embedding
    embedder = pw.xpacks.llm.embedders.OpenAIEmbedder(
        model="text-embedding-3-small",
        cache_strategy=pw.udfs.DefaultCache(),
    )


    splitter = pw.xpacks.llm.splitters.NullSplitter()

    parser = pw.xpacks.llm.parsers.UnstructuredParser()

    retriever_factory = pw.stdlib.indexing.UsearchKnnFactory(
        reserved_space=1000,
        embedder=embedder,
        metric=pw.stdlib.indexing.USearchMetricKind.COS,
    )
    
    retriever_factory_2 = pw.stdlib.indexing.UsearchKnnFactory(
        reserved_space=1000,
        embedder=embedder,
        metric=pw.stdlib.indexing.USearchMetricKind.COS,
    )

    document_store = pw.xpacks.llm.document_store.DocumentStore(
        docs = sources,
        retriever_factory=retriever_factory,
        splitter=splitter,
        parser=parser
    )

    document_store_2 = pw.xpacks.llm.document_store.DocumentStore(
        docs=sources_2,
        retriever_factory=retriever_factory_2,
        splitter=splitter,
        parser=parser
    )

    question_answerer = TwoDocQuestionAnswerer(
        llm=llm,
        indexer=document_store,
        indexer_2=document_store_2,
        search_topk=24,
        prompt_template=prompt_template,
    )

    config = dict(
        question_answerer=question_answerer,
        host="0.0.0.0",
        port=8000,
    )

    app = App(**config)
    app.run()
