import discord
from discord.ext import commands
import json
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ARQUIVO = "dados.json"

# Criar arquivo se não existir
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w") as f:
        json.dump({"saldo": 0.0, "wins": 0, "losses": 0}, f)

def carregar():
    with open(ARQUIVO, "r") as f:
        return json.load(f)

def salvar(dados):
    with open(ARQUIVO, "w") as f:
        json.dump(dados, f, indent=4)

@bot.event
async def on_ready():
    print(f"Bot online como {bot.user}")

@bot.command()
async def win(ctx, valor: float):
    dados = carregar()
    dados["saldo"] += valor
    dados["wins"] += 1
    salvar(dados)

    await ctx.send(f"✅ Vitória registrada!\n💰 Saldo atual: R$ {dados['saldo']:.2f}")

@bot.command()
async def flop(ctx, valor: float):
    dados = carregar()
    dados["saldo"] -= valor
    dados["losses"] += 1
    salvar(dados)

    await ctx.send(f"❌ Derrota registrada!\n💰 Saldo atual: R$ {dados['saldo']:.2f}")

@bot.command()
async def painel(ctx):
    dados = carregar()
    await ctx.send(
        f"📊 **PAINEL**\n"
        f"🏆 Vitórias: {dados['wins']}\n"
        f"❌ Derrotas: {dados['losses']}\n"
        f"💰 Saldo: R$ {dados['saldo']:.2f}"
    )

bot.run(TOKEN)
