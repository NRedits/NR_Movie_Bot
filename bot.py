import pandas as pd
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "YOUR TELEGRAM API"
MOVIES_DF = pd.read_csv("movie.csv")  # Load dataset once

# 🏁 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome to MovieBot!\nUse /suggest genre, /random, or /search movie name.")

# 🎯 /suggest genre
async def suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❓ Usage: /suggest [genre] (e.g., /suggest comedy)")
        return

    genre = context.args[0].capitalize()
    filtered = MOVIES_DF[MOVIES_DF['genre'].str.lower() == genre.lower()]

    if filtered.empty:
        await update.message.reply_text(f"🚫 No movies found in genre: {genre}")
    else:
        movie = filtered.sample().iloc[0]
        await update.message.reply_text(
            f"🎬 *{movie['title']}* ({movie['year']})\n"
            f"🎭 Genre: {movie['genre']}\n"
            f"📝 {movie['description']}",
            parse_mode="Markdown"
        )

# 🎲 /random
async def random_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    movie = MOVIES_DF.sample().iloc[0]
    await update.message.reply_text(
        f"🎲 Random Movie:\n\n*{movie['title']}* ({movie['year']})\n"
        f"🎭 Genre: {movie['genre']}\n"
        f"📝 {movie['description']}",
        parse_mode="Markdown"
    )

# 🔍 /search movie title
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❓ Usage: /search [movie name]")
        return

    query = " ".join(context.args).lower()
    results = MOVIES_DF[MOVIES_DF['title'].str.lower().str.contains(query)]

    if results.empty:
        await update.message.reply_text("🚫 No matching movies found.")
    else:
        response = ""
        for _, row in results.iterrows():
            response += f"🎬 *{row['title']}* ({row['year']}) - {row['genre']}\n📝 {row['description']}\n\n"
        await update.message.reply_text(response.strip(), parse_mode="Markdown")

# 🚀 Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("suggest", suggest))
    app.add_handler(CommandHandler("random", random_movie))
    app.add_handler(CommandHandler("search", search))
    app.run_polling()

if __name__ == "__main__":
    main()
