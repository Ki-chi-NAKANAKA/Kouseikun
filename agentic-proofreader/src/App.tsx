import { useState } from 'react';
import { invoke } from '@tauri-apps/api/core';
import './App.css';

function App() {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isProofreading, setIsProofreading] = useState(false);
  const [isExporting, setIsExporting] = useState(false);
  const [selectedStyle, setSelectedStyle] = useState('Formal'); // New state for style

  const handleProofread = async () => {
    if (!inputText) return;
    setIsProofreading(true);
    try {
      const response = await fetch('http://localhost:8000/proofread', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: inputText,
          style: selectedStyle,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setOutputText(data.result);

    } catch (error) {
      console.error("Failed to communicate with Python backend:", error);
      setOutputText(`Error: ${error}`);
    } finally {
      setIsProofreading(false);
    }
  };

  const handleExport = async () => {
    if (!outputText) return;
    setIsExporting(true);
    try {
      await invoke('export_as_docx', { text: outputText });
      alert('Successfully exported to .docx!');
    } catch (error) {
      console.error("Failed to call export_as_docx command:", error);
      alert(`Export failed: ${error}`);
    } finally {
      setIsExporting(false);
    }
  };


  return (
    <div className="container">
      <h1>Agentic AI Proofreader</h1>

      {/* New Settings Section */}
      <div className="settings">
        <label htmlFor="style-select">Proofreading Style:</label>
        <select
          id="style-select"
          value={selectedStyle}
          onChange={(e) => setSelectedStyle(e.target.value)}
          disabled={isProofreading}
        >
          <option value="Formal">Formal</option>
          <option value="Casual">Casual</option>
          <option value="Technical">Technical</option>
        </select>
      </div>

      <div className="main-content">
        <div className="textarea-container">
          <h2>Input Text</h2>
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter text to proofread..."
            disabled={isProofreading || isExporting}
          />
        </div>
        <div className="controls">
          <button onClick={handleProofread} disabled={isProofreading || !inputText}>
            {isProofreading ? 'Processing...' : 'Run Proofread'}
          </button>
          <button onClick={handleExport} disabled={isExporting || !outputText}>
            {isExporting ? 'Exporting...' : 'Export to Word'}
          </button>
        </div>
        <div className="textarea-container">
          <h2>Output Text</h2>
          <textarea
            value={outputText}
            readOnly
            placeholder="Proofread text will appear here..."
          />
        </div>
      </div>
    </div>
  );
}

export default App;
