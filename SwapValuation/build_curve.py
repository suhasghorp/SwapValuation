from QuantLib import *
from math import log, exp
import pandas as pd
from scipy import interpolate
from datetime import date

from curveinstruments import Depo, Edf


calendar = JointCalendar(UnitedStates(UnitedStates.Settlement), UnitedKingdom(UnitedKingdom.Exchange),JoinHolidays)
calendar.addHoliday(Date(5,6,2012)) # Add Queens Jubilee Holiday
today = Date(3, April, 2012)
Settings.instance().evaluationDate = today
settlementDate = calendar.advance(today, Period(2, 'Days'), ModifiedFollowing)

#only upto 6M liquid
depoON = Depo(today, 0.003861, '1D')
depoTN = Depo(today, 0.003861, '2D')
depo1W = Depo(today, 0.004055, '1W')
depo1M = Depo(today, 0.004497, '1M')
depo2M = Depo(today, 0.005531, '2M')
depo3M = Depo(today, 0.0066655, '3M')
depo6M = Depo(today, 0.009756, '6M')

# we are in sep 2017 now, so select sep-17 futures contract
# take 8 futures contracts
edfSEP17 = Edf(today,98.84,'SEP-17')
