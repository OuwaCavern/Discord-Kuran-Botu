import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import requests

client = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())


ServerID = [SERVERID OF THE DISCORD SERVER YOU WANT TO USE THIS BOT IN HERE]

author_list_api_url = f"https://api.acikkuran.com/authors"
response_authors = requests.get(author_list_api_url)
author_list_json = response_authors.json()
author_list = []
for çevirmen_entry in author_list_json.get("data", []):
    çevirmenler = çevirmen_entry.get("name", "")
    author_list.append(çevirmenler)

@client.event
async def on_ready():
    print(f'{client.user.name} ({client.user.id}) çalışmaya başladı!')


@client.slash_command(
    name="sure",
    description="Sureyi mesaj olarak atar.",
    guild_ids=ServerID
)

async def sure(interaction: Interaction, 
               çevirmen: str = SlashOption(description="Tercih ettiğiniz çevirmeni seçin.", choices=author_list), 
               sure: int = SlashOption(description="Sure numarasını giriniz.", required=False), 
               ayet: int = SlashOption(description="Ayet numarasını giriniz.", required=False)):
    if sure is not None:
        sure_api_url = f'https://api.acikkuran.com/surah/{sure}'
    if ayet is not None:
        ayet_api_url = f"https://api.acikkuran.com/surah/{sure}/verse/{ayet}"
    if çevirmen is not None:
        çeviri_api_url = f"https://api.acikkuran.com/surah/{sure}/verse/{ayet}/translations"
    else:
        await interaction.send("Lütfen bütün alanları doldurunuz.")
        return

    response_sure = requests.get(sure_api_url)
    response_ayet = requests.get(ayet_api_url)
    response_çeviri = requests.get(çeviri_api_url)
    try:
        sure_data = response_sure.json()
        sure = sure_data["data"]["id"]
        surah_text = sure_data["data"]["name"]
        ayet_data = response_ayet.json()
        ayet = ayet_data["data"]["verse_number"]
        ayet_text = ayet_data["data"]["translation"]["text"]
        çeviri_data = response_çeviri.json()
        for çeviri_entry in çeviri_data.get("data", []):
            çevirmen1 = çeviri_entry.get("author", {}).get("name", "")
            if çevirmen1 == çevirmen:
                çeviri = çeviri_entry.get("text", "")
                break
            else:
                çeviri = "Lütfen tam ismini giriniz."
        em = nextcord.Embed(url=f"https://acikkuran.com/{sure}/{ayet}",color=0x206694, title=f"{surah_text} {ayet}",
                            description=f"{çevirmen}\n\n{çeviri}")
        await interaction.send(embed=em)
    except Exception as e:
        await interaction.send(f'Error fetching data: {e}')

client.run(
    "CHATBOT TOKEN HERE")
