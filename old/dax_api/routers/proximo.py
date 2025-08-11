from fastapi import APIRouter, HTTPException, Response

from dax_api.database import database


router = APIRouter(prefix="/proximo")

@router.get("/")
async def get_proximo():
    """
    Returns the next patient to be called.
    example:
    {
        "NOME": "João da Silva",
        "SENHA": "B104",
        "DESTINO": "Sala 101",
        "PRIORIDADE": "Emergência"
    }
    """
    paciente = database.get_next_patient()
    return paciente
