import discord
from discord.ext import commands
import json
import os

TOKEN = os.getenv("TOKEN")
OWNER_ID = os.getenv("OWNER_ID")

if OWNER_ID is None:
    print("OWNER_ID não encontrado!")
    OWNER_ID = 0
else:
    OWNER_ID = int(OWNER_ID)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = "dados.json"

def carregar():
    if not os.path.exists(DATA_FILE):
        return {"saldo": 0.0, "vitorias": 0, "derrotas": 0}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def salvar(dados):
    with open(DATA_FILE, "w") as f:
        json.dump(dados, f)

def formatar(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")

@bot.command()
async def win(ctx, valor: float):
    if ctx.author.id != OWNER_ID:
        return
    
    dados = carregar()
    dados["saldo"] += valor
    dados["vitorias"] += 1
    salvar(dados)

    await ctx.send(
        f"📊 **PAINEL**\n"
        f"🏆 Vitórias: {dados['vitorias']}\n"
        f"❌ Derrotas: {dados['derrotas']}\n"
        f"💰 Saldo: {formatar(dados['saldo'])}"
    )

@bot.command()
async def flop(ctx, valor: float):
    if ctx.author.id != OWNER_ID:
        return
    
    dados = carregar()
    dados["saldo"] -= valor
    dados["derrotas"] += 1
    salvar(dados)

    await ctx.send(
        f"📊 **PAINEL**\n"
        f"🏆 Vitórias: {dados['vitorias']}\n"
        f"❌ Derrotas: {dados['derrotas']}\n"
        f"💰 Saldo: {formatar(dados['saldo'])}"
    )

@bot.command()
async def limpar(ctx, quantidade: int):
    if ctx.author.id != OWNER_ID:
        return
    await ctx.channel.purge(limit=quantidade + 1)

bot.run(TOKEN)
