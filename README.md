# GPT-Logprobs-Visualizer
Visualize the decisions gpt made while generating the response

LLMs like GPT-3.5 / 4 sample from a distribution of likely tokens to choose the next one while generating a response.
This tool helps you to visualize what top choices the model had before finally choosing (technically it is being sampled with a specified temperature) the next token.

## Usage
#### Live Demo

Head over to :  [https://gpt-logprobs-visualizer.streamlit.app/](https://gpt-logprobs-visualizer.streamlit.app/)

#### Running Locally

```bash
git clone https://github.com/JayantTaneja/GPT-Logprobs-Visualizer.git
cd GPT-Logprobs-Visualizer

pip install streamlit
pip install -r requirements.txt

streamlit run app.py
```