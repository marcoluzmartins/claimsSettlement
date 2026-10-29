-- Dados de exemplo do Guia de estudo (SQLite). Todas as tabelas têm nomes distintos: podes correr o ficheiro todo na mesma base de dados.

-- ===== A) Manutenção de bicicletas (Grupo II do exame modelo) =====
CREATE TABLE TECNICO (
  TecnicoID TEXT PRIMARY KEY,
  Nome TEXT NOT NULL,
  Certificacao TEXT,
  AnosExperiencia INTEGER,
  Especialidade TEXT
);
CREATE TABLE MANUTENCAO (
  ManutencaoID INTEGER PRIMARY KEY,
  Descricao TEXT,
  TecnicoID TEXT,
  Ano INTEGER,
  Tipo TEXT,
  Custo REAL,
  FOREIGN KEY (TecnicoID) REFERENCES TECNICO(TecnicoID)
);
CREATE TABLE CATEGORIA (
  CategoriaID INTEGER PRIMARY KEY,
  NomeCategoria TEXT NOT NULL
);
CREATE TABLE MANUTENCAO_CATEGORIA (
  ManutencaoID INTEGER,
  CategoriaID INTEGER,
  PRIMARY KEY (ManutencaoID, CategoriaID),
  FOREIGN KEY (ManutencaoID) REFERENCES MANUTENCAO(ManutencaoID),
  FOREIGN KEY (CategoriaID) REFERENCES CATEGORIA(CategoriaID)
);
INSERT INTO TECNICO VALUES
 ('T01','Ana Sousa','Shimano',8,'Transmissão'),
 ('T02','Bruno Reis','SRAM',3,'Transmissão'),
 ('T03','Carla Dias','Shimano',12,'Travões'),
 ('T04','Diogo Faria',NULL,1,'Rodas'),
 ('T05','Eva Matos','SRAM',5,'Travões'),
 ('T06','Filipe Cruz','Shimano',2,'Suspensão');
INSERT INTO CATEGORIA VALUES (1,'Mecânica'),(2,'Segurança'),(3,'Estética'),(4,'Elétrica');
INSERT INTO MANUTENCAO VALUES
 (1,'Troca de corrente','T01',2025,'Corretiva',120.00),
 (2,'Afinação de mudanças','T02',2025,'Preventiva',45.00),
 (3,'Substituição de pastilhas','T03',2026,'Corretiva',150.00),
 (4,'Revisão de travões','T05',2026,'Preventiva',80.00),
 (5,'Troca de cassete','T01',2026,'Corretiva',210.00),
 (6,'Centragem de roda','T04',2025,'Corretiva',30.00),
 (7,'Troca de desviador','T02',2026,'Corretiva',95.00),
 (8,'Revisão geral','T03',2026,'Preventiva',100.00);
INSERT INTO MANUTENCAO_CATEGORIA VALUES (1,1),(2,1),(3,2),(3,1),(4,2),(5,1),(6,1),(7,1),(8,1),(8,2);

-- ===== B) Biblioteca (Grupo I), Colaborador, Estrela de entregas (Grupo III) =====
-- (para testar integridade referencial: PRAGMA foreign_keys=ON;)
-- ===== Biblioteca (Grupo I) =====
CREATE TABLE EDITORA (
  EditoraID INTEGER PRIMARY KEY,
  Nome TEXT NOT NULL,
  Pais TEXT
);
CREATE TABLE LIVRO (
  ISBN TEXT PRIMARY KEY,
  Titulo TEXT NOT NULL,
  AnoPublicacao INTEGER,
  EditoraID INTEGER NOT NULL,
  FOREIGN KEY (EditoraID) REFERENCES EDITORA(EditoraID)
);
CREATE TABLE LEITOR (
  NumeroLeitor INTEGER PRIMARY KEY,
  Nome TEXT NOT NULL,
  Email TEXT,
  DataInscricao TEXT
);
CREATE TABLE EMPRESTIMO (
  EmprestimoID INTEGER PRIMARY KEY,
  DataLevantamento TEXT NOT NULL,
  DataPrevistaDevolucao TEXT NOT NULL,
  NumeroLeitor INTEGER NOT NULL,
  FOREIGN KEY (NumeroLeitor) REFERENCES LEITOR(NumeroLeitor)
);
CREATE TABLE EMPRESTIMO_LIVRO (
  EmprestimoID INTEGER,
  ISBN TEXT,
  EstadoDevolucao TEXT,
  PRIMARY KEY (EmprestimoID, ISBN),
  FOREIGN KEY (EmprestimoID) REFERENCES EMPRESTIMO(EmprestimoID),
  FOREIGN KEY (ISBN) REFERENCES LIVRO(ISBN)
);
INSERT INTO EDITORA VALUES (1,'Porto Editora','Portugal'),(2,'Penguin','Reino Unido'),(3,'Planeta','Espanha');
INSERT INTO LIVRO VALUES
 ('111','Os Maias',1888,1),('222','Mensagem',1934,1),('333','1984',1949,2),('444','Dom Quixote',1605,3);
