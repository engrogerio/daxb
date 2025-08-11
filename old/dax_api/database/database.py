arrivals =  [
    {"NOME": "Rogério", "SENHA": "A122", "CHEGADA": "2025-10-01 08:00:00"},
    {"NOME": "Maria", "SENHA": "B101", "CHEGADA": "2025-10-01 09:00:00"},
    {"NOME": "Carlos", "SENHA": "C102", "CHEGADA": "2025-10-01 10:00:00"},
    {"NOME": "Ana", "SENHA": "D103", "CHEGADA": "2025-10-01 10:10:00"},
    {"NOME": "João", "SENHA": "E104", "CHEGADA": "2025-10-01 10:30:00"},
    {"NOME": "Fernanda", "SENHA": "A105", "CHEGADA": "2025-10-01 13:00:00"},
    {"NOME": "Lucas", "SENHA": "C106", "CHEGADA": "2025-10-01 13:10:00"},
    {"NOME": "Juliana", "SENHA": "B107", "CHEGADA": "2025-10-01 14:16:00"},
    {"NOME": "Ricardo", "SENHA": "E108", "CHEGADA": "2025-10-01 14:20:00"},
    {"NOME": "Patrícia", "SENHA": "D109", "CHEGADA": "2025-10-01 15:00:00"}
]
# arrivals =  [
#         {"POSIÇÃO": "Em Atendimento", "NOME": "Rogério", "SENHA": "A122", "PREVISÃO": " - "},
#         {"POSIÇÃO": "1º", "NOME": "Maria", "SENHA": "B101", "PREVISÃO": "Próxima Chamada"},
#         {"POSIÇÃO": "2º", "NOME": "Carlos", "SENHA": "C102", "PREVISÃO": "09:45"},
#         {"POSIÇÃO": "3º", "NOME": "Ana", "SENHA": "D103", "PREVISÃO": "10:00"}
# ]
schedules = [
    {"NOME": "Rogério", "SENHA": "A122", "CHEGADA": "2025-10-01 08:00:00", "ATENDIMENTO": "2025-10-01 08:30:00"},
]

# Define a list of ticket formats with their respective rules.
severities ={
    "A": {"description": "Emergência", "rule": ""},
    "B": {"description": "Urgência", "rule": ""},
    "C": {"description": "Idoso", "rule": ""},
    "D": {"description": "Normal", "rule": ""},
    "E": {"description": "Agendado", "rule": ""}
}

salas = [
    {"SALA": "101", "MÉDICO": "Dr. Lima"},
    {"SALA": "102", "MÉDICO": "Dra. Rocha"},
    {"SALA": "103", "MÉDICO": "Dr. Souza"}
]

pacientes_em_atendimento = [
]

def get_next_patient():
    """
    This function transforms the patient from the queue into a pacient being served and add to the list of patients being served for the same room.
    The function also removes the patient from the queue.
    
    returns the list of patients being served in each room.
    Example:
    
    """
    next_patient = {}
    try:
        patient = arrivals[0]
    except IndexError:
        return None
    next_patient["DESTINO"] = salas[0]["SALA"]
    next_patient["PRIORIDADE"] = "Emergência"
    next_patient["NOME"] = patient["NOME"]
    next_patient["SENHA"] = patient["SENHA"]
    arrivals.pop(0)
    # if room of the next patient is already in use, replace it with the next one othewise add it to the list of patients being served.
    # for room in pacientes_em_atendimento:
    #     if room["DESTINO"] == next_patient["DESTINO"]:
    #         room["NOME"] = next_patient["NOME"]
    #         room["SENHA"] = next_patient["SENHA"]
    #         break
    #
    
    pacientes_em_atendimento.append(next_patient)
    return pacientes_em_atendimento
    """
    Calculates the next patient to be called based on the the rule for the entire patient queue.
    The rules are as follows:
    # Define a method to get the next patient
    # 1- If there is on A patient in the queue, return it.
    # 2- If there is no A patient, return the next B patient.
    # 3- If there is no A or B patient, return the next C patient.
    # 4- If there is no A, B or C patient, return the next D patient.
    # 5- Check the current time and return the next E patient.
    Example queue =  [
        {"POSIÇÃO": "Em Atendimento", "NOME": "Rogério", "SENHA": "A122", "PREVISÃO": " - "},
        {"POSIÇÃO": "1º", "NOME": "Maria", "SENHA": "B101", "PREVISÃO": "Próxima Chamada"},
        {"POSIÇÃO": "2º", "NOME": "Carlos", "SENHA": "C102", "PREVISÃO": "09:45"},
        {"POSIÇÃO": "3º", "NOME": "Ana", "SENHA": "D103", "PREVISÃO": "10:00"}
    ]
    """
    """
    # Rule 1
    if any(patient["SENHA"].startswith("A") for patient in arrivals):
        p = next(patient for patient in arrivals if patient["SENHA"].startswith("A"))
        
        arrivals.remove(p)
        return p
    # Rule 2
    if any(patient["SENHA"].startswith("B") for patient in arrivals):
        p = next(patient for patient in arrivals if patient["SENHA"].startswith("B"))
        arrivals.remove(p)
        return p
    # Rule 3
    if any(patient["SENHA"].startswith("C") for patient in arrivals):
        p = next(patient for patient in arrivals if patient["SENHA"].startswith("C"))
        arrivals.remove(p)
        return p
    # Rule 4
    
    
    """