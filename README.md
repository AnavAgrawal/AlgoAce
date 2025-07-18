# AlgoAce local LLM version

Python 3.12 or more is required.

    apt (or brew) install libmagic 
    python -m venv venv
    source venv/bin/activate
    pip install -r req.txt  # By that line your venv should be 2.3 GB, good luck
    pip install -U pathway  # Hope they fix it someday
    python app.py  # Pathway
    streamlit run ui/ui.py  # AlgoAce

ollama should be running in the background.

    snap (or brew) install ollama
    ollama pull gemma3  # For example

## Troubleshoot

If you have some error regarding NullSplitter, you should upgrade pathway; does not work on 0.16.4, works on 0.23 or 0.25.
