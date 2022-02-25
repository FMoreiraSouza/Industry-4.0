from time import sleep
from pandas import DataFrame
from pendulum import now

from managers.tags_values import TagsValuesManager
from modules.utils import stopwatch,next_time_to_predict
from config.sync import INTERVAL
from managers import tags_values_manager

def fake_dataframe(timestamp):
    data = {
        'timestamp': timestamp,
        'RD1_MD_VRM01_PID_MILL_FEED': 1000,
        'RD1_PV_BI05_WEIGHT': 10
    }
    return DataFrame(data=data, columns=['timestamp', 'RD1_MD_VRM01_PID_MILL_FEED', 'RD1_PV_BI05_WEIGHT'], index=[0])

def ai_procedure():
    #Too see if tags_values has new values
    #You must generate a next time prediction below.
    #Otherwise, has_new_values() will always return True.
    #while not tags_values_manager.has_new_values():
    #    pass
    #get N values in descendent time
    dataframe = tags_values_manager.get_last_n_read_values(5, True)

    #AI do something here and create new predicted values
    #to the next time interval.
    next_time = next_time_to_predict(dataframe)

    #some computation
    sleep(5)

    #Predicted values
    tags_values_manager.set_predictions(fake_dataframe(next_time))

    #Define the last time predicted
    tags_values_manager.set_last_time(next_time)
