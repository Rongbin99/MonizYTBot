import discord, json, os, re, urllib, requests, random, time
from stuff import bot_token, now, appid
from discord.ext import commands, tasks
from discord.ext.commands import has_guild_permissions
from discord import Option, OptionChoice
from urllib.request import Request, urlopen

intents = discord.Intents.all()
game = discord.Activity(name='Matthew Moniz on YouTube', type=discord.ActivityType.watching)
prefix = 'm.'

client = commands.Bot(command_prefix = commands.when_mentioned_or(prefix), intents=intents, status=discord.Status.idle, activity=game, help_command=None)

@client.event
async def on_ready():
    videocheck.start()
    print(f'The MattyMo Bot is ready for operation.')

@client.command(aliases=['test'])
async def ping(ctx):
    await ctx.send(f'Bamn! {round(client.latency * 1000, ndigits=2)} ms.')
@client.slash_command(description = "Test the latency of the bot.")
async def ping(ctx):
    await ctx.respond(f'Bamn! {round(client.latency * 1000, ndigits=2)} ms.')

@client.command(aliases=['ytstop'])
@has_guild_permissions(administrator=True)
async def stop_notifying(ctx):
    videocheck.stop()
    print(f'Stopped Notifying - {now}')
    await ctx.send(f'Stopped Notifying')
@client.command(aliases=['ytrestart'])
@has_guild_permissions(administrator=True)
async def restart_notifying(ctx):
    videocheck.stop()
    videocheck.start()
    print(f'Restarted Notifying - {now}')
    await ctx.send(f'Restarted Notifying')
@restart_notifying.error
async def restart_notifying_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"It's currently stopped, please use 'm.ytstart'")
@client.command(aliases=['ytstart'])
@has_guild_permissions(administrator=True)
async def start_notifying(ctx):
    videocheck.start()
    print(f'Started Notifying - {now}')
    await ctx.send(f'Started Notifying')
@start_notifying.error
async def start_notifying_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"It's already running!")

@client.slash_command(description = "Stops YT Notifying.")
@has_guild_permissions(administrator=True)
async def stop_notifying(ctx):
    videocheck.stop()
    print(f'Stopped Notifying - {now}')
    await ctx.respond(f'Stopped Notifying')
@stop_notifying.error
async def stop_notifying_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("You don't have the required power.")
@client.slash_command(description = "Restarts YT Notifying.")
@has_guild_permissions(administrator=True)
async def restart_notifying(ctx):
    videocheck.stop()
    videocheck.start()
    print(f'Restarted Notifying - {now}')
    await ctx.respond(f'Restarted Notifying')
@restart_notifying.error
async def restart_notifying_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("You don't have the required power.")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.respond("It's currently stopped, please use 'm.ytstart'")
@client.slash_command(description = "Starts YT Notifying.")
@has_guild_permissions(administrator=True)
async def start_notifying(ctx):
    videocheck.start()
    print(f'Started Notifying - {now}')
    await ctx.respond(f'Started Notifying')
@start_notifying.error
async def start_notifying_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("You don't have the required power.")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.respond("It's already running!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the required power.")
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please include all arguments (variables).")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command entered.")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send("Error 403: Forbidden")

#------------yt notif----------------
"""
@tasks.loop(seconds=60)
async def videocheck():
    yt_notif_channel = client.get_channel(468857960295170059)
    with open('data.json', 'r') as f:
        data=json.load(f)
        for youtube_channel in data:
            print(f"Now checking for {data[youtube_channel]['channel_name']} - {now}")
            channel  =  f'https://www.youtube.com/channel/{youtube_channel}'
            html1 = requests.get(channel+"/videos").text
            html2  = requests.get(channel+"/shorts").text
            html3 = requests.get(channel+"/streams").text

            try:
                latest_video_url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html1).group()
            except:
                continue

            try:
                latest_short_url = "https://www.youtube.com/shorts/" + re.search('(?<="videoId":").*?(?=")', html2).group()
            except:
                continue

            try:
                latest_live_url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html3).group()
            except:
                continue

            if not str(data[youtube_channel]["latest_video_url"]) == latest_video_url:
                data[str(youtube_channel)]['latest_video_url'] = latest_video_url
                with open("data.json", "w") as f:
                    json.dump(data, f)
                await yt_notif_channel.send(f"Yo <@&591756011245797389>, {data[str(youtube_channel)]['channel_name']} just uploaded a new video! Check it out: {latest_video_url}")
                await cooldown()

            if not str(data[youtube_channel]["latest_short_url"]) == latest_short_url:
                data[str(youtube_channel)]['latest_short_url'] = latest_short_url
                with open("data.json", "w") as f:
                    json.dump(data, f)
                await yt_notif_channel.send(f"Yo <@&591756011245797389>, {data[str(youtube_channel)]['channel_name']} just uploaded a new YouTube Short! Check it out: {latest_short_url}")
                await cooldown()

            if not str(data[youtube_channel]["latest_live_url"]) == latest_live_url:
                data[str(youtube_channel)]['latest_live_url'] = latest_live_url
                with open("data.json", "w") as f:
                    json.dump(data, f)
                await yt_notif_channel.send(f"Yo <@&863200658118934538>, {data[str(youtube_channel)]['channel_name']} just went live! Join the livestream: {latest_live_url}")
                await cooldown()

            print(f"Done {data[youtube_channel]['channel_name']} - {now}")

@client.event
async def cooldown():
    videocheck.stop()
    time.sleep(1800)
    videocheck.start()
"""
#-----------moderation---------------