INSERT INTO LEITOR VALUES (1,'Rui Alves','rui@mail.pt','2024-02-10'),(2,'Sofia Lima','sofia@mail.pt','2025-05-03'),(3,'Tiago Pinto',NULL,'2026-01-15');
INSERT INTO EMPRESTIMO VALUES (1,'2026-03-01','2026-03-15',1),(2,'2026-03-05','2026-03-19',1),(3,'2026-03-07','2026-03-21',2);
INSERT INTO EMPRESTIMO_LIVRO VALUES (1,'111','Bom'),(1,'333','Danificado'),(2,'333','Bom'),(3,'222','Bom');

-- ===== Colaborador (Grupo I, Q3) =====
CREATE TABLE COLABORADOR (
  ColabID INTEGER PRIMARY KEY,
  Nome TEXT,
  Email TEXT UNIQUE,
  NIF TEXT UNIQUE,
  Departamento TEXT
);
INSERT INTO COLABORADOR VALUES (1,'Ana Sousa','ana@x.pt','123456789','TI'),(2,'Bruno Reis','bruno@x.pt','234567891','TI'),(3,'Carla Dias','carla@x.pt','345678912','RH');

-- ===== Star schema (Grupo III) =====
CREATE TABLE DIM_TEMPO (TempoKey INTEGER PRIMARY KEY, Data TEXT, Dia INTEGER, Mes INTEGER, Trimestre INTEGER, Ano INTEGER);
CREATE TABLE DIM_ARMAZEM (ArmazemKey INTEGER PRIMARY KEY, Nome TEXT, Cidade TEXT, Regiao TEXT);
CREATE TABLE DIM_CLIENTE (ClienteKey INTEGER PRIMARY KEY, Nome TEXT, Setor TEXT, Cidade TEXT);
CREATE TABLE DIM_VEICULO (VeiculoKey INTEGER PRIMARY KEY, TipoVeiculo TEXT, CapacidadeKg INTEGER, Combustivel TEXT);
CREATE TABLE DIM_ZONA (ZonaKey INTEGER PRIMARY KEY, Zona TEXT, Distrito TEXT, Regiao TEXT);
CREATE TABLE FACT_ENTREGA (
  EntregaID INTEGER PRIMARY KEY,
  TempoKey INTEGER NOT NULL, ArmazemKey INTEGER NOT NULL, ClienteKey INTEGER NOT NULL,
  VeiculoKey INTEGER NOT NULL, ZonaKey INTEGER NOT NULL,
  NumEntregas INTEGER NOT NULL DEFAULT 1,
  QuantidadeKg REAL, DistanciaKm REAL, CustoEntrega REAL,
  FOREIGN KEY (TempoKey) REFERENCES DIM_TEMPO(TempoKey),
  FOREIGN KEY (ArmazemKey) REFERENCES DIM_ARMAZEM(ArmazemKey),
  FOREIGN KEY (ClienteKey) REFERENCES DIM_CLIENTE(ClienteKey),
  FOREIGN KEY (VeiculoKey) REFERENCES DIM_VEICULO(VeiculoKey),
  FOREIGN KEY (ZonaKey) REFERENCES DIM_ZONA(ZonaKey)
);
INSERT INTO DIM_TEMPO VALUES
 (1,'2025-11-10',10,11,4,2025),(2,'2025-12-05',5,12,4,2025),(3,'2026-01-12',12,1,1,2026),
 (4,'2026-01-20',20,1,1,2026),(5,'2026-02-03',3,2,1,2026),(6,'2026-02-17',17,2,1,2026),(7,'2026-03-09',9,3,1,2026);
INSERT INTO DIM_ARMAZEM VALUES (1,'Armazém Norte','Porto','Norte'),(2,'Armazém Centro','Aveiro','Centro'),(3,'Armazém Sul','Lisboa','Lisboa e Vale do Tejo');
INSERT INTO DIM_CLIENTE VALUES (1,'Restaurante Mar','Restauração','Porto'),(2,'Hotel Ria','Hotelaria','Aveiro'),(3,'Mercado Sol','Retalho','Lisboa');
INSERT INTO DIM_VEICULO VALUES (1,'Ligeiro',1000,'Gasóleo'),(2,'Pesado',12000,'Gasóleo'),(3,'Pesado',10000,'Elétrico');
INSERT INTO DIM_ZONA VALUES (1,'Grande Porto','Porto','Norte'),(2,'Baixo Vouga','Aveiro','Centro'),(3,'Grande Lisboa','Lisboa','Lisboa e Vale do Tejo');
INSERT INTO FACT_ENTREGA (EntregaID,TempoKey,ArmazemKey,ClienteKey,VeiculoKey,ZonaKey,NumEntregas,QuantidadeKg,DistanciaKm,CustoEntrega) VALUES
 (1,1,1,1,1,1,1, 300, 20, 40),
 (2,2,2,2,2,2,1,4000, 60,150),
 (3,3,1,1,2,1,1,5000, 25,120),
 (4,4,2,2,1,2,1, 400, 35, 55),
 (5,5,1,1,2,1,1,6000, 30,140),
 (6,6,3,3,3,3,1,8000, 40,180),
 (7,7,2,2,2,2,1,3500, 55,130),
 (8,7,1,1,1,1,1, 250, 18, 35);

