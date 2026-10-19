# Demo-POC deck conversion

This directory contains the source decks in text format (`decks/*.txt`).

To generate actual PPTX files locally:

1. Create a virtualenv and install the dependencies:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run the generator:
   python scripts/generate_pptx.py

3. Output files will be created alongside the source files in `/decks` as `.pptx` slides.

4. Open the generated files in PowerPoint and polish the layout/icons if needed.

Note: This environment cannot create a valid binary `.pptx` file directly through the GitHub file API, so the generation step is run locally. The source slide text is already present in `/decks` and the script will produce the actual PPTX deck files for you.
