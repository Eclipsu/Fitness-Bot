import discord                                  # discord.py module.
from discord.ext import commands, tasks         # discord.py commands module.
import asyncio                                  # time.sleep function.
import json                                     # json module for reading and writing into json file(s).
from datetime import datetime                   # datetime for getting current time. 
import datetime as dt                           # datetime for setting time.
import functions                                # external file containing getters and settrs and other functions

client = commands.Bot(command_prefix = "<3 ")   # global bot delcaration.


# bot on ready function
@client.event
async def on_ready():
    wt_h, wt_m, wt_s = functions.get_routine_time()
    await client.change_presence(activity = discord.Game("<3 profile"))
    print(f'------')
    print(f'Bot deployed!')
    print(f'Logged in as: {client.user.name}')
    print(f'------')
    print(f'Reminder set to : {wt_h}:{wt_m}:{wt_s}')
    print(f'------')


@client.event
async def on_reaction_add(reaction, user):
    channel = client.get_channel(827830879359336448)
    # if reaction.message.author.id == client.user.id: # Ignore bots reaction
    #     return
    if reaction.message.channel.id != 827830879359336448: # Ignore other channels except attendence channnel
        return

    if reaction.emoji == "✅": # Workout done
        try: # If user data exist in our db
            old_workout, old_streak, old_skip, old_top_streak = functions.get_user_data(user.id) # Get old user data
            new_workout = old_workout + 1 # Incriment workout by 1
            new_streak  = old_streak + 1 # Incriment streak by 1
            new_skip    = old_skip + 0 # No changes
            if new_streak == old_top_streak or new_streak > old_top_streak:
                new_top_streak = old_top_streak + 1
            elif new_streak < old_top_streak:
                new_top_streak = old_top_streak + 0
            
            functions.set_user_data(user.id, new_workout, new_streak, new_skip, new_top_streak) # Updates the user data
            
        except: # If it doesn't exist.
            functions.set_user_data(user.id, 0 + 1, 0 + 1, 0, 1) # Makes user data
    if reaction.emoji == "❌": # Workout skip
        try:  # If user data exist in our db
            old_workout, old_streak, old_skip, old_top_streak = functions.get_user_data(user.id) # Get old user data
            new_workout = old_workout + 0 # now changes
            new_streak  = old_streak * 0 # Resets streak
            new_skip    = old_skip + 1 # Increments streak by one
            print(f"Purano: {old_top_streak} Naya: {new_streak} ")
            new_top_streak = old_top_streak
            functions.set_user_data(user.id, new_workout, new_streak, new_skip, new_top_streak) # Updates db
        except: # If it doesn't exist.
            functions.set_user_data(user.id, 0, 0, 1, 0)# Makes user data

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
    
    channel = client.get_channel(ch) # Channel ID
    week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'] 
    cr_year   = datetime.today().strftime('%Y')
    cr_month  = datetime.today().strftime('%m')
    cr_day    = datetime.today().strftime('%d')
    week_num  = dt.date(int(cr_year), int(cr_month), int(cr_day)).weekday()

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


@client.command()
async def profile(ctx, member : discord.Member):
    """
    Displays profile of a user.
    Args:
        workout, streak, skips = user data
    """
    try: # If user data is in our database
        workout, streak, skips, top_streak = functions.get_user_data(member.id)
        profile_embed = discord.Embed(title="Profile", description=f"{member.name}'s profile", color = discord.Color.purple())
        profile_embed.set_thumbnail(url = member.avatar_url)
        profile_embed.add_field(name="Workouts: ", value = f"{workout} Days", inline=True) # Workouts
        profile_embed.add_field(name="Skips: ", value = f"{skips}", inline=True) # Skips
        profile_embed.add_field(name="Streaks: ", value = f"{streak}", inline=True)
        profile_embed.set_footer(text = f"{member.name}'s top streak: {top_streak}")
        await ctx.send(content=None, embed=profile_embed)


    except: # If its not in our database, make it.
        functions.set_user_data(member.id, 0, 0, 0, 0)
        workout, streak, skips, top_streak = functions.get_user_data(member.id)
        profile_embed = discord.Embed(title="Profile", description=f"{member.name}'s' Profile", color = discord.Color.purple())
        profile_embed.set_thumbnail(url = member.avatar_url)
        profile_embed.add_field(name="Workouts: ", value = f"{workout} Days", inline=True) # Workouts
        profile_embed.add_field(name="Skips: ", value = f"{skips}", inline=True) # Skips
        profile_embed.add_field(name="Streaks: ", value = f"{streak}", inline=True)
        profile_embed.set_footer(text = f"{member.name}'s top streak: {top_streak}")
        await ctx.send(content=None, embed=profile_embed)


