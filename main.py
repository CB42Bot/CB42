import discord
from discord import Option
from discord.ext import commands
from discord.ext.commands import *
from discord.ui import *
import aiohttp
import random
import pymongo
import certifi
from pymongo import MongoClient
from defs import *


ca = certifi.where()
intents = discord.Intents().all()
token_ = "MTAwNDcyNzI3NDAzMTAzODU3NA.GAtfaZ.XgGAUv--cb8pvokVoBIROysFAmdroL7TK_7IpU"
mango_url = "mongodb+srv://codemilo:amogus@cb42.tp0m3.mongodb.net/test"
cluster = MongoClient(mango_url, tlsCAFile=ca)
db = cluster["cb42"]
coll = db["prefix"]
collection = db["level"]


def prefix(client, message):
    prefix = coll.find_one({"_id": message.guild.id})["prefix"]
    return prefix


client = commands.Bot(command_prefix=prefix,
                      case_insensitive=True, help_command=None, intents=intents)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="cb!help"))
    print(f"{client.user.name} says, Hello world")


@client.event
async def on_guild_join(guild):
    coll.insert_one({"_id": guild.id, "prefix": "cb!"})


@client.event
async def on_guild_remove(guild):
    coll.delete_one({"_id": guild.id})


@client.command(aliases=['prefix'])
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def setprefix(ctx, prefix=None):
    if prefix is None:
        await ctx.reply("Please enter a prefix!", delete_after=5)
    else:
        coll.update_one({"_id": ctx.guild.id}, {
                        "$set": {"prefix": prefix}}, upsert=True)
        await ctx.reply("Prefix has been changed to: {}".format(prefix))


class DropDownMenu(discord.ui.View):
    @discord.ui.select(placeholder="Select a value", min_values=1, max_values=1, options=[
        discord.SelectOption(label="Moderation",
                             description="Moderation commands", emoji="🚩"),
        discord.SelectOption(
            label="Fun", description="Fun commands", emoji="🚀"),
        discord.SelectOption(
            label="Information", description="Information commands commands", emoji="ℹ")
    ])
    async def callback(self, select, interaction: discord.Interaction):
        if select.values[0] == "Moderation":
            view = View()
            modembed = discord.Embed(
                title="Moderation commands",
                description="`clear`, `kick`, `ban`, `unban`, `membercount`, `setprefix`, `addrole`, `delrole`",
            )

            await interaction.response.send_message(embed=modembed, view=view, ephemeral=True)

        if select.values[0] == "Fun":
            view = View()
            funembed = discord.Embed(
                title="Fun commands",
                description="`cat`, `dog`, `meme`, `showerthought`, `dice`",
            )

            await interaction.response.send_message(embed=funembed, view=view, ephemeral=True)

        if select.values[0] == "Information":
            view = View()
            inembed = discord.Embed(
                title="Information commands",
                description="`invite`, `ping`",
            )

            await interaction.response.send_message(embed=inembed, view=view, ephemeral=True)


@client.command(aliases=['commands'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx):
    helpem = discord.Embed(
        title="CB42 helpnel",
        url="https://cb42bot.tk",
        description="CB42 is an all in one bot you ever need.."
    )
    dropdowns = DropDownMenu()

    await ctx.reply(embed=helpem, view=dropdowns)


@client.command(aliases=['p', 'latency'])
@commands.cooldown(1, 15, commands.BucketType.user)
async def ping(ctx):
    l = round(client.latency * 1000, 1)
    await ctx.reply(f"The bots ping is: `{l}`")


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def fact(ctx):
    await ctx.send(get_fact())


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def topic(ctx):

    await ctx.send(get_topic())


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def showerthought(ctx):
    shower = get_shower()
    thought = shower[0]
    author = shower[1]
    embed = discord.Embed(title=f"{thought}\n  {author}")
    await ctx.send(embed=embed)


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def meme(ctx):
    embed = discord.Embed(title="Meme")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/memes/top.json?sort=top&t=week&limit=100') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children']
                            [random.randint(0, 25)]['data']['url'])

            await ctx.reply(embed=embed)

