__author__ = 'sghorp'

from QuantLib import *
import datetime as dt
from math import exp
from CurveInstrument import CurveInstrument

class Edf(CurveInstrument):
    def __init__(self, ref_date, rate, tenor,  calendar):
        self.ref_date = ref_date
        self.rate = (100. - rate)/100.
        self.tenor = tenor
        self.calendar = calendar
        self.busdayadj = Unadjusted
        self.daycount = Actual360()
        self.months = {'JAN': 1, 'FEB': 2, 'MAR': 3, 'APR': 4, 'MAY': 5, 'JUN': 6, 'JUL': 7, 'AUG': 8, \
                  'SEP': 9, 'OCT': 10, 'NOV': 11, 'DEC': 12}
        self.begin_date = self.get_begin_date()
        self.end_date = self.get_end_date()
        self.offset = self.end_date - self.ref_date
        self.yf = round(self.daycount.yearFraction(self.begin_date,self.end_date),8)
        self.end_date_serial = self.end_date.serialNumber()

    def get_begin_date(self):
        #split tenor into JUN and 16
        str = self.tenor.split('-')
        mon = self.months.get(str[0])
        return IMM.nextDate(Date(1, mon, 2000+int(str[1])))

    def get_end_date(self):
        return self.calendar.advance(self.begin_date, Period(3, Months), self.busdayadj)

    def get_df_row(self):
        return ['Future', 'CME-EURODOLLAR-'+self.tenor, \
                self.qldate_to_pydate(self.begin_date),self.qldate_to_pydate(self.end_date), \
                #self.qldate_to_pydate(self.begin_date),self.qldate_to_pydate(self.end_date), \
                self.offset, self.yf, self.rate]
    def get_market_implied_df(self):
        return 1.0 / self.cf

    def get_curve_implied_df(self, guess):
        return 1.0 / exp(guess * self.yf)