@client.command(aliases=['boot'])
@has_guild_permissions(kick_members=True)
async def kick(ctx, member : commands.MemberConverter, *, why='No reason given.'):
    await member.kick(reason=why)
    mod_log_channel = client.get_channel(475330219327094784)
    await mod_log_channel.send(f'**{member}** has been kicked. Reason: *{why}*')
    await ctx.send(f'**{member}** has been kicked. Reason: *{why}*')
@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f'Sorry, they are too powerful for me.')
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(f"Does that person exist?")

@client.command(aliases=['clear', 'delete', 'del'])
@has_guild_permissions(manage_messages=True)
async def purge(ctx, *, amount):
    await ctx.send(f'`Deleting...`')
    await ctx.channel.purge(limit=int(amount)+2)

@client.command()
@has_guild_permissions(ban_members=True)
async def ban(ctx, member : commands.MemberConverter, *, why='No reason given.'):
    await member.ban(reason=why)
    mod_log_channel = client.get_channel(475330219327094784)
    await mod_log_channel.send(f'**{member}** has been banned. Reason: *{why}*')
    await ctx.send(f'**{member}** has been banned. Reason: *{why}*')
@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f'Sorry, they are too powerful for me.')
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(f"Does that person exist?")

@client.command()
@has_guild_permissions(ban_members=True)
async def unban(ctx, *, member : discord.User):
    await ctx.guild.unban(member)
    mod_log_channel = client.get_channel(475330219327094784)
    await mod_log_channel.send(f'**{member}** has been unbanned.')
    await ctx.send(f'**{member}** has been unbanned.')
@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(f"Sorry, that user couldn't be found or they've already been unbanned.")
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f"Sorry, that user couldn't be found or they've already been unbanned.")

#-------------ai--------------------

@client.command(help='Perform a unit conversion.')
async def ai(ctx, *, querystring):
    input = querystring.replace(" ", "%20")
    response = urlopen(Request(f"http://api.wolframalpha.com/v2/query?appid={appid}&input={input}&includepodid=Result&format=plaintext&output=json",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
    },)).read()
    data = json.loads(response)
    await ctx.send(data['queryresult']['pods'][0]['subpods'][0]['plaintext'])
@ai.error
async def ai_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f'Query unsuccessful or has no result.')
@client.slash_command(description = "Perform a unit conversion.")
async def ai(interaction: discord.Interaction, querystring: Option(str, "Insert what you wish to search", required=True)):
    input = querystring.replace(" ", "%20")
    response = urlopen(Request(f"http://api.wolframalpha.com/v2/query?appid={appid}&input={input}&includepodid=Result&format=plaintext&output=json",
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
    },)).read()
    data = json.loads(response)
    await interaction.respond(data['queryresult']['pods'][0]['subpods'][0]['plaintext'])
@ai.error
async def ai_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.send(f'Query unsuccessful or has no result.')
    
#--------------misc---------------

