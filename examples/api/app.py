import pathway as pw
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..','')))
sys.path.append(os.path.dirname(__file__))
from common.embedder import embeddings, index_embeddings
from common.prompt import prompt
import os


def run(host, port):
    # Given a user question as a query from your API
    query_context, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema =QueryInputSchema,
        autocommit_duration_ms=50,
        delete_completed_queries=False
    )

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, '..', 'data')

    # Real-time data coming from external data sources such as jsonlines file
    submission_data = pw.io.jsonlines.read(
        file_path,
        schema=DataInputSchema,
        mode="streaming"
    )

    # Compute embeddings for each document using the OpenAI Embeddings API
    embedded_data = embeddings(context=submission_data, data_to_embed=submission_data.doc)

    # Construct an index on the generated embeddings in real-time
    index = index_embeddings(embedded_data)

    # Generate embeddings for the query from the OpenAI Embeddings API
    embedded_query = embeddings(context=query_context, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query, pw.this.language)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)

    # Run the pipeline
    pw.run()


class DataInputSchema(pw.Schema):
    doc: str


class QueryInputSchema(pw.Schema):
    query: str
    language : str
