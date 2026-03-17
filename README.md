# BIA 810 Project
### Team: 
* Mick Twohig 
* Matt Kelly
* Brian Hasselbeck

# Project Overview
The aim of the project is to provide an application for researchers that will allow
* the researcher to enter a search criteria,
* the system will query PubMed for any pertinent documentation,
* the system will fetch any relevant PDF copies of these papers,
* the system will generate a summary and create an output document of this summary,
* source documents will be cited accordingly.

## Tools used
We will implement the solution as a locally running agent. We will use [Ollama](https://ollama.com/)
as the runtime for the LLM models, Langchain and Langgraph for the orchestration,  [Streamlit](https://streamlit.io/) 
for UI, and some of the common python libraries.

*NOTE TO TEAM: We're looking at putting RAG into the mix, so if we go with that will need a little text contented added here for this*

# Usage
The project relies on a local [Ollama](https://ollama.com/) instance. Installation of this is outside of our current scope, 
but is fortunately a well-documented process on the project website.

The project also needs a suitable local model. We use `llama3:8b`, which is a reasonable
model, and comes in at around 2.7GB, so not too demanding in terms of storage.
The model can be fetched as follows:
```console
$ ollama pull llama3:8b
```

#### Application
Our application provides a [Streamlit](https://streamlit.io/) user interface. To run the application using streamlit, 
navigate to the project location and enter the following:
```console
$ streamlit run main.py
```