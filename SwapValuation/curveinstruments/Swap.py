__author__ = 'sghorp'

from QuantLib import *
from math import exp
import datetime as dt
from CurveInstrument import CurveInstrument



class Swap(CurveInstrument):
    def __init__(self, ref_date, rate, tenor, calendar):
        self.ref_date = ref_date
        self.rate = rate
        self.tenor = tenor
        self.calendar = calendar

        self.fixedLegFrequency = Semiannual
        self.fixedLegTenor = Period(6, Months)
        self.fixedLegAdjustment = Unadjusted
        self.fixedLegDayCounter = Thirty360()

        self.floatingLegFrequency = Quarterly
        self.floatingLegTenor = Period(3, Months)
        self.floatingLegAdjustment = ModifiedFollowing

        self.begin_date = self.get_begin_date()
        self.end_date = self.get_end_date()
        self.offset = self.end_date - self.ref_date
        self.yf = round(self.daycount.yearFraction(self.begin_date,self.end_date),8)
        self.end_date_serial = self.end_date.serialNumber()

    def get_begin_date(self):
        return self.ref_date

    def get_end_date(self):
        #split tenor into n and timeunits
        n, timeunit = int(self.tenor[:-1]),self.tenor[-1:]
        if timeunit == 'Y':
            return self.calendar.advance(self.settle_date, Period(n, Years), self.floatingLegAdjustment)
        else:
            raise ValueError('Swap was given with a non Year tenor, possibly Day or Week or Month', self.tenor)

    def get_df_row(self):
        return ['Swap', 'USD-LIBOR-' + self.tenor, \
                self.qldate_to_pydate(self.begin_date), self.qldate_to_pydate(self.end_date), \
                # self.qldate_to_pydate(self.begin_date),self.qldate_to_pydate(self.end_date), \
                self.offset, self.yf, self.rate]