@client.command()
async def rps(ctx, input):
    if input == "rock" or "paper" or "scissors":
        oppo = random.choice(['rock', 'paper', 'scissors'])
        if oppo == input:
            await ctx.send(f"I picked {oppo}, you picked {input}. It's a tie!")
        elif oppo == 'rock' and input == 'paper':
            await ctx.send(f"I picked {oppo}, you picked {input}. You win!")
        elif oppo == 'rock' and input == 'scissors':
            await ctx.send(f"I picked {oppo}, you picked {input}. I win!")
        elif oppo == 'paper' and input == 'rock':
            await ctx.send(f"I picked {oppo}, you picked {input}. I win!")
        elif oppo == 'paper' and input == 'scissors':
            await ctx.send(f"I picked {oppo}, you picked {input}. You win!")
        elif oppo == 'scissors' and input == 'rock':
            await ctx.send(f"I picked {oppo}, you picked {input}. You win!")
        elif oppo == 'scissors' and input == 'paper':
            await ctx.send(f"I picked {oppo}, you picked {input}. I win!")
        else:
            await ctx.send(f'Whoops, please pick "rock" "paper" or "scissors"')
@rps.error
async def rps_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'Whoops, please pick "rock" "paper" or "scissors"')
@client.slash_command(description = "Play Rock, Paper, Scissors.")
async def rps(interaction: discord.Interaction, input: Option(str, "Pick Rock, Paper, or Scissors", choices = [
    OptionChoice(name='Rock', value='rock'),
    OptionChoice(name='Paper', value='paper'),
    OptionChoice(name='Scissors', value='scissors'),
    ], required = True)):
    oppo = random.choice(['rock', 'paper', 'scissors'])
    if oppo == input:
        await interaction.respond(f"I picked {oppo}, you picked {input}. It's a tie!")
    elif oppo == 'rock' and input == 'paper':
        await interaction.respond(f"I picked {oppo}, you picked {input}. You win!")
    elif oppo == 'rock' and input == 'scissors':
        await interaction.respond(f"I picked {oppo}, you picked {input}. I win!")
    elif oppo == 'paper' and input == 'rock':
        await interaction.respond(f"I picked {oppo}, you picked {input}. I win!")
    elif oppo == 'paper' and input == 'scissors':
        await interaction.respond(f"I picked {oppo}, you picked {input}. You win!")
    elif oppo == 'scissors' and input == 'rock':
        await interaction.respond(f"I picked {oppo}, you picked {input}. You win!")
    elif oppo == 'scissors' and input == 'paper':
        await interaction.respond(f"I picked {oppo}, you picked {input}. I win!")

@client.command()
@has_guild_permissions(kick_members=True)
async def say(ctx, *, message='_ _'):
    await ctx.channel.purge(limit=1)
    await ctx.send(f'{message}')
@client.command()
@has_guild_permissions(kick_members=True)
async def esay(ctx, *, message='_ _'):
    await ctx.channel.purge(limit=1)
    await ctx.send(embed = discord.Embed(description=f'{message}', color=ctx.author.color))

#-----------help---------------------

@client.slash_command(description = 'Sends the help menu for this bot.')
async def help(ctx):
    em = discord.Embed(title='MattyMo Bot Help Menu', description=f'Use {prefix}help <command> for specific help with that command.\n_ _\n < > indicates the value is required\n[ ] indicates the value is optional', color=ctx.author.color)
    em.add_field(name='Available Commands', value=f'ping\nai\nrps\nhelp')
    await ctx.respond(embed = em)

@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title='MattyMo Bot Help Menu', description=f'Use {prefix}help <command> for specific help with that command.\n_ _\n < > indicates the value is required\n[ ] indicates the value is optional', color=ctx.author.color)
    em.add_field(name='Available Commands', value=f'ping\nai\nrps\nhelp')
    await ctx.send(embed = em)
@help.command()
async def ping(ctx):
    em = discord.Embed(title='Ping', description=f'Checks the responsiveness of the MattyMo Bot.',color=ctx.author.color)
    em.add_field(name='Usage', value=f'{prefix}ping')
    await ctx.send(embed=em)
@help.command()
async def ai(ctx):
    em = discord.Embed(title='AI Search', description=f'Search for something using the Wolframalpha AI\n_ _\n< > indicates the value is required', color=ctx.author.color)
    em.add_field(name='Usage', value=f'{prefix}ai <search input>')
    await ctx.send(embed=em)
@help.command()
async def rps(ctx):
    em = discord.Embed(title='Rock Paper Scissors', description=f'Plays rock, paper, scissors against the bot.\n_ _\n < > indicates the value is required',color=ctx.author.color)
    em.add_field(name='Usage', value=f'{prefix}rps <rock/paper/scissors>')
    await ctx.send(embed=em)

client.run(bot_token)