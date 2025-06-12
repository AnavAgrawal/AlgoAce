import streamlit as st
import os
import sys
import base64
import re
sys.path.append(os.path.abspath(
os.path.join(os.path.dirname(__file__), '..', '')))
sys.path.append(os.path.dirname(__file__))

from cf_api import get_data, prompt_enhancer
from pathway.xpacks.llm.document_store import IndexingStatus
from pathway.xpacks.llm.question_answering import RAGClient
from dotenv import load_dotenv

load_dotenv()

PATHWAY_HOST = os.environ.get("PATHWAY_HOST", "0.0.0.0")
PATHWAY_PORT = os.environ.get("PATHWAY_PORT", 8000)

conn = RAGClient(url=f"http://{PATHWAY_HOST}:{PATHWAY_PORT}")


def question_page():

    # import cf_data as cf

    base_dir = os.path.dirname(os.path.abspath(__file__))
    submissions_path = os.path.join(
        base_dir, '..', 'data', 'submission_data.jsonl')
    problems_path = os.path.join(base_dir, '..', 'data', 'problems_data.jsonl')
    # logo_path = os.path.join(base_dir, 'Logo.jpeg')

    with st.sidebar:

        programming_language = st.text_input(
            "Enter preferred programming language (Optional):",
            placeholder="Python/C++/Java etc.",
            help="Any code output will be in this langauge."
        )

        if not programming_language:
            programming_language = "Python"

        st.markdown(
            "## How to use\n"
            "1. Enter your codeforces handle (Case Sensitive).\n"
            "3. Ask any question and you will get personalized answers.\n"
        )

        st.markdown("---")

        st.markdown("# About")
        st.markdown(
            "AI app to help user with personalized competitive programming answers. "
            "It uses Pathway’s [LLM App features](https://github.com/pathwaycom/llm-app) "
            "to build real-time LLM(Large Language Model)-enabled data pipeline in Python and join data from multiple input sources\n"

        )
        st.markdown(
            "[View the source code on GitHub](https://github.com/AnavAgrawal/AlgoAce)")

    file_ = open(r"assets/AlgoAce_Logo.jpeg", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    circular_logo_html_new = f"""
        <div style="text-align: center;">
            <img src="data:image/gif;base64,{data_url}" alt="Logo" style="border-radius: 50%; width: 150px; height: 150px; object-fit: cover; display: inline-block;">
            <br>
        </div>
        """

    # Streamlit UI elements

    st.markdown(circular_logo_html_new, unsafe_allow_html=True)
    st.title("AlgoAce - CP Companion")

    cf_handle = st.text_input(
        "Enter handle",
        placeholder="codeforces_handle",
    )

    question = st.text_input(
        "Ask any question",
        placeholder="What insights do you want?",
    )

    if cf_handle:
        get_data.send_request(cf_handle)

    # Handle Discounts API request if data source is selected and a question is provided
    if cf_handle and question:
        if not os.path.exists(submissions_path) and not os.path.exists(problems_path):
            st.error("Failed to process file. Please check the codeforces handle")

        # url = f'http://{api_host}:{api_port}/'
        # data = {"query": question,
        #         "language": programming_language}

        # response = requests.post(url, json=data)

        # if response.status_code == 200:
        #     st.write("### Answer")
        #     st.write(response.json())
        # else:
        #     st.error(f"Failed to send data to Codeforces API. Status code: {
        #              response.status_code}")
            
        # query = question + f"\nIf you give any code, please use {programming_language} as the programming language."
        query = prompt_enhancer.enhance_query(question)
        
        # query = question


        with st.spinner("Retrieving response..."):
            api_response = conn.answer(query, return_context_docs=True)
            response = api_response["response"]
            context_docs = api_response["context_docs"]

        think_match = re.search(r'<think>(.*?)</think>', response, re.DOTALL)
        think_content = think_match.group(1).strip() if think_match else ""

        # Remove <think>...</think> block to get the actual response
        response_content = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()

        st.write("### Answer")

        with st.expander(label="Show reasoning"):
            st.write(think_content)

        st.write(response_content)

        # with st.expander(label="Context documents"):
        #     st.markdown("Documents sent to LLM as context:\n")
        #     for i, doc in enumerate(context_docs):
        #         st.markdown(
        #             f"{i+1}. {doc['text']}\n```"
        #         )


def graph_page():
    import os
    import sys
    sys.path.append(os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '')))
    sys.path.append(os.path.dirname(__file__))
    import streamlit as st
    import streamlit.components.v1 as components

    # import cf_data as cf

    with st.sidebar:

        st.markdown(
            "Here you will find resources for all the major topics required for competitive programming.\n"
            "## How to use\n"
            "1. Left click on any topic to see more advanced topics.\n"
            "3. Right click on any topic to open the linked resource .\n"
        )

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "AI app to help user with personalized competitive programming answers. "
            "It uses Pathway’s [LLM App features](https://github.com/pathwaycom/llm-app) "
            "to build real-time LLM(Large Language Model)-enabled data pipeline in Python and join data from multiple input sources\n"

        )
        st.markdown(
            "[View the source code on GitHub](https://github.com/AnavAgrawal/AlgoAce)")

    # Streamlit UI elements

    HtmlFile = open("ui/graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    components.html(source_code, height=1000, width=1100)

    st.markdown(
        " <style> .st-emotion-cache-13ln4jf { max-width: 2000rem; padding : 1rem 1rem 10rem} </style> ", unsafe_allow_html=True)


page_names_to_funcs = {
    "Ask Questions": question_page,
    "Get Resources": graph_page
}

demo_name = st.sidebar.selectbox(
    "Select a mode", page_names_to_funcs.keys(), label_visibility="visible")

with st.sidebar:

    file_ = open(r"assets/AlgoAce_Logo.jpeg", "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    # HTML and CSS to make the image circular and center-align it along with the text
    circular_logo_html = f"""
    <div style="text-align: center;">
        <br>
        <img src="data:image/gif;base64,{data_url}" alt="Logo" style="border-radius: 50%; width: 150px; height: 150px; object-fit: cover; display: inline-block;">
        <br>
        <h1 style="margin-top: 10px;">Algo  Ace</h1>
        <br>
    </div>
    """

    # Use Markdown to render the HTML and CSS
    st.markdown(circular_logo_html, unsafe_allow_html=True)
# st.sidebar.success("Select your mode above.")
# demo_name = st.sidebar.selectbox("Choose a demo", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
