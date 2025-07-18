# AlgoAce local LLM version

Python 3.12 or 3.13 will be required.

    apt (or brew) install libmagic 
    python -m venv venv
    pip install -r req.txt  # By that line your venv should be 1.2 GB, good luck
    pip install -U pathway
    python app.py  # Pathway
    streamlit run ui/ui.py  # Streamlit

ollama should be running in the background. brew install ollama
ollama pull gemma3  # For example

## Troubleshoot

If you have some error regarding NullSplitter, you should upgrade pathway; does not work on 0.16.4, works on 0.23 or 0.25.

I also had to brew install libmagic.
