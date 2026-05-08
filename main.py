# Criar um sistema SSR 

from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db, Usuario

app = FastAPI(title="Sistema de login simples")

# Rodar o codigo:
# python -m uvicorn main:app --reload

templates = Jinja2Templates(directory="templates")
# Rota - Metodo HTML (get, post)

@app.get("/cadastro")
def tela_cadastro(request: Request):
    return templates.TemplateResponse(
        request,
        "cadastro.html",
        {"request": request}
    )

@app.get("/login")
def tela_login(request: Request):
    return templates.TemplateResponse(
        request,
        "login.html",
        {"request": request}
    )

@app.get("/")
def tela_inicial(request: Request):
    return templates.TemplateResponse(
        request,
        "home.html",
        {"request": request}
    )

#Post - Criar um usuário
@app.post("/cadastro")
def cadastrar_usuario(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db) #dependência com a tabela
):
    #Procurar o email no banco de dados.
    user_existente = db.query(Usuario).filter_by(email=email).first()

    if user_existente:
        return templates.TemplateResponse(
            request,
            "cadastro.html",
            {"request": request, "erro": "Email: já cadastrado."}
        )
    #Criando um objeto
    novo_usuario = Usuario(email=email, senha=senha)
    db.add(novo_usuario)
    db.commit()

    return RedirectResponse(url="/login", status_code=303)