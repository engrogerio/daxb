import requests
import os
from io import BytesIO
from fastapi import APIRouter, HTTPException, Response
from murf import Murf
from fastapi.responses import StreamingResponse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
router = APIRouter(prefix="/audio")

@router.get("/")
async def get_audio(text: str=''):
    client = Murf(api_key="ap2_985b0b72-d741-4bed-b735-187754fb7049")

    response = client.text_to_speech.generate(
        text = text,
        voice_id = "pt-BR-eloa"
    )
    
    audio_url = response.audio_file

    # Baixa o conteúdo da URL como bytes
    audio_response = requests.get(audio_url)
    if audio_response.status_code != 200:
        return {"error": "Falha ao obter o áudio"}

    audio_bytes = BytesIO(audio_response.content)

    return StreamingResponse(
        audio_bytes,
        media_type="audio/wav",
        headers={
            "Content-Disposition": "inline; filename=voz.wav",
            "Cache-Control": "no-cache"
        }
    )