# 🚀 DevOpsPipeLens

DevOpsPipeLens é uma aplicação web que analisa arquivos YAML de pipelines CI/CD (ex: GitLab) e arquivos de infraestrutura como código (IaC), como Terraform. A ferramenta utiliza regras internas e integrações com ferramentas como `checkov`, `tflint` e `tfsec` para avaliar a qualidade, segurança e boas práticas dos pipelines e recursos de nuvem descritos no código.

---

## 🧠 Funcionalidades

- ✅ Análise de arquivos YAML de pipeline (GitLab CI/CD)
- 📊 Métricas por análise com visualização de gráfico
- 🧾 Geração de relatório em PDF com nota, alertas e sugestões
- 💡 Sugestões automáticas de melhoria para a pipeline
- 🕵️ Integração com `checkov`, `tflint`, `tfsec` para IaC (Terraform) [X] Em Desenvolvimento 
- 📈 Histórico das análises com visualização por data
- 🧩 API REST desenvolvida com FastAPI

---

## 🛠️ Tecnologias Utilizadas

| Componente       | Tecnologia                  |
|------------------|-----------------------------|
| Backend          | Python, FastAPI, FPDF       |
| Análise de IaC   | checkov, tflint, tfsec      |
| Frontend         | React + Vite + Chart.js     |
| Estilização      | CSS3                        |
| Relatórios       | PDF com gráficos            |

---

## 📦 Pré-requisitos

- Python 3.9+
- Node.js 18+ (para rodar o frontend)
- Ferramentas CLI opcionais (para análise IaC):
  - [checkov](https://github.com/bridgecrewio/checkov)
  - [tflint](https://github.com/terraform-linters/tflint)
  - [tfsec](https://github.com/aquasecurity/tfsec)

---

## ▶️ Como rodar o backend

```bash
# 1. Vá para a pasta do app
cd app

# 2. Crie o ambiente virtual
python3 -m venv venv

# 3. Ative o ambiente virtual
source venv/bin/activate  # (Linux/macOS)

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Inicie a aplicação FastAPI
uvicorn main:app --reload
```

A API estará disponível em: http://127.0.0.1:8000

Você pode visualizar a documentação da API via Swagger em: http://127.0.0.1:8000/docs

## Frontend Ainda não adicionado no repo

💻 Como rodar o frontend
```bash
# 1. Vá para a pasta do frontend
cd frontend

# 2. Instale as dependências
npm install

# 3. Inicie o projeto
npm run dev
```

## O frontend estará disponível em: http://localhost:5173

## 📄 Endpoints disponíveis
| Método | Rota                  | Descrição                                      |
|--------|-----------------------|------------------------------------------------|
| POST   | /analyze              | Faz análise do YAML enviado                    |
| GET    | /history              | Retorna histórico de análises                  |
| GET    | /metrics              | Retorna métricas de análises                   |
| GET    | /jobs/details         | Detalhes dos últimos jobs analisados           |
| GET    | /score/average        | Score médio geral das análises                 |
| GET    | /warnings/frequent    | Warnings mais frequentes                       |
| GET    | /suggestions/random   | Sugestão aleatória gerada                      |
| GET    | /report               | Gera e retorna PDF com resumo e gráfico        |


## 🧪 Futuras melhorias
- ✅ Upload múltiplo de arquivos para análise
- 🔐 Login com autenticação JWT
- 📡 Armazenamento em banco de dados (SQLite/PostgreSQL)
- 🤖 Integração com modelos de IA para avaliação inteligente
- 🔍 Análise de vulnerabilidades e segurança em tempo real

👨‍💻 Autor
Desenvolvido por Cassius Clay Filo
📫 [linkedin.com/in/cassiussilva](https://www.linkedin.com/in/cassius-clay-filho/)
