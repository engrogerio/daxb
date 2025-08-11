# uuid as id



customer = {
    "customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", 
    "name": "Unimed", 
    "title":"", 
    "data": {}, 
    "created_at": "2025-10-01 08:00:00", 
    "updated_at": "2025-10-01 08:00:00"
}


severities ={
    "A": {"id": "", "description": "Emergência","customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "rule": ""},
    "B": {"id": "", "description": "Urgência","customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "rule": ""},
    "C": {"id": "", "description": "Idoso","customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "rule": ""},
    "D": {"id": "", "description": "Normal","customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "rule": ""},
    "E": {"id": "", "description": "Agendado","customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "rule": ""}
}

arrivals =  [
    {"id": "", "customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "is_scheduled": true, "scheduled_at": "2025-10-01 08:00:00", "scheduled_doctor_id":"", "name": "Rogério", "age": 30, "ticket": "A122", "arrival": "2025-10-01 08:00:00"},
    {"id": "", "customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "is_scheduled": false, "scheduled_at": "", "scheduled_doctor_id":"", "name": "Maria", "age": 25, "ticket": "B101", "arrival": "2025-10-01 09:00:00"},

status = [
    {"id": "", "customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "description": "Em espera"},
    {"id": "", "customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "description": "Em atendimento"},
    {"id": "", "customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "description": "Atendido"},
    {"id": "", "customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "description": "Cancelado"},
    {"id": "", "customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "description": "Faltou"},
]

arrival_status = [
    {"id": "", "customer_id": "76e9998f-e5de-43d0-885b-00a141eaf653", "arrival_id": "", "status_id": ""},

rooms = [
    {"id": "", "customer_id": "", "name": "Sala 1", "capacity": 1},
    {"id": "", "customer_id": "", "name": "Sala 2", "capacity": 1},
    {"id": "", "customer_id": "", "name": "Sala 3", "capacity": 1},
]
doctors = [
    {"id": "", "customer_id": "", "name": "Dr. Lima", "specialty": "Cardiologia", "room_id": ""},
    {"id": "", "customer_id": "", "name": "Dra. Rocha", "specialty": "Ginecologia", "room_id": ""},
    {"id": "", "customer_id": "", "name": "Dr. Souza", "specialty": "Oftalmologia", "room_id": ""}
]


create table dax.public.patient (
    id uuid primary key,
    customer_id uuid,
    name text,
    age integer,
    ticket text,
    arrival timestamp
);

create table dax.public.status (
    id uuid primary key,
    customer_id uuid,
    description text
);