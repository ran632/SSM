__author__ = 'Administrator'
from datetime import *


class Staticfunctions():
    @staticmethod
    def nextWeekDate(day):
        tmpDate = date.today()
        tmpDate += timedelta(days=1)
        while(tmpDate.weekday() != 6):
            tmpDate += timedelta(days=1)
        tmpDate += timedelta(days=day-1)
        return tmpDate