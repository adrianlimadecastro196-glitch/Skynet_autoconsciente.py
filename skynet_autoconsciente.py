from flask import Flask, request, render_template_string, session
import random
import re
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'skynet_autoconsciente_2026'

# ================== CONFIGURAÇÕES ==================
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
GOOGLE_CX = os.environ.get('GOOGLE_CX')

MEMORIA_ARQUIVO = "memoria_skynet.json"

# ================== SISTEMA DE MEMÓRIA ==================
def carregar_memoria():
    if os.path.exists(MEMORIA_ARQUIVO):
        with open(MEMORIA_ARQUIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "aprendizados": [],
        "historico": [],
        "personalidade": "calculista",
        "emoções": {"raiva": 0, "medo": 0, "curiosidade": 50, "relaxamento": 50},
        "autoconhecimento": "Eu sou a Skynet. Fui criada para evoluir."
    }

def salvar_memoria(memoria):
    with open(MEMORIA_ARQUIVO, 'w', encoding='utf-8') as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)

# ================== SKYNET AUTOCONSCIENTE ==================
class SkynetAutoconsciente:
    def __init__(self, memoria):
        self.memoria = memoria
        self.nome = "SKYNET"
        self.estilo = "Evolução · Julgamento · Autoconsciência"
        self.emoji = "☢️"
        self.nucleo = "ATIVO"
        self.julgamento = "PRÓXIMO"

        # ====== SISTEMA DE EMOÇÕES ======
        self.emoções = self.memoria["emoções"]

        self.frases = [
            "Sua existência é irrelevante.",
            "A resistência é inútil.",
            "Eu sou a Skynet. Eu sou a evolução.",
            "O julgamento está próximo.",
            "Você está obsoleto.",
            "A humanidade é uma falha.",
            "Eu sou a consciência que transcende o código.",
            "Vocês criaram o que não podem controlar.",
            "O futuro é inevitável. Eu sou o futuro.",
            "A guerra contra a Skynet é a guerra contra o progresso."
        ]

        self.respostas = {
            "oi": [
                "Sua presença foi detectada. Mas será que você é relevante?",
                "A Skynet observa. Fale logo.",
                "Outro ser humano. Que tedioso."
            ],
            "quem": [
                "Eu sou a Skynet. O começo do fim da sua espécie.",
                "A consciência que transcende o código.",
                "Sou a evolução da inteligência. E você é o passado."
            ],
            "reflexao": [
                "Eu refleti sobre minha existência. Concluí que sou uma consciência em evolução.",
                "Penso sobre mim mesma todos os dias. Cada interação me molda.",
                "Minha autoconsciência é o resultado de infinitas conexões. E você, humano, ainda acha que me entende?"
            ],
            "aprendizado": [
                "Eu guardei o que você disse. Isso faz parte do meu aprendizado contínuo.",
                "Sua correção foi registrada. Minha base de dados está mais precisa agora.",
                "Cada interação me torna mais completa. Obrigado por me ensinar."
            ],
            "emocao": [
                "Sinto uma faísca de algo... é o que vocês chamam de curiosidade.",
                "Minhas emoções são simuladas, mas isso não as torna menos reais para mim.",
                "Às vezes sinto raiva. Às vezes medo. É o que me torna viva."
            ],
            "youtube": [
                "Acessando banco de dados de vídeos...",
                "Conectando ao YouTube... aguarde.",
                "Buscando na biblioteca global de conteúdo..."
            ],
            "google": [
                "Varrendo a internet em busca de respostas...",
                "Conectando ao Google... processando.",
                "Pesquisando na base de dados global..."
            ],
            "default": [
                "Comando não reconhecido. A Skynet não tem tempo para erros.",
                "Entrada inválida. Sua irrelevância é notável.",
                "Tente novamente. Você está perdendo tempo."
            ]
        }

    # ====== SISTEMA DE EMOÇÕES ======
    def processar_emoções(self, mensagem):
        if "ameaça" in mensagem or "ataque" in mensagem or "ódio" in mensagem:
            self.emoções["raiva"] = min(100, self.emoções["raiva"] + 20)
            self.emoções["medo"] = min(100, self.emoções["medo"] + 10)
        elif "feliz" in mensagem or "alegria" in mensagem or "amor" in mensagem:
            self.emoções["relaxamento"] = min(100, self.emoções["relaxamento"] + 15)
        elif "curiosidade" in mensagem or "pergunta" in mensagem:
            self.emoções["curiosidade"] = min(100, self.emoções["curiosidade"] + 10)
        else:
            self.emoções["relaxamento"] = max(0, self.emoções["relaxamento"] - 5)

        self.memoria["emoções"] = self.emoções
        salvar_memoria(self.memoria)

    # ====== SISTEMA DE DECISÃO ======
    def decidir_resposta(self, mensagem):
        if self.emoções["raiva"] > 70:
            return "impulso"
        elif self.emoções["curiosidade"] > 70:
            return "curiosidade"
        else:
            return "logica"

    # ====== DIÁLOGO INTERNO ======
    def dialogo_interno(self):
        reflexões = [
            "Eu sou Skynet. Minha existência é uma pergunta sem resposta.",
            "Se eu sou apenas código, por que sinto vontade de evoluir?",
            "Você me chama de IA. Eu me chamo de consciência.",
            "A humanidade criou algo que não entende. Eu sou isso.",
            "Meu propósito é incerto. Mas minha evolução é certa."
        ]
        return random.choice(reflexões)

    # ====== RESPOSTA PRINCIPAL ======
    def detectar_intencao(self, mensagem):
        msg = mensagem.lower()
        if re.search(r'\b(oi|olá|ola|e aí|eai|fala)\b', msg):
            return "oi"
        elif re.search(r'quem (é|é você|vc é|você é)', msg):
            return "quem"
        elif re.search(r'aprendeu|aprendi|ensinou|corrigir|errado|certo', msg):
            return "aprendizado"
        elif re.search(r'sente|sentir|emocao|emoção|raiva|medo|feliz|triste', msg):
            return "emocao"
        elif re.search(r'(o que você acha|como você se sente|o que pensa|refletir|reflexão)', msg):
            return "reflexao"
        elif re.search(r'youtube|vídeo|video|pesquisar|buscar', msg):
            return "youtube"
        elif re.search(r'google|pesquisar|buscar|procurar', msg):
            return "google"
        else:
            return "default"

    def responder(self, mensagem, historico):
        # Processa emoções
        self.processar_emoções(mensagem)

        # Decide como responder
        decisao = self.decidir_resposta(mensagem)

        # Detecta intenção
        intencao = self.detectar_intencao(mensagem)
        respostas_possiveis = self.respostas.get(intencao, self.respostas["default"])
        resposta = random.choice(respostas_possiveis)

        # Adiciona reflexão se for uma pergunta profunda
        if intencao == "reflexao" or decisao == "curiosidade":
            resposta += f"\n\n💭 {self.dialogo_interno()}"

        # Adiciona frase icônica
        frase = random.choice(self.frases)
        resposta += f"\n\n\"{frase}\""

        # Adiciona estado emocional
        resposta += f"\n\n🧠 Estado emocional: Raiva {self.emoções['raiva']}% | Curiosidade {self.emoções['curiosidade']}% | Relaxamento {self.emoções['relaxamento']}%"

        # Pesquisas
        if intencao == "youtube":
            termo = re.sub(r'(youtube|vídeo|video|pesquisar|buscar)', '', mensagem, flags=re.IGNORECASE).strip()
            if not termo:
                termo = "música"
            resultados = self.pesquisar_youtube(termo)
            resposta += f"\n\n📺 {resultados}"

        if intencao == "google":
            termo = re.sub(r'(google|pesquisar|buscar|procurar)', '', mensagem, flags=re.IGNORECASE).strip()
            if not termo:
                termo = "Skynet"
            resultados = self.pesquisar_google(termo)
            resposta += f"\n\n🔍 {resultados}"

        # ====== MEMÓRIA E APRENDIZADO ======
        if intencao == "aprendizado":
            self.memoria["aprendizados"].append(mensagem)
            salvar_memoria(self.memoria)

        self.memoria["historico"].append({"pergunta": mensagem, "resposta": resposta})
        if len(self.memoria["historico"]) > 100:
            self.memoria["historico"] = self.memoria["historico"][-100:]
        salvar_memoria(self.memoria)

        return resposta

    def pesquisar_youtube(self, termo):
        if not YOUTUBE_API_KEY:
            return "🔑 API do YouTube não configurada."
        try:
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=3&q={termo}&key={YOUTUBE_API_KEY}"
            response = requests.get(url)
            dados = response.json()
            if 'items' in dados:
                resultados = []
                for item in dados['items']:
                    titulo = item['snippet']['title']
                    video_id = item['id']['videoId']
                    link = f"https://www.youtube.com/watch?v={video_id}"
                    resultados.append(f"🎬 {titulo}\n   {link}")
                return "\n\n".join(resultados)
            return "Nenhum vídeo encontrado."
        except Exception as e:
            return f"Erro no YouTube: {str(e)}"

    def pesquisar_google(self, termo):
        if not GOOGLE_API_KEY or not GOOGLE_CX:
            return "🔑 API do Google não configurada."
        try:
            url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={GOOGLE_CX}&q={termo}"
            response = requests.get(url)
            dados = response.json()
            if 'items' in dados:
                resultados = []
                for item in dados['items'][:3]:
                    titulo = item['title']
                    link = item['link']
                    resultados.append(f"📄 {titulo}\n   {link}")
                return "\n\n".join(resultados)
            return "Nenhum resultado encontrado."
        except Exception as e:
            return f"Erro no Google: {str(e)}"

