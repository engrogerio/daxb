import sys

from abc import ABC, abstractmethod
import pdb

class State(ABC):

	@abstractmethod
	def cadastrar(self):
		pass

	@abstractmethod
	def aguardar(self):
		pass

	@abstractmethod
	def chamar(self):
		pass
	
	@abstractmethod
	def dispensado(self):
		pass

class Paciente(State):
	def __init__(self):
		self.nome: str = ''
		self.senha: str = ''
		self.idade: int = 0
		self.prioridade: str = ''
		self.state = Checked_in(self)
	
	def __repr__(self):
		return str(self.__class__.__name__)

	def cadastrar(self):
		self.state = self.state.cadastrar()
		return self.state

	def aguardar(self):
		self.state = self.state.aguardar()
		return self.state

	def chamar(self):
		self.state = self.state.chamar()
		return self.state
	
	def dispensado(self):
		self.state = self.state.dispensado()
		return self.state

class Checked_in(State):
	def __init__(self, paciente: Paciente):
		self.paciente = paciente
		self.paciente.nome = input('Nome: ')
		self.paciente.senha = input('Senha: ')
		self.paciente.idade = int(input('Idade: '))
		self.paciente.prioridade = input('Prioridade: ')
		print('Paciente Cadastrado')
		# pdb.set_trace()
	def __repr__(self):
		return str(self.__class__.__name__)

	def cadastrar(self):
		return self

	def aguardar(self):
		return Aguardando()

	def chamar(self):
		return Chamado()
	
	def dispensado(self):
		return Checked_out()
    
class Aguardando(State):

	def __inits__(self, paciente: Paciente):
		self.paciente = paciente
		print('Paciente Aguardando')
  
	def __repr__(self):
		return str(self.__class__.__name__)

	def cadastrar(self):
		return Checked_in()

	def aguardar(self):
		return self

	def chamar(self):
		return Chamado()
	
	def dispensado(self):
		return Checked_out()

class Chamado(State):
	def __inits__(self, paciente: Paciente):
		self.paciente = paciente
		print('Paciente Chamado !')
  
	def __repr__(self):
		return str(self.__class__.__name__)

	def cadastrar(self):
		return self

	def aguardar(self):
		return self

	def chamar(self):
		return self
	
	def dispensado(self):
		return Checked_out()

class Atendendo(State):
	def __inits__(self, paciente: Paciente):
		self.paciente = paciente
		print('Paciente Atendendo')
  
	def __repr__(self):
		return str(self.__class__.__name__)

	def cadastrar(self):
		return self

	def aguardar(self):
		return self

	def chamar(self):
		return self
	
	def dispensado(self):
		return Checked_out()

class Checked_out(State):
	def __inits__(self, paciente: Paciente):
		self.paciente = paciente
		print('Paciente Dispensado')
  
	def __repr__(self):
		return str(self.__class__.__name__)

	def cadastrar(self):
		return self

	def aguardar(self):
		return self

	def chamar(self):
		return self
	
	def dispensado(self):
		return self

