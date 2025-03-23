import gradio as gr
import requests

BACKEND_URL = "http://127.0.0.1:8000"

# === Utility Function to Call API ===
ERROR_MESSAGE = "⚠️ Apologies! We encountered an issue processing your request. 🙏 Please try again shortly."

def call_api(endpoint, data):
    try:
        response = requests.post(f"{BACKEND_URL}/{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"{ERROR_MESSAGE} (Details: {e})"}


# === Updated Functions with Provider & Model ===
def grammar_checker(text, provider, model):
    return call_api("grammar-check", {"text": text, "provider": provider, "model": model}).get("corrected_text", ERROR_MESSAGE)

def plagiarism_checker(text, provider, model):
    return call_api("plagiarism-check", {"text": text, "provider": provider, "model": model}).get("plagiarism_result", ERROR_MESSAGE)

def translator(text, target_language, provider, model):
    return call_api("translate", {
        "text": text, 
        "target_language": target_language,
        "provider": provider,
        "model": model
    }).get("translated_text", ERROR_MESSAGE)

def word_counter(text):
    return call_api("word-count", {"text": text}).get("word_count", ERROR_MESSAGE)

def summarizer(text, provider, model):
    return call_api("summarize", {"text": text, "provider": provider, "model": model}).get("summary", ERROR_MESSAGE)

def paraphrase(text, provider, model):
    return call_api("paraphrase", {"text": text, "provider": provider, "model": model}).get("paraphrased_text", ERROR_MESSAGE)

# === Available Providers & Models ===
PROVIDERS = ["google", "openai", "cohere"]
MODELS = {
    "google": ["gemini-1.5-flash"],
    "openai": ["gpt-4o-mini"],
    # "cohere": ["Command-R+", "Command-R"]
}

# === Function to Create UI Tasks ===
def create_task(tab_name, input_label, button_label, output_label, function, example_inputs, include_provider=False):
    with gr.Tab(tab_name):
        gr.Markdown(f"## {tab_name}")

        with gr.Row():
            with gr.Column(scale=1):
                input_text = gr.Textbox(label=input_label, placeholder=f"Enter text for {tab_name}", lines=10)
                inputs = [input_text]

                if include_provider:
                    with gr.Row():
                        provider_dropdown = gr.Dropdown(choices=PROVIDERS, label="Choose Provider", value=PROVIDERS[0])
                        model_dropdown = gr.Dropdown(choices=MODELS[PROVIDERS[0]], label="Choose Model", value=MODELS[PROVIDERS[0]][0])

                    def update_models(provider):
                        return gr.update(choices=MODELS[provider], value=MODELS[provider][0])

                    provider_dropdown.change(update_models, inputs=[provider_dropdown], outputs=[model_dropdown])
                    inputs.extend([provider_dropdown, model_dropdown])

                button = gr.Button(button_label)

            with gr.Column(scale=1):
                output_text = gr.Textbox(label=output_label, interactive=False, lines=10)

        button.click(function, inputs=inputs, outputs=output_text)
        gr.Examples(examples=example_inputs, inputs=input_text)

# === CREATE THE MAIN INTERFACE ===
with gr.Blocks(theme=gr.themes.Ocean()) as demo:
    gr.Markdown("# ✍️ Sharpen: Refine, Enhance, and Perfect Your Writing")

    with gr.Tabs():
        create_task("Grammar Checker", "Enter text", "Check Grammar", "Checked Grammar", grammar_checker, ["This is an example sentence."], include_provider=True)
        
        create_task("Plagiarism Checker", "Enter text", "Check Plagiarism", "Plagiarism Check Result", plagiarism_checker, ["The quick brown fox."], include_provider=True)
        
        # **Translator Tab (with Target Language input)**
        with gr.Tab("Translator"):
            gr.Markdown("## Translator")
            
            with gr.Row():
                with gr.Column(scale=1):
                    input_text = gr.Textbox(label="Enter text", placeholder="Enter text to translate", lines=10)
                    target_language = gr.Textbox(label="Target Language", placeholder="e.g., French")
                    with gr.Row():
                        provider_dropdown = gr.Dropdown(choices=PROVIDERS, label="Choose Provider", value=PROVIDERS[0])
                        model_dropdown = gr.Dropdown(choices=MODELS[PROVIDERS[0]], label="Choose Model", value=MODELS[PROVIDERS[0]][0])

                    def update_models(provider):
                        return gr.update(choices=MODELS[provider], value=MODELS[provider][0])

                    provider_dropdown.change(update_models, inputs=[provider_dropdown], outputs=[model_dropdown])

                    button = gr.Button("Translate")
                
                with gr.Column(scale=1):
                    output_text = gr.Textbox(label="Translated Text", interactive=False, lines=10)

            button.click(translator, inputs=[input_text, target_language, provider_dropdown, model_dropdown], outputs=output_text)
            gr.Examples(examples=["Hello world!"], inputs=input_text)
        
        create_task("Summarizer", "Enter text", "Summarize", "Summary", summarizer, ["A long passage."], include_provider=True)
        
        create_task("Paraphrase", "Enter text", "Paraphrase", "Paraphrased Text", paraphrase, ["Rewrite this sentence."], include_provider=True)

        create_task("Word Counter", "Enter text", "Count Words", "Word Count", word_counter, ["Count these words."])

# === LAUNCH THE APP ===
demo.launch()
