import discord
import deepl
import os

intents = discord.Intents.all()
bot = discord.Client(intents=intents)

DEEPL_API_KEY = "fb04155f-fc1b-49d3-ad63-992b24ba91a6:fx"

LANGUAGES = {
    "🇫🇷": "FR",
    "🇬🇧": "EN-GB",
    "🇪🇸": "ES",
    "🇩🇪": "DE",
    "🇮🇹": "IT",
    "🇵🇹": "PT-PT",
    "🇨🇳": "ZH",
    "🇯🇵": "JA",
    "🇸🇦": "AR",
    "🇷🇺": "RU",
    "🇰🇷": "KO",
}

translator = deepl.Translator(DEEPL_API_KEY)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté : {bot.user}")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    emoji = str(reaction.emoji)
    if emoji not in LANGUAGES:
        return

    target_lang = LANGUAGES[emoji]
    message_text = reaction.message.content

    if not message_text:
        return

    try:
        result = translator.translate_text(message_text, target_lang=target_lang)
        translated = result.text
    except Exception as e:
        translated = f"❌ Erreur : {str(e)}"

    await reaction.message.reply(
        f"{emoji} **Traduction en `{target_lang}` :**\n{translated}",
        mention_author=False
    )

TOKEN = "MTQ4Njc2MzQzNDM1NDY3MTY4Ng.GUq0-_.DpD2Q7GrMDTrGd7RaBtbgedMN6_ipuGxd-uj-c"
bot.run(TOKEN)