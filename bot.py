import discord
from discord.ext import commands
from time import sleep
import openai
import os
from dotenv import load_dotenv

load_dotenv()

chave_api = os.environ.get("API_GPT")
openai.api_key = chave_api

intents = discord.Intents.default()
intents.message_content = True

token = os.environ.get("DISCORD_TOKEN")
prefixo = '!'
bot = commands.Bot(command_prefix=prefixo,intents=intents)
kk = ['Boas vindas e Registros', 'boas-vindas-e-regras', 'recursos-e-notas', 'Canais Principais', 'bate-papos', 'ajuda-em-algum-problema', 'todos-projetos', 'Canais de voz', 'Sala de estudo 1', 'Sala de estudo 2', 'area-para-divulgar-conhecimentos', 'Linguagens', 'html', 'css', 'javascript-js', 'membros-novos', 'saidas-membros', 'niveis', 'bots', 'area-de-comandos-bots', 'comandos-dos-bots', 'Descanso', 'javascript-react', 'area-de-criacao-de-jogos']

nomes_canais = []

class DropdownView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Dropdown())

class Dropdown(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(value='comandos', label='Lista de Comandos')
        ]
        super().__init__(
            placeholder='Escolha uma opção...',
            min_values=1,
            max_values=1,
            options=options,
            custom_id="dropdown_menu"
        )

    async def callback(self, interaction: discord.Interaction):
        selected_value = self.values[0]

        if selected_value == "comandos":
            await comandos(interaction)

messageInfo = """"
    Comandos: !limpar -- !raid_canais -- !desraid_canais -- !chatgpt \n \n
    Exemplo Comando !limpar: '!limpar 15' \n
    Exemplo Comando !raid_canais: '!raid_canais' \n
    Exemplo Comando !desraid_canais: '!desraid_canais' \n
    Exemplo Comando !chatgpt: '!chatgpt Me explique a historia da terra'
"""

async def comandos(interaction):
    await interaction.response.send_message(messageInfo)

@bot.command(name='menu', help='Abre um menu dropdown')
async def menu(ctx):
    view = DropdownView()
    await ctx.send("Escolha uma opção:", view=view)

@bot.command(name='raid_canais')
async def listar_canais(ctx):
    guild = ctx.guild

    # Percorre todos os canais no servidor
    for channel in guild.channels:
        sleep(0.4)
        nomes_canais.append(channel.name)
        await channel.edit(name='Eu amo pudim 🍮')

    for channel in guild.channels:
        sleep(0.4)
        if isinstance(channel, discord.TextChannel):
            await channel.send('Toma pudim seus filhas da puta: 🍮')

@bot.command(name='desraid_canais')
async def listar_canais(ctx):
    guild = ctx.guild

    # Percorre todos os canais no servidor
    if nomes_canais:
        for i,channel in enumerate(guild.channels):
            sleep(0.4)
            nomes_canais.append(channel.name)
            await channel.edit(name=nomes_canais[i])

        for channel in guild.channels:
            sleep(0.4)
            if isinstance(channel, discord.TextChannel):
                async for message in channel.history(limit=10):
                    if message.author == bot.user:
                        await channel.purge(limit=2)

@bot.command(name='limpar')
async def limpar(ctx, quantidade: int):
    if ctx.author.guild_permissions.manage_messages:
        if quantidade > 80:
            await ctx.send('Quantidade Muito Alta. Aceito Apenas Apagar de 80 Pra Baixo')
        else:
            await ctx.channel.purge(limit=quantidade + 1)
            await ctx.send(f'{quantidade} mensagens foram apagadas por {ctx.author.mention}.', delete_after=5)
    else:
        await ctx.send('Você não tem permissão para gerenciar mensagens.')

@bot.command('criarCanal')
async def criarCanais(ctx, nome: str):
    guild = ctx.guild
    try:
        await guild.create_text_channel(nome)  
    except:
        await ctx.send('Nome não pode conter espaço')

@bot.command('mudarNomeCanal')
async def mudarNomeCanais(ctx, alvo: discord.TextChannel, novo_nome: str):
    try:
        await alvo.edit(name=novo_nome)
    except:
        await ctx.send('Não foi possivel mudar o nome do {} para {}'.format(alvo,novo_nome))

@bot.command(name='chatgpt')
async def enviarMensagem(ctx):
    mensagem = ctx.message.content.split('!chatgpt')
    mensagem = mensagem[1]

    resposta = openai.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages = [
            {'role':'user','content':mensagem}
        ]
    )

    await ctx.send(resposta.choices[0].message.content)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

bot.run(token)