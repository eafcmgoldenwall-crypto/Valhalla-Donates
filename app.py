from flask import Flask, render_template, request
from supabase import create_client
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv(
    os.path.join(os.path.dirname(__file__), ".env"),
    override=True
)

app = Flask(__name__)

# Conexão com o Supabase
url = os.getenv("SUPABASE_URL")
chave = os.getenv("SUPABASE_KEY")

if not url or not chave:
    raise ValueError("Verifique as configurações do arquivo .env.")

supabase = create_client(url, chave)

print("Projeto:", url)
print("Conexão configurada:", bool(chave))


# Página inicial
@app.route("/")
def inicio():
    return render_template(
        "ValhallaMarket.html",
        sucesso=False
    )


# Receber doações
@app.route("/doar", methods=["POST"])
def doar():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    valor = request.form.get("valor", "").strip()
    mensagem = request.form.get("mensagem", "").strip()

    # Verificar campos obrigatórios
    if not nome or not email or not valor:
        return "Preencha todos os campos obrigatórios.", 400

    # Dados da doação
    dados = {
        "nome": nome,
        "email": email,
        "valor": valor,
        "mensagem": mensagem
    }

    try:
        # Salvar no Supabase
        supabase.table("doacoes").insert(
            dados,
            returning="minimal"
        ).execute()

        # Mostrar tela de agradecimento
        return render_template(
            "ValhallaMarket.html",
            sucesso=True
        )

    except Exception as erro:
        print("Erro ao registrar doação:", erro)
        return "Não foi possível registrar sua doação. Tente novamente.", 500


if __name__ == "__main__":
    app.run(debug=True)