@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: Option(int, required=True)):
    t = ctx.channel
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.reply(f"**Set the slowmode for <#{t}> as** `{seconds}` **seconds** ✅", delete_after=5)

@client.command(aliases=['members', 'guildcount'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def membercount(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Membercount of this server",
                          description=f"**This server has** `{guild.member_count}` **members**")

    await ctx.reply(embed=embed)


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
    embed = discord.Embed(title="Dog!")
    embed.set_image(url=dogjson['link'])

    await ctx.reply(embed=embed)


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/cat')
        dogjson = await request.json()
    embed = discord.Embed(title="Cat!")
    embed.set_image(url=dogjson['link'])

    await ctx.reply(embed=embed)


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def dice(ctx):
    num = [
        '1',
        '2',
        '3',
        '4',
        '5',
        '6']
    await ctx.reply(f"Your random number is: {random.choice(num)}")


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason=None):
    if member == None:
        await ctx.reply("Mention the member to be kicked!", delete_after=3)
    if reason == None:
        reason = "None"
    await member.kick(reason=reason)
    await ctx.reply(f"Successfully kicked {member.mention}")


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def invite(ctx):
    invitebt = Button(
        label="Invite CB42",
        url="https://discord.com/api/oauth2/authorize?client_id=1004727274031038574&permissions=8&redirect_uri=https%3A%2F%2Fcb42bot.tk&response_type=code&scope=bot%20connections%20applications.commands"
    )
    view = View()
    view.add_item(invitebt)

    embed = discord.Embed(title="Invite CB42")

    await ctx.reply(embed=embed, view=view)


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if member == None:
        await ctx.reply("Mention the member to be banned!", delete_after=3)
    if reason == None:
        reason = "None"
    await member.ban(reason=reason)
    await ctx.reply(f"Successfully banned {member.mention}")


@client.command()
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def unban(ctx, id: int):
    user = await client.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.reply(f'Unbanned {user.mention}')


@client.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, user: discord.Member, *, role: discord.Role):
    await user.add_roles(role)
    await ctx.reply(f"Added {role} to {user.mention}")


