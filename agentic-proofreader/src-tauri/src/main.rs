// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use docx_rs::{Docx, Paragraph, Run};
use std::fs::File;
use std::process::Command;
use std::thread;
use tauri::AppHandle;

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
    // Spawn the Python backend in a separate thread
    thread::spawn(|| {
        let _ = Command::new("python")
            .arg("../src-python/main.py") // Corrected path relative to src-tauri
            .spawn()
            .expect("Failed to start Python backend");
        // We could add more robust error handling and process management here
    });

    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![export_as_docx])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
