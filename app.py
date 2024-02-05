import openai

from pyvis import network as net

import streamlit as st
from streamlit.components.v1 import html

import math


st.set_page_config(page_title="GPT Logprobs Visualizer", layout="wide")


def make_gpt_call(prompt: str, bf: int):
    openai.api_key = api_key
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",
        messages=[{"role": "user", "content": prompt}],
        logprobs=True,
        top_logprobs=bf,
    )
    openai.api_key = ""

    return completion


def build_tree(response, bf):
    content = response.choices[0].logprobs.content

    tree = net.Network(height="1000px", cdn_resources="remote")
    tree.toggle_physics("False")

    prev_node = ""
    tree.add_node(prev_node + "0", label="<START>", x=0, y=-100)

    step = 0

    for tokenset in content:
        step += 1

        token_chosen = tokenset.token

        x_offset = -(bf) // 2

        for token_object in tokenset.top_logprobs:
            node_id = token_object.token + str(step)
            token = token_object.token
            if token == token_chosen:
                tree.add_node(
                    node_id,
                    title=token,
                    label=token,
                    x=(x_offset * 150),
                    y=step * 200,
                    color="green",
                )

            else:
                tree.add_node(
                    node_id,
                    title=token,
                    label=token,
                    x=(x_offset * 150),
                    y=step * 200,
                    color="orange",
                )

            tree.add_edge(
                prev_node + str(step - 1),
                node_id,
                label=f"{int(math.exp(token_object.logprob) * 100000)/1000} %",
            )

            x_offset += 1
        prev_node = token_chosen

    tree.add_node("<END>", x=0, y=(step + 1) * 200)
    tree.add_edge(prev_node + str(step), "<END>")

    tree.write_html("tree_code.html")


def render_tree():
    with open("tree_code.html", "r") as f:
        raw_html_code = f.read()

    html(raw_html_code, height=1010)


st.title("GPT Logprobs Visualizer")
st.markdown(
    "Visualizing the ```logprobs``` parameter to see what options GPT evaluated while generating a response"
)

api_key = st.text_input(
    "Enter your OpenAI API Key (NOT stored in a database)",
    type="password",
    help="The API key is not stored in any databases by the app",
)
prompt = st.text_input("Enter the prompt")
bf = st.slider(
    "Branching Factor or the ```top_logprobs``` setting",
    min_value=1,
    max_value=5,
    value=2,
)

go = st.button("Let's Go!")

if go:
    if api_key == "":
        st.error("Please Enter a Valid API Key")
        st.stop()

    with st.spinner("Making API Call to GPT"):
        try:
            response = make_gpt_call(prompt, bf)
        except openai.error.AuthenticationError:
            st.error("Invalid API Key")
            st.stop()

        st.success("Got following response from GPT")
        st.markdown(response.choices[0].message.content)

    with st.spinner("Parsing Response"):
        build_tree(response=response, bf=bf)
        success_banner = st.success("Response Parsed")

    with st.spinner("Rendering Graph"):
        render_tree()
        success_banner.success("Graph Rendered, drag around/hover to explore more")
