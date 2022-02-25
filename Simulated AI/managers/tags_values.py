from database.connection import db_client
from pendulum import timezone, instance
from config.timezone import LOCAL_TIME_ZONE
from pandas import DataFrame
from models.tags_values import TagsValuesModel
from modules.utils import without_keys


class TagsValuesManager:
    def __init__(self):
        self.db_client = db_client.connect()
        self.last_time = None

    def get_last_n_read_values(self, number: int, reverse: bool) -> DataFrame:
        """
        This function returns the last number documents of tags values read from OPC.
        If reverse is True, it will return the values in descendant time order.
        Otherwise, when reverse is False, it will return the values in ascendant time order.
        The function will return a Dataframe that could be manipulated to recover
        each tag value in some timestamp.
        """
        number_of_tags_values = TagsValuesModel.objects().count()
        index = number_of_tags_values - number
        tags_values = None
        tz = timezone(LOCAL_TIME_ZONE)

        if index > 0:
            tags_values = TagsValuesModel.objects[index:]
        else:
            tags_values = TagsValuesModel.objects[:]

        if not tags_values:
            return None

        columns = ['timestamp']
        columns.extend(tags_values[0].read.keys())

        values_to_dt = []

        for tag_value in tags_values:
            new_dict = {'read': {}}  # create a new dict.
            timestamp = tag_value['timestamp'] # get the timestamp for the retrieved data.
            # timestamp = timestamp / 1000 # convert to seconds.
            # timestamp = datetime.fromtimestamp(int(timestamp))# convert the timestamp to datetime.
            in_utc = instance(timestamp) # convert the timestamp to datetime in UTC time zone.
            new_dict['read']['timestamp'] = tz.convert(in_utc).to_iso8601_string()  # put the timestamp as a dict value.

            for key in tag_value['read']:  # for every tag and value, insert them into the dict.
                new_dict['read'][key] = tag_value['read'][key]

            values_to_dt.append(new_dict)  # put the dict into the result list.

        dt = None

        if reverse:
            dt = DataFrame(data=[values['read']
                                 for values in values_to_dt[::-1]], columns=columns)
        else:
            dt = DataFrame(data=[values['read']
                                 for values in values_to_dt], columns=columns)

        return dt

    def set_last_time(self, time):
        """
            Sets last_time as the last time that AI predicted something.
            time must be a datetime in UTC time zone.
        """
        self.last_time = time

    def has_new_values(self) -> bool:
        """
            This function verifies if the last time predicted has real values
            collected. If the last time predicted is None, it will return True
            to force AI to predict new values, because it is being started.
            Otherwise, it will see if the last time predicted has some new values.
        """
        if not self.last_time:
            return True
        else:
            timestamp_doc = TagsValuesModel.objects(timestamp=self.last_time)

            if timestamp_doc and (len(timestamp_doc[0].read) != 0):
                return True

            return False

    def set_predictions(self, dataframe):
        predicted = dataframe.to_dict('records')[0]
        predicted['timestamp'] = predicted['timestamp'].tz_convert(tz='UTC')

        query_result = TagsValuesModel.objects(timestamp=predicted['timestamp'])
        tags_values = query_result.first()

        if tags_values == None:
            tags_values = TagsValuesModel()
            tags_values.timestamp = predicted['timestamp']
            tags_values.read = {}
            tags_values.predicted = without_keys(predicted, {'timestamp'})
            tags_values.save()
        else:
            tags_values.predicted = without_keys(predicted, {'timestamp'})
            tags_values.save()