@profile.error
async def profile_handler(ctx, error):
    """A local Error Handler for our command do_repeat.
    This will only listen for errors in do_repeat.
    The global on_command_error will still be invoked after.
    """

    # Check if our required argument inp is missing.
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'member':
            try: # If user data is in our database
                workout, streak, skips, top_streak = functions.get_user_data(ctx.author.id)
                profile_embed = discord.Embed(title="Profile", description= f"{ctx.author.name} Profile", color = discord.Color.purple())
                profile_embed.set_thumbnail(url = ctx.author.avatar_url)
                profile_embed.add_field(name="Workouts: ", value = f"{workout} Days", inline=True) # Workouts
                profile_embed.add_field(name="Skips: ", value = f"{skips}", inline=True) # Skips
                profile_embed.add_field(name="Streaks: ", value = f"{streak}", inline=True)
                profile_embed.set_footer(text = f"{ctx.author.name}'s top streak: {top_streak}")
                await ctx.send(content=None, embed=profile_embed)


            except: # If its not in our database, make it.
                functions.set_user_data(ctx.author.id, 0, 0, 0, 0)
                workout, streak, skips, top_streak = functions.get_user_data(ctx.author.id)
                profile_embed = discord.Embed(title="Profile", description=f"{ctx.author.name}", color = discord.Color.purple())
                profile_embed.set_thumbnail(url = ctx.author.avatar_url)
                profile_embed.add_field(name="Workouts: ", value = f"{workout} Days", inline=True) # Workouts
                profile_embed.add_field(name="Skips: ", value = f"{skips}", inline=True) # Skips
                profile_embed.add_field(name="Streaks: ", value = f"{streak}", inline=True)
                profile_embed.set_footer(text = f"{ctx.author.name}'s top streak: {top_streak}")
                await ctx.send(content=None, embed=profile_embed)




#for Attendance reaction
@client.command(pass_contest=True)
async def attendence(ctx):
    today = today = datetime.today()
    today_date = today.strftime("%d/%m/%Y")
    attendence_embed = discord.Embed(
        title = f"{today_date}'s Attendance 📋",
        description = " React below to Mark your attendance  ",
        color= discord.Color.purple()
    )

    msg = await ctx.send(embed = attendence_embed)
    await msg.add_reaction("✅") # YES
    await msg.add_reaction("❌") # NO  

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
        current_time  = now.strftime("%H:%M:%S") # Current time
        wt_h, wt_m, wt_s = functions.get_routine_time() # Reminder time
        std_reminder = dt.time(int(wt_h), int(wt_m), int(wt_s)) 
        # attendence_time = dt.time(int(wm_h), int(wt_m)  + 30, int(wt_s))

        attendence_time = dt.time(int(wt_h), int(wt_m) + 30, int(wt_s)) # Attendence 30 minutes after workout
        
        if current_time == str(std_reminder): # Reminder
            global channel
            channel = client.get_channel(827830863127248896)
            await channel.send(f'<@&{827955469884325909}> its time to grind!\n your schedule for today: ')
            await print_routine(ch = 827830863127248896)
        
        if current_time == str(attendence_time): # Attendence
            await channel.send(f'<@&{827955469884325909}> Did you do your workout?: ')
            today = today = datetime.today()
            today_date = today.strftime("%d/%m/%Y")
            attendence_embed = discord.Embed(
                title = f"{today_date}'s Attendance 📋",
                description = " React below to Mark your attendance  ",
                color= discord.Color.purple()
            )

            attendence_channel = client.get_channel(827830879359336448)
            msg = await attendence_channel.send(embed = attendence_embed)
            await msg.add_reaction("✅") # YES
            await msg.add_reaction("❌") # NO 
 
client.loop.create_task(check_reminder())
client.run(functions.get_token())

