import discord
from discord.ext import commands
from time import sleep
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import openai
import os
from dotenv import load_dotenv

load_dotenv()

chave_api = os.environ.get("API_GPT")
openai.api_key = chave_api

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument('--enable-chrome-browser-cloud-management')
options.add_argument('--headless=new')

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

async def comandos(interaction):
    await interaction.response.send_message("Comandos: !proibidoPh \n !proibidoPhImg \n !limpar \n !raid_canais \n !desraid_canais \n !chatgpt")

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
        await ctx.channel.purge(limit=quantidade + 1)
        await ctx.send(f'{quantidade} mensagens foram apagadas por {ctx.author.mention}.', delete_after=5)
    else:
        await ctx.send('Você não tem permissão para gerenciar mensagens.')

@bot.command('criarCanal')
async def criarCanais(ctx, nome: str):
    guild = ctx.guild  # Obtém o servidor (guild) do contexto
    await guild.create_text_channel(nome)  # Cria um canal de texto com o nome especificado

# Comando para mudar nome de canais
@bot.command('mudarNomeCanal')
async def mudarNomeCanais(ctx, alvo: discord.TextChannel, novo_nome: str):
    await alvo.edit(name=novo_nome)

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

@bot.command(name='proibidoPh')
async def proibidoPh(ctx):

    driver = webdriver.Chrome(options=options) 
    driver.get('https://pt.pornhub.com/')

    btn1 = driver.find_element(By.XPATH,'//*[@id="modalWrapMTubes"]/div/div/button')
    WebDriverWait(driver,20).until(EC.element_to_be_clickable(btn1)).click()

    thumbsIMG = driver.find_elements(By.CLASS_NAME,'thumb')

    thumbImg_list = []

    for thumb in thumbsIMG:
        thumbImg_list.append(thumb.get_attribute('src'))
        if(len(thumbImg_list) >= 30):
            break

    [await ctx.send(nome) for nome in thumbImg_list]

    driver.close()
    await ctx.send('Finalizado!')

@bot.command(name='proibidoPhImg')
async def proibidoPhImg(ctx):

    driver = webdriver.Chrome(options=options) 
    driver.get('https://rule34ai.art/')

    btnMore = driver.find_element(By.XPATH,'//*[@id="primary"]/div/div[2]/div/a')
    WebDriverWait(driver,20).until(EC.element_to_be_clickable(btnMore)).click()

    sleep(2)
    for i in range(5):
        sleep(2)
        driver.execute_script(f'window.scrollTo(0,{1000*i})')

    imgsR3 = driver.find_elements(By.CLASS_NAME,'wp-post-image')
    images_list = []

    for image in imgsR3:
        if(len(images_list) >= 30):
            break

        images_list.append(image.get_attribute('src'))

    [await ctx.send(nome) for nome in images_list]

    await ctx.send('Finalizado!')
    print(len(images_list))

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

bot.run(token)
