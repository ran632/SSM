__author__ = 'Administrator'
from datetime import *


class Staticfunctions():
    @staticmethod
    def nextWeekDate(day):
        nextWeek = date.today() + timedelta(days=7)
        return Staticfunctions.getSundayDate(nextWeek, day) #reduction

    @staticmethod
    def getSundayDate(someDate, day):
        while(someDate.weekday() != 6):
            someDate -= timedelta(days=1)
        someDate += timedelta(days=day-1)
        return someDate
