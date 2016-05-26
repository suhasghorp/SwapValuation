__author__ = 'sghorp'

from QuantLib import *
from math import exp
import datetime as dt



class CurveInstrument:
    def qldate_to_pydate(self, qldate):
        return dt.date(qldate.year(), qldate.month(), qldate.dayOfMonth())

    def get_df_row(self):
        raise NotImplementedError