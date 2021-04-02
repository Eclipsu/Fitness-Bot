import discord                                  # discord.py module.
from discord.ext import commands, tasks         # discord.py commands module.
import asyncio                                  # time.sleep function.
import json                                     # json module for reading and writing into json file(s).
from datetime import datetime                   # datetime for getting current time. 
import datetime as dt                           # datetime for setting time.
import functions 

client = commands.Bot(command_prefix = "<3 ")   # global bot delcaration.

async def print_routine(ch):
    """
    displays the schedule of the day (today).
    Args:
        cr_year, cr_month, cr_day    = Current year/month/day.
        week_days                    = array of weeks (starts with monday and ends with monday to fit internation week format).
        week_num                     = a int which acts as index to get current week from week_days array.
        title......**                = retuned value which contains information about the embed.

        schedule_embed               = embed containing info about todays schedule.
    """
    
    channel = client.get_channel(ch)
    week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    cr_year   = datetime.today().strftime('%Y')
    cr_month  = datetime.today().strftime('%m')
    cr_day    = datetime.today().strftime('%d')
    week_num  = dt.date(int(cr_year), int(cr_month), int(cr_day)).weekday()
    print(week_num)

    if week_num == 4: #if its friday (rest day)
        rest_embed = discord.Embed(
            title = f'🛌: Rest! ' ,
            color = discord.Color.purple(),
            description = 'Great! You did awsome! Lets get some rest, and call this a skip day today!'
        )
        rest_embed.set_image(url = 'https://raw.githubusercontent.com/Eclipsu/Fitness-Bot/MAIN/assets/rest.gif')
        rest_embed.set_thumbnail(url = 'https://raw.githubusercontent.com/Eclipsu/Fitness-Bot/MAIN/assets/rest.webp')
        await channel.send(embed = rest_embed)
        return

    title,_1_title, _1_reps, _1_link,  _2_title, _2_reps, _2_link, _3_title, _3_reps, _3_link, _4_title, _4_reps, _4_link, _5_title, _5_reps, _5_link, _6_title, _6_reps, _6_link = functions.get_routine(week_days[week_num])
    schedule_embed = discord.Embed(
        title = f'📋 {title}',
        color = discord.Color.purple(),
        description = 'Do 4 rounds of each reps!'
    )
    schedule_embed.add_field(name = _1_title,  value  = f"[{_1_reps}]({_1_link}) reps", inline = True)
    schedule_embed.add_field(name = _2_title,  value  = f"[{_2_reps}]({_2_link}) reps", inline = True)
    schedule_embed.add_field(name = _3_title,  value  = f"[{_3_reps}]({_3_link}) reps", inline = True)
    schedule_embed.add_field(name = _4_title,  value  = f"[{_4_reps}]({_4_link}) reps", inline = True)
    schedule_embed.add_field(name = _5_title,  value  = f"[{_5_reps}]({_5_link}) reps", inline = True)
    schedule_embed.add_field(name = _6_title,  value  = f"[{_6_reps}]({_6_link}) reps", inline = True)
    schedule_embed.set_footer(text = 'DM us for more info')

    await channel.send(embed = schedule_embed)


# bot on ready function
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('<3/ Workout'))
    print(f'Bot deployed!')
    print('Logged in as:')
    print(f'Username: {client.user.name}')
    print(f'ID: {str(client.user.id)}')
    print('------')




#for Attendance reaction
@client.command(pass_contest=True)
async def testi(ctx):
    await ctx.message.add_reaction("👍🏿") #adding reaction to the comand
    embed = discord.Embed(
        title = "Attendance 📋",
        description = " React below to Mark your attendance  ",
        color= discord.Color.purple()


    )
    msg = await ctx.send(embed=embed)
    await msg.add_reaction("✅") #adding reaction to embed
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['✅']
    while True:
        reaction, user = await client.wait_for("reaction_add", timeout=60, check=check)
        if str(reaction.emoji) == "✅":
                await ctx.send('{} Done!'.format(user))
    else:
        await msg.remove_reaction(reaction, user) 

@client.command()
async def schedule(ctx):
    """
    displays the schedule of the day (today).
    Calls:
        print_routine()
    Args:
        channe_id = channel id 
    """

    channel_id = ctx.channel.id
    await print_routine(ch = int(channel_id))

# lists outs schedule of the week
@client.command()
async def routine(ctx):
    """
    Displays routine of the whole week.
    Args:
        routine_embed = Embed with information about the routine of the whole week.
    """

    routine_embed = discord.Embed(
        title = "\📋: Routine",
        color = discord.Color.purple(),
        description = "7 days, 6 grind, 1 rest."
    )
    routine_embed.add_field(name = "Sun",  value  = "Push day", inline = True)
    routine_embed.add_field(name = "Mon",  value  = "Pull day", inline = True)
    routine_embed.add_field(name = "Tues", value  = "Leg day", inline = True)
    routine_embed.add_field(name = "Wed",  value  = "Abs day", inline = True)
    routine_embed.add_field(name = "Thrs", value  = "Pull day", inline = True)
    routine_embed.add_field(name = "Sat",  value  = "Pull day")
    routine_embed.set_thumbnail(url = 'https://media4.giphy.com/media/3o7qE4gcYTW1zZPkre/source.gif')
    routine_embed.set_footer(text = 'Friday rest  🛌')

    await ctx.send(embed = routine_embed)


@client.command()
async def ping(ctx):
    """
    Displays the latency of the bot (TEST COMMAND)
    """
    
    await ctx.send(f'Pong! 🏓 {round(client.latency*1000)}ms')

async def check_reminder():
    """
    a function loop for checking reminder every sec.
    Calls:
        get_routine_time() to get routine time
    Args:
        now: current time
        std_reminder: workout times
    """
    
    while(True):
        await asyncio.sleep(1)
        now = datetime.now()
        current_time  = now.strftime("%H:%M:%S")
        wt_h, wt_m, wt_s = functions.get_routine_time()

        std_reminder = dt.time(int(wt_h), int(wt_m), int(wt_s))
        if current_time == str(std_reminder):
            print('time')
            channel = client.get_channel(813017363443482645)
            await channel.send(f'<@&{825697640560853004}> Its time to grind!\n your schedule for today: ')
            await print_routine(ch = 813017363443482645)
        
client.loop.create_task(check_reminder())
client.run(functions.get_token())

