# Django Libraries
import datetime


def get_achievement_id(request):
    """
    Method to create achievement_id for each achievement.
    return type: integer
    """
    time_stamp= int(str(datetime.datetime.now())[11:].replace(":","").replace(".",""))
    return time_stamp
	
