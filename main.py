from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response, JSONResponse
from rembg import remove
from PIL import Image
import io
import uvicorn
import os

app = FastAPI(title="Background Remover")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.30:8000", 
        "http://192.168.1.30:5173",
        "http://192.168.1.30:3000" 
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Background Removal API is running"}

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...)):
    try:
        if file.content_type not in ["image/png", "image/jpeg", "image/jpg"]:
            return JSONResponse(
                content={"error": "Invalid file type. Upload PNG or JPG."}, 
                status_code=400
            )

        file_content = await file.read()
        if not file_content:
            return JSONResponse(
                content={"error": "Uploaded file is empty"}, 
                status_code=400
            )

        # Process image
        input_image = Image.open(io.BytesIO(file_content)).convert("RGBA")
        output_image = remove(input_image)

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        return Response(
            content=img_byte_arr.getvalue(), 
            media_type="image/png",
            headers={
                "Content-Disposition": "attachment; filename=removed_bg.png"
            }
        )

    except Exception as e:
        return JSONResponse(
            content={"error": f"Processing error: {str(e)}"}, 
            status_code=500
        )

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)