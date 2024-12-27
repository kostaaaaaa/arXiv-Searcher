discord_token = "Your Own Discord Token"

import discord
from discord.ext import commands
import arxiv

# Initialize the bot
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix=">", intents=intents)

# Function to search arXiv
def search_arxiv(query, search_type, result_limit):
    if search_type == "topic":
        search_query = arxiv.Search(query=query, max_results=result_limit)
    elif search_type == "author":
        search_query = arxiv.Search(query=f"au:{query}", max_results=result_limit)
    elif search_type == "subject":
        search_query = arxiv.Search(query=f"cat:{query}", max_results=result_limit)
    else:
        return []

    return list(search_query.results())

# Bot event: Ready
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# Bot command: Search
@bot.command(name="Athena.bot")
async def athena_bot(ctx, *, args):
    args = args.split("--")
    arguments = {arg.split(" ", 1)[0]: arg.split(" ", 1)[1] for arg in args if " " in arg}

    topic = arguments.get("topic", None)
    search_type = arguments.get("type", "topic")  # Defaults to 'topic'
    action = arguments.get("action", None)
    limit = int(arguments.get("limit", 5))

    if not topic:
        await ctx.send("Please specify a topic using `--topic`.")
        return

    results = search_arxiv(topic, search_type, 100)

    if not results:
        await ctx.send("No results found.")
        return

    # Pagination
    page = 0
    per_page = limit
    last_message = None  # Track the last sent message

    def format_result(result, index):
        return (f"**[{index + 1}] {result.title}**\n"
                f"Author(s): {', '.join(author.name for author in result.authors)}\n"
                f"Published: {result.published.year}\n"
                f"Abstract: {result.summary[:200]}...\n"
                f"PDF: {result.pdf_url}\n")

    async def display_page(page):
        nonlocal last_message
        start = page * per_page
        end = start + per_page
        message = "\n\n".join([format_result(results[i], i) for i in range(start, min(end, len(results)))])
        if last_message:
            await last_message.delete()  # Delete the last page message
        last_message = await ctx.send(f"**Page {page + 1}/{(len(results) - 1) // per_page + 1}**\n{message}")

    await display_page(page)

    # Navigation and selection
    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    while True:
        try:
            msg = await bot.wait_for("message", check=check, timeout=60)
            if msg.content == "+":
                if (page + 1) * per_page < len(results):
                    page += 1
                    await display_page(page)
                else:
                    await ctx.send("You're at the last page.")
            elif msg.content == "-":
                if page > 0:
                    page -= 1
                    await display_page(page)
                else:
                    await ctx.send("You're at the first page.")
            elif msg.content == "0":
                await ctx.send("Exiting...")
                break
            elif msg.content.isdigit():
                choice = int(msg.content)
                if 1 <= choice <= len(results):
                    paper = results[choice - 1]
                    if action == "download":
                        pdf_content = paper.download_pdf()
                        filename = f"{paper.title.replace('/', '-').replace(':', '-')}.pdf"
                        await ctx.send(f"Downloading paper: **{paper.title}**...")
                        await ctx.send(file=discord.File(pdf_content, filename=filename))
                        await ctx.send("Paper uploaded to #papers.")
                    elif action == "open":
                        await ctx.send(f"Opening PDF: {paper.pdf_url}")
                    break
                else:
                    await ctx.send("Invalid selection. Try again.")
            else:
                await ctx.send("Invalid command. Use +, -, or a paper number.")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")
            break

# Run the bot
bot.run(discord_token)
