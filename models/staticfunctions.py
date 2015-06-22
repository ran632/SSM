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

    @staticmethod
    def dateToDate(sundayDate, day):
        return sundayDate+timedelta(days=day-1)

    @staticmethod
    def dayToString(day):
        return{
            1:'Sunday',
            2:'Monday',
            3:'Tuesday',
            4:'Wednesday',
            5:'Thursday',
            6:'Friday',
            7:'Saturday'
        }.get(day, 'noday')

    @staticmethod
    def hourToString(hour):
        int(hour)
        return{
            0:'Morning',
            1:'Evening',
            2:'Night'
        }.get(hour, 'nohour')
