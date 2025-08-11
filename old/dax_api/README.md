# Clinica dax-b
Projeto de um sistema de gerenciamento de pacientes em consultas de uma clinica.
A ideia é ter uma TV mostrando o status de todas as 

# ISSUES
1- Como clinica quero configurar se a definição de sala é feita durante o check-in (por especialidade) ou a sala é escolhida quando estiver desocupada (atendimento emergencial)?

2- Como paciente, quero ser alertado da minha vez com uma mensagem de audio
    * Fazer o iframe da esquerda tocar o audio para cada atualizaçao

3- Como paciente, quero ser alertado da minha vez com um SMS no meu celular, se cadastrado.
    * Twilio

4- Como paciente, quero visualizar se eu já fui chamado.
    * Iframe da esquerda deve conter o ultimo paciente que entrou para cada sala.
    * Iframe deve ter status "CHAMANDO" e "EM ATENDIMENTO"

5- Como paciente, quero visualizar o tempo que estou esperando na fila.

6- Como paciente, quero visualizar que médicos estão disponíveis para atendimento.

7- Como paciente, quero visualizar o tempo de espera para ser atendido.

# ARCHITECTURE SUGGESTED
https://github.com/seapagan/fastapi_async_sqlalchemy2_example


# STANDARD NAMES
1- 


# MAQUINA DE ESTADOS

* 1 - Gera a senha
* 3 - Avaliação do paciente: Cadastre nome, especialidade e urgência
* 4 - Atribuição de sala
* 5 - Inicio Atendimento
* 6 - Encerra Atendimento ou...
* 7 - Encaminhamento a outro painel (outra especialidade) se aplicavel.
