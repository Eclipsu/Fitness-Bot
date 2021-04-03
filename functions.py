import json                                     # json module for reading and writing into json file(s).
from datetime import datetime                   # datetime for getting current time. 
import datetime as dt                           

def get_routine_time():
    """
    gets time for reminder.
    Args:
        wt_h = workout time (hour)
        wt_m = workout time (minute)
        wt_s = workout time (second)
    Returns:
        reminder time : wt_h, wt_m, wt_s
    """

    with open('routine.json', 'r') as openfile:
        json_object = json.load(openfile)
        wt_h = json_object["reminder"]["h"]
        wt_m = json_object["reminder"]["m"]
        wt_s = json_object["reminder"]["s"]

    return wt_h, wt_m, wt_s

def get_token():
    """
    token grabber. returns: client's token  
    """
    with open('bot_config.json', 'r') as openfile:
        json_object = json.load(openfile)
        pairs = json_object.items()
        bot_token = json_object["token"]
    return bot_token



def get_routine(week_day):
    """
    get details about routines from routine.json
    Takes:
        week_day = week of the day eg: sunday, monday tuesday.
    Args:
        openfile, json_object, pairs = variables req by json module (honestly idk what it does). 
        today_routine                = return value containing informations about the workouts.
    Returns:
        wokrout, video, thumnail_link, gif_link, rounds, etc.
    """

    with open('routine.json', 'r') as openfile:
        json_object = json.load(openfile)
        pairs = json_object.items()
        
        routine_title = json_object[str(week_day)]['title']
        _1_title = json_object[str(week_day)]['1']['name']
        _1_reps  = json_object[str(week_day)]['1']['reps']
        _1_link  = json_object[str(week_day)]['1']['link']

        _2_title = json_object[str(week_day)]['2']['name']
        _2_reps  = json_object[str(week_day)]['2']['reps']
        _2_link  = json_object[str(week_day)]['2']['link']

        _3_title = json_object[str(week_day)]['3']['name']
        _3_reps  = json_object[str(week_day)]['3']['reps']
        _3_link  = json_object[str(week_day)]['3']['link']

        _4_title = json_object[str(week_day)]['4']['name']
        _4_reps  = json_object[str(week_day)]['4']['reps']
        _4_link  = json_object[str(week_day)]['4']['link']

        _5_title = json_object[str(week_day)]['5']['name']
        _5_reps  = json_object[str(week_day)]['5']['reps']
        _5_link  = json_object[str(week_day)]['5']['link']

        _6_title = json_object[str(week_day)]['6']['name']
        _6_reps  = json_object[str(week_day)]['6']['reps']
        _6_link  = json_object[str(week_day)]['6']['link']

    return routine_title, _1_title, _1_reps, _1_link, _2_title, _2_reps, _2_link, _3_title, _3_reps, _3_link, _4_title, _4_reps, _4_link, _5_title, _5_reps, _5_link, _6_title, _6_reps, _6_link

def get_user_data(user_id):
    """
    gets user data
    """    
    with open('attendence.json', 'r') as openfile:
        db = json.load(openfile)
        workouts  = db[f"{user_id}"]["workouts"] 
        streaks   = db[f"{user_id}"]["streaks"]
        skips     = db[f"{user_id}"]["skips"]
    return workouts, streaks, skips

def set_user_data(user_id, workout, streak, skip):
    """
    sets user data
    """
    with open('attendence.json', 'r+') as openfile:

        db = json.load(openfile)
        
        db.update({str(user_id):{"workouts":workout,"streaks":streak,"skips":skip}})
        openfile.seek(0)

        json.dump(db, openfile, indent = 4)

def init_user(user_id):
    """
    initialize user data to database
    """
    init_data = {user_id:{"workouts":0,"streaks":0,"skips":0}}
    with open("attendence.json", "r+") as openfile:
        db = json.load(openfile)
        
        db.update(init_data)
        openfile.seek(0)

        json.dump(db, openfile, indent = 4)
        # data = json.load(file)
        # data.update(a_dictionary)
        # file.seek(0)

        # json.dump(data, file, indent = 4)
