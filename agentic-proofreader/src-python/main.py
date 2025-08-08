from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# --- Specialist Agents (internal functions) ---

def grammar_checker_agent(text: str) -> str:
    """Simulates a basic grammar check."""
    return f"[Grammar Checked] {text}"

def researcher_agent(text: str) -> list[str]:
    """
    Simulates a researcher agent.
    It looks for keywords and returns canned facts.
    """
    findings = []
    # Use case-insensitive search for keywords
    if re.search(r'tauri', text, re.IGNORECASE):
        findings.append("Fact: Tauri is a framework for building desktop applications with web technologies.")
    if re.search(r'rust', text, re.IGNORECASE):
        findings.append("Fact: Rust is a systems programming language focused on safety and performance.")
    if re.search(r'python', text, re.IGNORECASE):
        findings.append("Fact: Python is a high-level, general-purpose programming language.")

    return findings

def refine_agent(text: str, style: str) -> str:
    """Simulates refining the text based on style."""
    return f"[Refined for {style} Style] {text}"

# --- Master Agent / Pipeline ---

def run_proofreading_pipeline(text: str, style: str) -> tuple[str, list[str]]:
    """
    This is the Master Agent's job.
    It orchestrates the calls to various specialist agents.
    Returns the final text and a list of findings.
    """
    # 1. Run Grammar Checker
    checked_text = grammar_checker_agent(text)
    # 2. Run Researcher
    findings = researcher_agent(checked_text)
    # 3. Run Refiner
    refined_text = refine_agent(checked_text, style)

    return refined_text, findings

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
    result_text, findings = run_proofreading_pipeline(input_text, selected_style)

    # The API response will be updated in the next step to include findings
    return jsonify({'result': result_text, 'findings': findings})

if __name__ == '__main__':
    app.run(port=8000)
