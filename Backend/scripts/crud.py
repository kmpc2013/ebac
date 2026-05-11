from fastapi import FastAPI, HTTPException

app = FastAPI()

livros = {}

@app.get("/livros")
def get_livros():
    if not livros:
        return {"message": "Nenhum livro encontrado."}
    return {"livros": livros}

@app.post("/adiciona")
def post_livro(id: int, titulo: str, autor: str, ano: int):
    if id in livros:
        raise HTTPException(status_code=400, detail="Livro já existe.")
    livros[id] = {"titulo": titulo, "autor": autor, "ano": ano}
    return {"message": "Livro adicionado com sucesso."}

@app.put("/atualiza/{id}")
def put_livro(id: int, titulo: str, autor: str, ano: int):
    livro = livros.get(id)
    if not livros:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    if titulo:
        livro["titulo"] = titulo
    if autor:
        livro["autor"] = autor
    if ano:
        livro["ano"] = ano
    return {"message": "Livro atualizado!!"}

@app.delete("/deletar/{id}")
def delete_livro(id: int):
    if id not in livros:
        raise HTTPException(status_code=404, detail="Livro não econtrado")
    del livros[id]
    return {"message": "Livro DELETADO!!"}