
from asyncio.tasks import sleep
import discord
from discord.ext import commands
from discord.utils import get


intents = discord.Intents.default()
intents.members = True

# bot and command prefix
bot = commands.Bot(command_prefix='.', intents=intents, help_command=None, case_insensitive=True)

channelId = 883796582464618608

# When the bot is ready
@bot.event
async def on_ready():
    # changes bots activity. Aka game
    await bot.change_presence(activity=discord.Game("Im happy :D"))

    # says im back in the general chat
    general_channel = bot.get_channel(channelId)
    await general_channel.send("I'm back :D")

# When a member joins
@bot.event 
async def on_member_join(member):

        # Gets the member role and gives it on member join
        role = get(member.guild.roles, id=885059561055203381)
        await member.add_roles(role)

        # Gets the general channel
        channel = bot.get_channel(channelId)   

        # Gets the bots id and stores it in a variable
        WelcomeAuthor = bot.get_user(352122359857152011)

        # Gets the server.
        server = bot.get_guild(883796581978107947)

        # creates and embed with the previous variables in it 
        embed=discord.Embed(title=f"Welcome {member.display_name}!!! Glad to have you :D", color=discord.Color.purple())
        embed.set_author(name=WelcomeAuthor.display_name, icon_url=WelcomeAuthor.avatar_url)
        embed.set_footer(text="automated message. Disapears after 60 sec.", icon_url= server.icon_url)

        # Sends the welcome embed and deletes it after 60 sec
        await channel.send(embed=embed, delete_after=60)

        # presence animation when new user is added. 
        statuses = 'Loading.', 'Loading..', 'Loading...', f'Welcome {member.display_name} :D' 
        
        # Goes through the statuses list and shows it on the bots activity. Aka game
        for x in statuses:
            await bot.change_presence(activity=discord.Game(x))
            await sleep(1)
        
        # Changes activity back to Im happy :D
        await sleep(5)
        await bot.change_presence(activity=discord.Game("Im happy :D"))

# Message Delete
@bot.event
async def on_message_delete(ctx):
    # if user deletes a message it will say "user#1234 Has deleted a message"
    if ctx.author != bot.user:
        if '$' in ctx.content:
            return
        else:
            return await ctx.channel.send(f'{ctx.author} Has deleted a message')

# User info
@bot.command(pass_context=True)
# If user has any of the following roles they can use this command.
@commands.has_any_role("Admin", "User Checker", "Owner")
async def userinfo(ctx, *, user: discord.Member = None):
        
        # Gets users role with most rights. example "Owner" is the highest and "Admin" is the second highest 
        role = user.top_role.name

        # Checks if the user does not have a role and sets higest role to N/A if they dont 
        if role == "@everyone":
            role = "N/A"
        
        # Checks if user is in a voice channel
        voice_state = None if not user.voice else user.voice.channel

        # If there is no user inputed in command it just takes the context author
        if user is None:
            user = ctx.author
        
        # Creates and embed and sets it up with Name, Activity/Game, and time of account creation.
        embed = discord.Embed(
            title=f"{user.name}'s Stats and Information.",
        color=user.color)
        embed.set_thumbnail(url=user.avatar_url_as())
        embed.add_field(name="__**General information:**__", value=f"**Discord Name:** {user}\n"
                                                                   f"**Game** {user.activity}\n"                                                                                              
                                                                   f"**Account created:** {user.created_at.__format__('%A, %d. %B %Y at %H:%M:%S')}\n", inline= False)

        # Makes a field in the same embed with the server stats. Join date, if user is in voice channel, and highest role. Aka Owner, Admin
        embed.add_field(name='__**Server Stats:**__', value=user.joined_at.__format__("**join date:** %A, %d. %B %Y at %H:%M:%S\n"
                                                                             f"**In Voice:** {voice_state}\n"
                                                                             f"**Highest Role:** {role}"), inline= False)                             
                  
        # Sets the embed footer, aka bottom text. author has checked users stats. users ID: 123456789123456789. Message wil be removed after 30 sec                                           
        embed.set_footer(icon_url=ctx.author.avatar_url, text= f"{ctx.author.display_name} Has checked {user.display_name}'s stats.\n" f"{user.display_name}'s ID: {user.id}\nMessage removed after 30 sec"     )

        # Sends the embed and deletes it after 30 secs
        return await ctx.send(embed=embed, delete_after=30)

# Help command
@bot.command()
async def help(ctx):
    # Gets the bot
    WelcomeAuthor = bot.get_user(352122359857152011)

    # Creats and embed with the bots commands
    embed = discord.Embed(
            title=f"{WelcomeAuthor.display_name}'s Commands",
    color=discord.Color.red())

    # Sets the footer Aka bottom text
    embed.set_footer(text=f"Help message. Removed after 30 secs")

    # Sets tumbnail to the bots profile picture
    embed.set_thumbnail(url=WelcomeAuthor.avatar_url_as())

    # Adds a field with commands
    embed.add_field(name="__**General commands:**__", value=f"**.help** is this command.\n"
                                                            f"**.hello** makes the bot say hello.\n"
                                                            f"**.UserInfo** is a command to check a users info. Admin/User Checker only.\n"
                                                            f"**.kick** Kicks a member. Kick perms needed.\n"
                                                            f"**.ban** Bans a member. Ban perms needed.\n", inline= False)

    # sends the embed and deletes it after 30 secs
    return await ctx.send(embed=embed, delete_after=30)

# kick command. smider folk ud af serveren 
@bot.command()
# Only activates if you have the permission to kick members
@commands.has_permissions(kick_members= True)
async def kick(ctx, member: discord.Member, *, reason=None):

        if reason is None:
            reason == "For being a jerk!"
        # Kicks member and states the reason to them
        await member.kick(reason=reason)

        # Sends in context chat that user has been banned and the reason
        await ctx.send(f'User {member} has kicked. for {reason}')

#Bans a user with a reason
@bot.command()
# Only activates if you have ban premissions. 
@commands.has_permissions(ban_members= True)
async def ban (ctx, member:discord.User=None, *, reason =None):
    
    # If member specified for ban is the author its send "you cannot ban yourself" and returns
    if member == None or member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself")
        return
    # If reason is None. Aka not inputed. Reason will be "For being a jerk!"
    if reason == None:
        reason = "For being a jerk!"
    #Send message to user that he has been banned for reason
    message = f"You have been banned from {ctx.guild.name} for {reason}"
    await member.send(message)

    # And finally bans user and types in ctx chat that user has been banned
    await ctx.guild.ban(member, reason=reason)
    await ctx.channel.send(f"{member} has been banned!")

# Says hello
@bot.command()
async def hello(ctx):
    # Says hello in the context channel
    await ctx.send("Well Hello there :D")
    


bot.run(Bot-token)