import discord
import deepl
import os

intents = discord.Intents.all()
bot = discord.Client(intents=intents)

DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY")

LANGUAGES = {
    "🇫🇷": "FR",
    "🇬🇧": "EN-GB",
    "🇺🇸": "EN-US",
    "🇪🇸": "ES",
    "🇩🇪": "DE",
    "🇮🇹": "IT",
    "🇵🇹": "PT-PT",
    "🇧🇷": "PT-BR",
    "🇨🇳": "ZH",
    "🇯🇵": "JA",
    "🇸🇦": "AR",
    "🇷🇺": "RU",
    "🇰🇷": "KO",
    "🇳🇱": "NL",
    "🇵🇱": "PL",
    "🇸🇪": "SV",
    "🇩🇰": "DA",
    "🇫🇮": "FI",
    "🇨🇿": "CS",
    "🇷🇴": "RO",
    "🇭🇺": "HU",
    "🇺🇦": "UK",
    "🇧🇬": "BG",
    "🇸🇰": "SK",
    "🇸🇮": "SL",
    "🇪🇪": "ET",
    "🇱🇻": "LV",
    "🇱🇹": "LT",
    "🇮🇩": "ID",
    "🇹🇷": "TR",
}

translator = deepl.Translator(DEEPL_API_KEY)

# Dictionnaire pour mémoriser les traductions
# {message_original_id: [id_traduction1, id_traduction2, ...]}
translations = {}

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

    reply = await reaction.message.reply(
        f"{emoji} **Traduction en `{target_lang}` :**\n{translated}",
        mention_author=False
    )

    # Mémorise la traduction
    original_id = reaction.message.id
    if original_id not in translations:
        translations[original_id] = []
    translations[original_id].append(reply.id)

@bot.event
async def on_message_delete(message):
    if message.id in translations:
        for translation_id in translations[message.id]:
            try:
                translation_msg = await message.channel.fetch_message(translation_id)
                await translation_msg.delete()
            except:
                pass
        del translations[message.id]

TOKEN = os.environ.get("DISCORD_TOKEN")
bot.run(TOKEN)