@client.command()
@commands.has_permissions(manage_roles=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def removerole(ctx, user: discord.Member, *, role: discord.Role):
    await user.remove_roles(role)
    await ctx.reply(f"Removed {role} from {user.mention}")


@client.command(aliases=['purge'])
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def clear(ctx, amount=1):
    c = ctx.channel.id
    amount = amount+1
    r = amount-1
    if amount > 101:
        await ctx.reply('**Not able to delete so many messages! Please try a number below 100.**', delete_after=5)
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Cleared `{r}` messages in <#{c}>', delete_after=3)


@client.command(aliases=['close', 'shutup'])
async def shutdown(ctx):
    user = ctx.message.author
    if user.id == 943492607688970262 or user.id == 895581887593078804:
        await ctx.reply("Successful shutdown")
        print("Shutdown successful")
        await client.close()
    else:
        await ctx.reply("Not allowed")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("This command doesn't exist!", delete_after=3)
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.reply(error, delete_after=3)
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("You dont have the permission to use this command!", delete_after=3)
    if isinstance("You are missing a required argument", commands.MissingRequiredArgument):
        await ctx.reply(error, delete_after=3)

# SLASH


@client.slash_command(aliases=['prefix'])
@commands.has_permissions(manage_guild=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def setprefix(ctx, prefix=None):
    if prefix is None:
        await ctx.respond("Please enter a prefix!", delete_after=5)
    else:
        coll.update_one({"_id": ctx.guild.id}, {
                        "$set": {"prefix": prefix}}, upsert=True)
        await ctx.respond("Prefix has been changed to: {}".format(prefix))


class DropDownMenuslash(discord.ui.View):
    @discord.ui.select(placeholder="Select a value", min_values=1, max_values=1, options=[
        discord.SelectOption(label="Moderation",
                             description="Moderation commands", emoji="🚩"),
        discord.SelectOption(
            label="Fun", description="Fun commands", emoji="🚀"),
        discord.SelectOption(
            label="Information", description="Information commands commands", emoji="ℹ")
    ])
    async def callback(self, select, interaction: discord.Interaction):
        if select.values[0] == "Moderation":
            view = View()
            modembed = discord.Embed(
                title="Moderation commands",
                description="`clear`, `kick`, `ban`, `unban`, `membercount`, `setprefix`, `addrole`, `delrole`",
            )

            await interaction.response.send_message(embed=modembed, view=view, ephemeral=True)

        if select.values[0] == "Fun":
            view = View()
            funembed = discord.Embed(
                title="Fun commands",
                description="`cat`, `dog`, `meme`, `showerthought`, `dice`",
            )

            await interaction.response.send_message(embed=funembed, view=view, ephemeral=True)

        if select.values[0] == "Information":
            view = View()
            inembed = discord.Embed(
                title="Information commands",
                description="`invite`, `ping`",
            )

            await interaction.response.send_message(embed=inembed, view=view, ephemeral=True)


@client.slash_command(name="help", description="Get all the commands of the bot")
@commands.cooldown(1, 5, commands.BucketType.user)
async def help(ctx):
    helpem = discord.Embed(
        title="CB42 helpnel",
        url="https://cb42bot.tk",
        description="CB42 is an all in one bot you ever need.."
    )
    dropdowns = DropDownMenuslash()

    await ctx.respond(embed=helpem, view=dropdowns)


@client.slash_command(name="ping", description="Get the bots latency")
@commands.cooldown(1, 15, commands.BucketType.user)
async def ping(ctx):
    l = round(client.latency * 1000, 1)
    await ctx.respond(f"The bots ping is: `{l}`", ephemeral=True)


@client.slash_command(name="fact", description="Get a random fact")
@commands.cooldown(1, 5, commands.BucketType.user)
async def fact(ctx):
    await ctx.respond(get_fact(), ephemeral=True)


@client.slash_command(name="topic", description="Get a random topic")
@commands.cooldown(1, 5, commands.BucketType.user)
async def topic(ctx):

    await ctx.respond(get_topic(), ephemeral=True)


@client.slash_command(name="showerthough", description="Get a random showerthought from reddit")
@commands.cooldown(1, 5, commands.BucketType.user)
async def showerthought(ctx):
    shower = get_shower()
    thought = shower[0]
    author = shower[1]
    embed = discord.Embed(title=f"{thought}\n  {author}")
    await ctx.respond(embed=embed, ephemeral=True)


@client.slash_command(name="meme", description="Get a random meme from reddit")
@commands.cooldown(1, 5, commands.BucketType.user)
async def meme(ctx):
    embed = discord.Embed(title="Meme")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/memes/top.json?sort=top&t=week&limit=100') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children']
                            [random.randint(0, 25)]['data']['url'])

            await ctx.respond(embed=embed)


@client.slash_command(name="membercount", description="Get the membercount of the specific server")
@commands.cooldown(1, 5, commands.BucketType.user)
async def membercount(ctx):
    guild = ctx.guild
    embed = discord.Embed(title="Membercount of this server",
                          description=f"**This server has** `{guild.member_count}` **members**")

    await ctx.respond(embed=embed)


