import gradio as gr
from pathlib import Path
import re
import random

def _read_patient_data(filepath: str):
    try:
        path = Path(filepath)
        if path.exists() and path.is_file():
            raw_text = path.read_text(encoding="utf-8")
            clean_text = re.sub(r"[#*`\-_\[\]\(\)]", "", raw_text)
            return clean_text.strip()
        return None
    except Exception as e:
        print(f"Error reading file {e}")
        return None


def select_patient(patient_path: str):
    content = _read_patient_data(patient_path)
    # TODO: Add context from maybe other files, for example session files or radiography interpretations.
    history = [
        {
            "role": "assistant",
            "content": [
                {"type": "text", "text": "Patient records loaded, ask me anything! 🦷"}
            ],
        }
    ]
    return history, content


def respond(message, history, patient_context):
    print(patient_context)
    return random.choice(["Yes", "No"])


with gr.Blocks(title="DentiGem") as dentigem:

    patient_history = gr.State()
    gr.Markdown("# DentiGem")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Select the desired patient record")
            patient = gr.FileExplorer(
                file_count="single",
                glob="*.md",
                root_dir="./DentiGem_Demo/Patients",
                interactive=True,
                height=400,
            )
            btn_select = gr.Button(value="Select Patient", variant="primary")

        with gr.Column(scale=2):
            gr.Markdown("### Patient Analysis")

            with gr.Group(visible=True) as chat_container:
                chat_window = gr.Chatbot(
                    placeholder="<strong> Please select the patient records first. </strong>"
                )
                gr.ChatInterface(
                    fn=respond,
                    multimodal=True,
                    autoscroll=True,
                    chatbot=chat_window,
                    additional_inputs=[patient_history],
                )

    btn_select.click(
        fn=select_patient, inputs=patient, outputs=[chat_window, patient_history]
    )

dentigem.launch(theme=gr.themes.Soft())
