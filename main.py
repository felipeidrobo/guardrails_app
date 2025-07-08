from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from guardrails import Guard, OnFailAction
import uvicorn
from guardrails.hub import ToxicLanguage
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="🛡️ API Guardrails AI")

guard = Guard().use_many(
    ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail=OnFailAction.EXCEPTION)
)

class TextInput(BaseModel):
    text: str

@app.post("/validate/")
def validate_text(input_data: TextInput):
    logging.info(f"Texto recibido: {input_data.text}")
    if not input_data.text.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío.")
    try:
        guard.validate(input_data.text)
        return {"status": "success", "message": "✅ El texto pasó todas las validaciones."}
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"❌ El texto falló la validación: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
