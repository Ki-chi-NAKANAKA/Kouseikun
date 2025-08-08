from flask import Flask, request, jsonify

app = Flask(__name__)

# --- Specialist Agents (internal functions) ---

def grammar_checker_agent(text: str) -> str:
    """Simulates a basic grammar check."""
    return f"[Grammar Checked] {text}"

def refine_agent(text: str, style: str) -> str:
    """Simulates refining the text based on style."""
    return f"[Refined for {style} Style] {text}"

# --- Master Agent / Pipeline ---

def run_proofreading_pipeline(text: str, style: str) -> str:
    """
    This is the Master Agent's job.
    It orchestrates the calls to various specialist agents.
    """
    # 1. Run Grammar Checker
    checked_text = grammar_checker_agent(text)
    # 2. Run Refiner
    refined_text = refine_agent(checked_text, style)

    return refined_text

# --- API Endpoint ---

@app.route('/proofread', methods=['POST'])
def proofread_endpoint():
    """
    The main API endpoint that the Tauri frontend will call.
    """
    data = request.get_json()
    if not data or 'text' not in data or 'style' not in data:
        return jsonify({'error': 'Missing text or style in request'}), 400

    input_text = data['text']
    selected_style = data['style']

    # Run the pipeline
    result_text = run_proofreading_pipeline(input_text, selected_style)

    return jsonify({'result': result_text})

if __name__ == '__main__':
    # The port should be chosen carefully to avoid conflicts.
    # 8000 is a common choice for local development servers.
    app.run(port=8000)
