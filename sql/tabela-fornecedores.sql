CREATE TABLE fornecedores(
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	nome VARCHAR(250) NOT NULL,
	contato VARCHAR(300) NOT NULL,
	email VARCHAR(250),
	estado VARVCAR(250),
	cidade VARCHAR(250),
	tempoespera VARCHAR(250)
	
)