// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use docx_rs::{Docx, Paragraph, Run};
use std::fs::File;
use tauri::AppHandle;

// --- Specialist Agents (internal functions) ---

fn grammar_checker_agent(text: String) -> String {
    // Simulate basic grammar check
    format!("[Grammar Checked] {}", text)
}

fn refine_agent(text: String, style: String) -> String {
    // Simulate refining the text based on style
    format!("[Refined for {} Style] {}", style, text)
}


// --- Tauri Commands (public-facing) ---

#[tauri::command]
async fn run_proofreading_pipeline(text: String, style: String) -> String {
    // This is the Master Agent's job.
    // 1. Run Grammar Checker
    let checked_text = grammar_checker_agent(text);
    // 2. Run Refiner
    let refined_text = refine_agent(checked_text, style);

    // In the future, other agents would be called here.

    refined_text
}

#[tauri::command]
async fn export_as_docx(app: AppHandle, text: String) -> Result<(), String> {
    let file_path = tauri::api::dialog::blocking::FileDialogBuilder::new(&app)
        .add_filter("Word Document", &["docx"])
        .set_file_name("proofread-document.docx")
        .save_file();

    if let Some(path) = file_path {
        let file = File::create(&path).map_err(|e| e.to_string())?;
        let docx = Docx::new()
            .add_paragraph(Paragraph::new().add_run(Run::new().add_text(text)));

        docx.build().pack(file).map_err(|e| e.to_string())?;
        Ok(())
    } else {
        Ok(())
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            run_proofreading_pipeline,
            export_as_docx
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
