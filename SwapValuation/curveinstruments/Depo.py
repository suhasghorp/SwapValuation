__author__ = 'sghorp'

from QuantLib import *
from math import exp
import datetime as dt
from CurveInstrument import CurveInstrument



class Depo(CurveInstrument):
    def __init__(self, ref_date, rate, tenor, calendar):
        self.ref_date = ref_date
        self.rate = rate
        self.tenor = tenor
        self.calendar = calendar
        self.busdayadj = ModifiedFollowing
        self.daycount = Actual360()
        self.settlementdays = 2
        self.begin_date = self.get_begin_date()
        self.end_date = self.get_end_date()
        self.yf = round(self.daycount.yearFraction(self.begin_date,self.end_date),8)
        self.end_date_serial = self.end_date.serialNumber()

    def get_begin_date(self):
        return self.ref_date

    def get_end_date(self):
        #split tenor into n and timeunits
        n, timeunit = int(self.tenor[:-1]),self.tenor[-1:]
        if timeunit == 'D':
            return self.calendar.advance(self.begin_date, Period(n, Days), self.busdayadj)
        elif timeunit == 'W':
            return self.calendar.advance(self.begin_date, Period(n, Weeks), self.busdayadj)
        elif timeunit == 'M':
            return self.calendar.advance(self.begin_date, Period(n, Months), self.busdayadj)

    def get_interval_begin_date(self):
        #comment
        if self.prev_end_date == Date():
            return self.begin_date
        else:
            return self.prev_end_date

    def get_interval_end_date(self):
        return self.end_date

    def get_df_row(self):
        return ['MoneyMarket', 'USD-DEPOSIT-'+self.tenor, \
                self.qldate_to_pydate(self.begin_date), self.qldate_to_pydate(self.end_date), \
                #self.qldate_to_pydate(self.get_interval_begin_date()), self.qldate_to_pydate(self.get_interval_end_date()), \
                self.end_date - self.ref_date, self.yf, self.rate]

