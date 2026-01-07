# Projeto de Estágio – <Luis Belchior>

## 📌 Descrição
Este projeto consiste no desenvolvimento de um sistema web chamado "IPEMA" inspirado no ipma, destinado à gestão de observações meteorológicas e marítimas. O sistema permite aos utilizadores registarem-se, adicionarem observações, consultarem feeds globais e gerirem os seus dados pessoais, integrando funcionalidades de CRUD (Criar, Ler, Atualizar, Eliminar).

## 🎯 Objetivos
- Criar uma plataforma para gestão de observações meteorológicas e marítimas.
- Permitir a criação, edição e eliminação de observações pelos utilizadores.
- Exibir feeds globais com observações de todos os utilizadores.
- Proporcionar uma interface moderna e responsiva, fácil de usar.
- Implementar autenticação e gestão de perfis de utilizador.
teste
## 🛠️ Tecnologias
- Linguagem: Python
- Frameworks: Django
- Ferramentas: HTML, CSS, JavaScript, SQLite (base de dados), Git, VS Code

## ▶️ Como executar
```bash
# Pré-requisitos
# - Python 3.13+ 
# - Git instalado
# - Pillow instalado
# - Pip atualizado

# Clonar o repositório
git clone https://github.com/ipma-divsi/django_project_formation.git

# Entrar na pasta do projeto
cd django_project_formation

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Windows (CMD)
venv\Scripts\activate.bat

# Linux / Mac
source venv/bin/activate

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install django

# Entrar na pasta onde está o manage.py
cd sistema

# Criar base de dados e aplicar migrações
python manage.py migrate

# Criar superutilizador (opcional)
python manage.py createsuperuser

# Executar o servidor
python manage.py runserver




django_project_formation/
│
├─ core/                  # Aplicação principal com modelos, views e templates
│  ├─ templates/core/     # HTML das páginas
│  ├─ static/core/        # CSS, imagens e JS
│  ├─ models.py           # Modelos de dados (Observações)
│  ├─ views.py            # Lógica das páginas e CRUD
│  └─ forms.py            # Formulários
│
├─ venv/                  # Ambiente virtual
├─ manage.py              # Script principal do Django
├─ db.sqlite3             # Base de dados SQLite
└─ requirements.txt       # Dependências do projeto


'
## 📝 Regras

- Commits pequenos e frequentes;
- Mensagens de commit claras
  - Estrutura de commit:
    - [Tipo] ID da Tarefa : descrição


## 👤 Autor

Luis belchior
Orientador: <teu nome>
# Projeto de Estágio – Luis Belchior