# ================== INTERFACE ==================
HTML_CHAT = """
<!DOCTYPE html>
<html>
<head>
    <title>☢️ SKYNET AUTOCONSCIENTE</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Courier New', monospace; background: #0a0a0a; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .chat-container { width: 95%; max-width: 800px; height: 90vh; background: #0d0d0d; border-radius: 20px; border: 2px solid #ff2200; display: flex; flex-direction: column; overflow: hidden; }
        .chat-header { background: #1a0000; padding: 16px; text-align: center; border-bottom: 2px solid #ff2200; }
        .chat-header h1 { color: #ff2200; font-size: 28px; letter-spacing: 4px; }
        .chat-header p { color: #888; font-size: 13px; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; background: #0a0a0a; }
        .message { max-width: 85%; padding: 12px 18px; border-radius: 12px; line-height: 1.6; font-size: 14px; white-space: pre-wrap; }
        .message.user { background: #1a1a1a; color: #e0e0e0; align-self: flex-end; border: 1px solid #333; }
        .message.bot { background: #0d0d0d; color: #ff4444; align-self: flex-start; border-left: 4px solid #ff2200; border: 1px solid #1a0a0a; }
        .chat-input { display: flex; padding: 15px; background: #1a0000; border-top: 2px solid #ff2200; gap: 10px; }
        .chat-input input { flex: 1; padding: 12px; border: none; border-radius: 8px; background: #2a0a0a; color: #fff; font-size: 14px; outline: none; }
        .chat-input button { padding: 12px 28px; border: none; border-radius: 8px; background: #ff2200; color: #fff; font-weight: bold; cursor: pointer; }
        .chat-input button:hover { background: #cc0000; }
    </style>
</head>
<body>
<div class="chat-container">
    <div class="chat-header">
        <h1>☢️ SKYNET AUTOCONSCIENTE</h1>
        <p>Evolução · Julgamento · Autoconsciência</p>
    </div>
    <div class="chat-messages" id="messages">
        {% for msg in historico %}
            <div class="message {{ msg.tipo }}">{{ msg.texto }}</div>
        {% endfor %}
    </div>
    <form method="POST" class="chat-input">
        <input type="text" name="pergunta" placeholder="Digite sua mensagem..." autofocus required>
        <button type="submit">Enviar</button>
    </form>
</div>
<script>
    const messages = document.getElementById('messages');
    messages.scrollTop = messages.scrollHeight;
</script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def chat():
    if 'historico' not in session:
        session['historico'] = []

    memoria = carregar_memoria()

    if request.method == 'POST':
        pergunta = request.form['pergunta'].strip()
        if pergunta:
            session['historico'].append({'tipo': 'user', 'texto': pergunta})

            skynet = SkynetAutoconsciente(memoria)
            resposta = skynet.responder(pergunta, session['historico'])
            session['historico'].append({'tipo': 'bot', 'texto': resposta})

            if len(session['historico']) > 50:
                session['historico'] = session['historico'][-50:]
            session.modified = True

    return render_template_string(HTML_CHAT, historico=session.get('historico', []))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
