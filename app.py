"""Gradio interface for the Columbia CS Unofficial Guide."""

from __future__ import annotations

import gradio as gr

from generator import answer_question, format_retrieval_details, format_sources, relevant_chunks
from retriever import build_vector_store


def respond(question: str) -> tuple[str, str, str]:
    if not question.strip():
        return "Enter a question.", "", ""
    answer, chunks = answer_question(question.strip())
    sources = format_sources(relevant_chunks(chunks))
    return answer, sources, format_retrieval_details(chunks)


with gr.Blocks(title="Columbia CS Unofficial Guide") as demo:
    gr.Markdown("# Columbia CS Unofficial Guide")
    question = gr.Textbox(label="Question", lines=3)
    ask = gr.Button("Ask", variant="primary")
    answer = gr.Markdown(label="Answer")
    sources = gr.Markdown(label="Sources")
    retrieved = gr.Markdown(label="Retrieved chunks")

    ask.click(respond, inputs=question, outputs=[answer, sources, retrieved])
    question.submit(respond, inputs=question, outputs=[answer, sources, retrieved])


if __name__ == "__main__":
    build_vector_store()
    demo.launch(server_name="127.0.0.1", server_port=7860)
