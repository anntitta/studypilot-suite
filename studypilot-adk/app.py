import os
from vector_store import extract_and_index_pdf
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from router import central_coordinator_router

app = FastAPI(title="StudyPilot Multimodal Vision Engine API - Production", version="6.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "success": False,
            "message": "Only PDF files allowed."
        }

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    success = extract_and_index_pdf(
        file_path=file_path,
        file_id=file.filename
    )

    return {
        "success": success,
        "message": "PDF indexed successfully."
        if success
        else "PDF indexing failed."
    }

@app.post("/api/chat")
async def handle_agent_request(
    message: str = Form(""),
    active_tab: str = Form("notes"),
    file: UploadFile = File(None)
):
    print(f"\n🛸 [Incoming Telemetry] Active Mode Segment: {active_tab} | Command: '{message}'")
    
    clean_message = message.strip() if message else f"Analyze this layout context for {active_tab} parameters"
    image_bytes = None
    mime_type = None

    if file is not None:
        print(f"📸 [Image Handler] Ingested raw visual attachment stream: '{file.filename}'")
        image_bytes = await file.read()
        mime_type = file.content_type  

    try:
        # FIXED: Forwarding active_tab parameter into routing matrix evaluations
        agent_response = central_coordinator_router(
            user_query=clean_message,
            image_bytes=image_bytes,
            mime_type=mime_type,
            active_tab=active_tab
        )
    except Exception as server_err:
        print(f"❌ Server Runtime Exception: {server_err}")
        agent_response = "🛸 An operational error occurred in the vision core matrix."

    return {"success": True, "response": agent_response}