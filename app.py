import os
import gradio as gr
from google import genai

# Get Gemini API key from environment variable
api_key = os.environ.get("vip")

# Initialize Gemini client
client = genai.Client(api_key=api_key)


def generate_questions(topic, difficulty, number_of_questions):

    if not topic:
        return "Please enter a topic."

    if not number_of_questions:
        return "Please enter the number of questions."

    prompt = f"""
You are an interactive question generator.

Topic: {topic}
Difficulty: {difficulty}
Number of questions: {int(number_of_questions)}

Generate exactly {int(number_of_questions)} questions.

Rules:
- Number each question clearly.
- Do not provide answers.
- Make the questions relevant to the topic.
- Make them appropriate for the selected difficulty level.
"""

    try:
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"Error: {str(e)}"


# Create Gradio application
app = gr.Interface(
    fn=generate_questions,

    inputs=[
        gr.Textbox(
            label="Topic",
            placeholder="Enter a topic, e.g. Artificial Intelligence"
        ),

        gr.Dropdown(
            choices=["easy", "medium", "hard"],
            value="medium",
            label="Difficulty"
        ),

        gr.Number(
            value=5,
            precision=0,
            label="Number of Questions"
        )
    ],

    outputs=gr.Textbox(
        label="Generated Questions",
        lines=12
    ),

    title="🤖 Interactive Question Generator",

    description=(
        "Generate questions using Google Gemini AI. "
        "Choose a topic, difficulty level, and number of questions."
    ),

    submit_btn="Generate Questions",
    clear_btn="Clear"
)


# Launch the application
app.launch()