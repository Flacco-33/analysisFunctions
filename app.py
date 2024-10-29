import gradio as gr
# from dataAnalysis import analizar_data_match 
from function.textAnalysis import analyze_comment
# from analysisTeacher import analysis_teacher as py
from function.analysisTeacher import analysis_teacher
from function.dataAnalysis import analysis_data_match

iface = gr.Interface(
    fn=analyze_comment,
    inputs="text",
    outputs="text",
    title="Sentiment and Emotion Analyzer",
    description="Analyze the sentiment and emotions of student comments about their teachers.",
    api_name="/analyze_comment"
)

iface2 = gr.Interface(
    fn=analysis_data_match,
    inputs=None,
    outputs="text",
    title="Emotion Match Analysis",
    description="Analyze the matches between the emotions of students and teachers.",
    api_name="/analysis_data_match"
)

iface3=gr.Interface(
    fn=analysis_teacher,
    inputs=None,
    outputs="text",
    title="Teacher Comments Analysis",
    description="Analyze the comments of the teachers.",
    api_name="/analysis_teacher"
)

demo = gr.TabbedInterface([iface, iface2,iface3], ["Text-to-text", "Emotion Match Analysis","Analysis Teacher"])
if __name__ == "__main__":
    demo.launch(server_port=7862)