@client.slash_command(name="dog", description="Get a random dog pic")
@commands.cooldown(1, 5, commands.BucketType.user)
async def dog(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/dog')
        dogjson = await request.json()
    embed = discord.Embed(title="Dog!")
    embed.set_image(url=dogjson['link'])

    await ctx.respond(embed=embed)


@client.slash_command(name="cat", description="Get a random cat pic")
@commands.cooldown(1, 5, commands.BucketType.user)
async def cat(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/img/cat')
        dogjson = await request.json()
    embed = discord.Embed(title="Cat!")
    embed.set_image(url=dogjson['link'])

    await ctx.respond(embed=embed)


@client.slash_command(name="dice", description="Get a random number form 1 to 6")
@commands.cooldown(1, 5, commands.BucketType.user)
async def dice(ctx):
    num = [
        '1',
        '2',
        '3',
        '4',
        '5',
        '6']
    await ctx.respond(f"Your random number is: {random.choice(num)}", ephemeral=True)


@client.slash_command(name="kick", description="Kick a member")
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason=None):
    if member == None:
        await ctx.respond("Mention the member to be kicked!", ephemeral=True)
    if reason == None:
        reason = "None"
    await member.kick(reason=reason)
    await ctx.respond(f"Successfully kicked {member.mention}")


@client.slash_command(name="invite", description="Invite CB42 to your server")
@commands.cooldown(1, 5, commands.BucketType.user)
async def invite(ctx):
    invitebt = Button(
        label="Invite CB42",
        url="https://discord.com/api/oauth2/authorize?client_id=1004727274031038574&permissions=8&redirect_uri=https%3A%2F%2Fcb42bot.tk&response_type=code&scope=bot%20connections%20applications.commands"
    )
    view = View()
    view.add_item(invitebt)

    embed = discord.Embed(title="Invite CB42")

    await ctx.respond(embed=embed, view=view, ephemeral=True)


@client.slash_command(name="ban", description="Ban a member")
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    if member == None:
        await ctx.respond("Mention the member to be banned!", ephemeral=True)
    if reason == None:
        reason = "None"
    await member.ban(reason=reason)
    await ctx.respond(f"Successfully banned {member.mention}")


@client.slash_command(name="unban", description="Unban a member using their USER-ID")
@commands.has_permissions(ban_members=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def unban(ctx, id: Option(required=True)):
    user = await client.fetch_user(id)
    await ctx.guild.unban(user)
    await ctx.respond(f'Unbanned {user.mention}')


@client.slash_command(name="addrole", description="Add a role to a discord member")
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, user: discord.Member, *, role: discord.Role):
    await user.add_roles(role)
    await ctx.respond(f"Added {role} to {user.mention}")


@client.slash_command(name="removerole", description="Remove a role from a discord member")
@commands.has_permissions(manage_roles=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def removerole(ctx, user: discord.Member, *, role: discord.Role):
    await user.remove_roles(role)
    await ctx.respond(f"Removed {role} from {user.mention}")


@client.slash_command(name="clear", description="Clear messages in a channel")
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 5, commands.BucketType.user)
async def clear(ctx, amount:Option(int, required=True)):
    c = ctx.channel.id
    amount = amount+1
    r = amount-1
    if amount > 101:
        await ctx.respond('**Not able to delete so many messages! Please try a number below 100.**', ephemeral=True)
    else:
        await ctx.channel.purge(limit=amount)
        await ctx.respond(f'Cleared `{r}` messages in <#{c}>', delete_after=3)

@client.slash_command(name="slowmode", description="Change/set the slowmode of a channel")
@commands.cooldown(1, 5, commands.BucketType.user)
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: Option(int, required=True)):
    t = ctx.channel
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.respond(f"**Set the slowmode for <#{t}> as** `{seconds}` **seconds** ✅", delete_after=5)

# SLASH


@client.event
async def on_message(message):
    if message.author.id == client.user.id:
        return

    if message.author.bot:
        return

    author_id = message.author.id
    guild_id = message.guild.id

    author = message.author

    user_id = {"_id": author_id}

    if(collection.count_documents({}) == 0):
        user_info = {"_id": author_id,
                     "GuildID": guild_id, "Level": 1, "XP": 0}
        collection.insert_one(user_info)

    if(collection.count_documents(user_id) == 0):
        user_info = {"_id": author_id,
                     "GuildID": guild_id, "Level": 1, "XP": 0}
        collection.insert_one(user_info)

    exp = collection.find(user_id)
    for xp in exp:
        cur_xp = xp["XP"]

        new_xp = cur_xp + 1

    collection.update_one({"_id": author_id}, {
                          "$set": {"XP": new_xp}}, upsert=True)

    lvl = collection.find(user_id)
    for levl in lvl:
        lvl_start = levl["Level"]

        new_level = lvl_start + 1

    if cur_xp >= round(5 * (lvl_start ** 4 / 5)):
        collection.update_one({"_id": author_id}, {
                              "$set": {"Level": new_level}}, upsert=True)
        await message.channel.send(f"{message.author.mention} is now level **{new_level}**!")
    answer = check_message(message)
    if answer[0] == "del":
        await message.delete()
        await message.channel.send(answer[1], delete_after=3)

    message.content = message.content.lower()
    await client.process_commands(message)

try:
    client.run(token_)
except:
    print("Make sure the token is correct!")
