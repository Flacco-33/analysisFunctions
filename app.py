import gradio as gr
from functions.textAnalysis import analyze_comment

demo = gr.Interface(
    fn=analyze_comment,
    inputs="text",
    outputs="text",
    title="Sentiment and Emotion Analyzer",
    description="Analyze the sentiment and emotions of student comments about their teachers.",
    api_name="/analyze_comment"
)

if __name__ == "__main__":
    demo.queue().launch(server_port=7862)