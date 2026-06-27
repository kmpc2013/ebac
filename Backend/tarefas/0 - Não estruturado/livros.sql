-- Passo 1
create table Livros(
  id INT PRIMARY KEY,
  titulo varchar(254),
  autor varchar(100),
  ano int,
  genero varchar(50),
  disponível bool
  );
  
-- Passo 2
INSERT INTO Livros (id, titulo, autor, ano, genero, disponível) VALUES (1, 'livro_A', 'Autor_A', 1930, 'suspense', true);
INSERT INTO Livros (id, titulo, autor, ano, genero, disponível) VALUES (2, 'livro_B', 'Autor_A', 1940, 'terror', false);
INSERT INTO Livros (id, titulo, autor, ano, genero, disponível) VALUES (3, 'livro_C', 'Autor_A', 1950, 'ação', true);
INSERT INTO Livros (id, titulo, autor, ano, genero, disponível) VALUES (4, 'livro_D', 'Autor_A', 1960, 'fantasia', false);
INSERT INTO Livros (id, titulo, autor, ano, genero, disponível) VALUES (5, 'livro_E', 'Autor_A', 1970, 'terror', true);

-- Passo 3
SELECT * FROM Livros WHERe disponível = true;

-- Passo 4
UPDATE Livros set disponível = false where titulo = 'livro_E';

-- Passo 5
SELECT * FROM Livros order by ano DESC;

-- Passo 6
DELETe FROM Livros Where ano < 1940;

-- Passo 7
DROP TABLE Livros;
create table Livros(
  id INT PRIMARY KEY,
  titulo varchar(254),
  autor varchar(100),
  ano int,
  genero varchar(50),
  disponível bool
  );