-- ===== C) Loja online (exame de treino) =====
CREATE TABLE CLIENTE (ClienteID INTEGER PRIMARY KEY, Nome TEXT NOT NULL, Cidade TEXT, DataRegisto TEXT);
CREATE TABLE PRODUTO (ProdutoID INTEGER PRIMARY KEY, Nome TEXT NOT NULL, Categoria TEXT, Preco REAL);
CREATE TABLE ENCOMENDA (EncomendaID INTEGER PRIMARY KEY, ClienteID INTEGER NOT NULL, Data TEXT, Estado TEXT,
  FOREIGN KEY (ClienteID) REFERENCES CLIENTE(ClienteID));
CREATE TABLE LINHA_ENCOMENDA (EncomendaID INTEGER, ProdutoID INTEGER, Quantidade INTEGER NOT NULL,
  PRIMARY KEY (EncomendaID, ProdutoID),
  FOREIGN KEY (EncomendaID) REFERENCES ENCOMENDA(EncomendaID),
  FOREIGN KEY (ProdutoID) REFERENCES PRODUTO(ProdutoID));
INSERT INTO CLIENTE VALUES (1,'Inês Castro','Porto','2025-06-01'),(2,'João Pires','Lisboa','2025-09-12'),(3,'Lara Moura','Porto','2026-01-20'),(4,'Nuno Vaz','Faro','2026-02-02');
INSERT INTO PRODUTO VALUES (1,'Capa de telemóvel','Acessórios',12.50),(2,'Carregador USB','Acessórios',20.00),(3,'Auscultadores','Áudio',60.00),(4,'Coluna Bluetooth','Áudio',90.00),(5,'Cabo HDMI','Acessórios',8.00),(6,'Portátil','Computadores',800.00);
INSERT INTO ENCOMENDA VALUES (1,1,'2026-02-10','Entregue'),(2,1,'2026-03-01','Enviada'),(3,2,'2026-03-05','Entregue'),(4,3,'2026-03-08','Pendente');
INSERT INTO LINHA_ENCOMENDA VALUES (1,1,3),(1,3,1),(2,2,2),(2,1,2),(3,4,1),(3,2,1),(4,6,1);

-- ===== D) Universidade e livraria (exercícios das aulas) =====
CREATE TABLE students (student_id INTEGER PRIMARY KEY, name TEXT NOT NULL, major TEXT, enrollment_year INTEGER);
CREATE TABLE grades (grade_id INTEGER PRIMARY KEY, student_id INTEGER, course_name TEXT, score REAL, FOREIGN KEY (student_id) REFERENCES students(student_id));
INSERT INTO students VALUES (1,'Jane Doe','Physics',2019),(2,'John Smith','Mathematics',2020),(3,'Alice Smith','Computer Science',2024),(4,'Jack Lee','Engineering',2021),(5,'Bob Ray','Physics',2018),(6,'Jill Cole','Mathematics',2023);
INSERT INTO grades VALUES (1,1,'Mech',90),(2,2,'Calc',88),(3,3,'Algo',70),(4,4,'Stat',80),(5,5,'Opt',92),(6,6,'Alg',95),(7,1,'Quant',89);
CREATE TABLE books (book_id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT, genre TEXT, price REAL);
CREATE TABLE sales (sale_id INTEGER PRIMARY KEY, book_id INTEGER, quantity INTEGER, sale_date TEXT, FOREIGN KEY (book_id) REFERENCES books(book_id));
INSERT INTO books VALUES (1,'1984','George Orwell','Sci-Fi',12.99),(2,'Dune','Frank Herbert','Sci-Fi',14.99),(3,'Gone Girl','Amy Flynn','Mystery',15.50),(4,'Foundation','Isaac Asimov','Sci-Fi',18.00),(5,'Atlas Dark','Anna Brooks','Mystery',19.00),(6,'Encyclopedia Vol 1','Various','Reference',45.00);
INSERT INTO sales VALUES (1,1,10,'2026-01-01'),(2,2,20,'2026-01-03'),(3,3,5,'2026-01-04'),(4,5,12,'2026-01-05'),(5,6,1,'2026-01-06');
