# TODOs
move models to:
```
from sqlalchemy.dialects.postgresql import UUID
id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
```
create customer token:
```python
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from yourproject.database import get_db
from yourproject.models import CustomerToken

router = APIRouter()

class AuthPayload(BaseModel):
    customer_name: str
    token: str
    redirect_to: str = "/room/panel"

@router.post("/auth")
async def authenticate_and_set_cookie(
    payload: AuthPayload,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(CustomerToken.customer_id).where(
        CustomerToken.customer_name == payload.customer_name,
        CustomerToken.token == payload.token,
    )
    result = await db.execute(stmt)
    customer_id = result.scalar_one_or_none()

    if not customer_id:
        raise HTTPException(status_code=403, detail="Token inválido")

    response = RedirectResponse(url=payload.redirect_to, status_code=302)
    response.set_cookie(key="customer_id", value=str(customer_id), httponly=True)
    return response

```
# Running
uv run uvicorn api.main:app --host 0.0.0.0 --port 8000

# Entidades do sistema
customer - Multitenant.Modela os clientes do sistema.

pacient - Modela os pacientes cadastrados no sistema para cada cliente.

room - Modela as salas de atendimento de cada cliente.

ticket - Modela os tickets de atendimento de cada paciente atendido em cada cliente.

## State Pattern


### Room 
#### States
ocupado

livre

manutenção

#### Events
ocupar

liberar

manutenção

### Paciente
* Estados

    em espera

    em atendimento:

      Opções abaixo são diferentes "salas":

        em consulta
        
        em exame

        em medicação

        em procedimento

        em internação

        em terapia

        em observação

        em transferência

    em alta

### Eventos

* chegar

* cadastrar

* chamar (a uma sala)

* aguardar

* sair


### Ticket 
#### States

em uso

cancelado

finalizado


# Interfaces com o usuário
## Recepcionista da clinica
1- Check-in de paciente gerando o ticket.

2- Cadastro de sala.

3- Atualização de sala.

## Médico / enfermeiro
1- Chamada de paciente

2- Atendimento de paciente

3- Redirecionamento de paciente

4- Alta de pacientes

# Possíveis caminhos:
## Happy paths
### Simples

1- Recepcionista realiza check-in de paciente.

2- Médico chama paciente para avaliação.

2- Médico atende paciente na sala 01.

3- Médico ajusta urgência no ticket.

4- Médico libera paciente para sala de espera.

5- Médico chama paciente.

6- Médico atende paciente.

7- Médico dá alta do paciente.

### Com multiplos atendimentos e redirecionamento de pacientes


1- Recepcionista realiza check-in de paciente.

2- Médico chama paciente para avaliação.

2- Médico atende paciente na sala 01.

3- Médico ajusta urgência no ticket.

4- Médico libera paciente para sala de espera.

5- Médico chama paciente.

6- Médico atende paciente.

7- Médico redireciona paciente para sala 02.

8- Médico libera paciente para sala de espera.

9- Médico chama paciente.

10- Médico atende paciente.

11- Médico libera paciente para sala de espera.

12- Médico atende paciente.

13- Médico dá alta do paciente.

### Com multiplos atendimentos e redirecionamento de pacientes com urgência

1- Recepcionista realiza check-in de paciente.

2- Médico chama paciente para avaliação.

2- Médico atende paciente na sala 01.
7- Médico dá alta do paciente.

## Caminhos alternativos
### Manutenção de sala
2- Recepcionista cadastro de sala.
3- Recepcionista atualização de sala.

# TODOs
- [ ] Implementar o sistema de check-in de pacientes.