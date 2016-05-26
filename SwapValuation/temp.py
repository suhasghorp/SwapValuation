from QuantLib import *
from math import log, exp
import pandas as pd
from scipy import interpolate
from datetime import date

from curveinstruments import Depo, Edf, Swap


calendar = Sweden()
today = Date(3, April, 2012)
Settings.instance().evaluationDate = today
settlementDate = calendar.advance(today, Period(2, Days), ModifiedFollowing)

#only upto 6M liquid
curveInstruments = []
curveInstruments.append(Depo(today, 0.015, '1D',calendar))
nextday = calendar.advance(today, Period(1, Days), ModifiedFollowing)
curveInstruments.append(Depo(nextday, 0.01628, '1D',calendar))
curveInstruments.append(Depo(settlementDate, 0.01745, '1W',calendar))
curveInstruments.append(Depo(settlementDate, 0.0199, '1M',calendar))
curveInstruments.append(Depo(settlementDate, 0.021, '2M',calendar))
curveInstruments.append(Depo(settlementDate, 0.02255, '3M',calendar))

dfrows = [x.get_df_row() for x in curveInstruments]

edfJUN12 = Edf(today,100. - 2.13,'JUN-12')
edfSEP12 = Edf(today,100. - 2.0175,'SEP-12')
edfDEC12 = Edf(today,100. - 2.0213,'DEC-12')
edfMAR13 = Edf(today,100. - 2.0450,'MAR-13')
edfJUN13 = Edf(today,100. - 2.0725,'JUN-13')
edfSEP13 = Edf(today,100. - 2.1138,'SEP-13')
edfDEC13 = Edf(today,100. - 2.1588,'DEC-13')
edfMAR14 = Edf(today,100. - 2.2138,'MAR-14')
edfJUN14 = Edf(today,100. - 2.2683,'JUN-14')
edfSEP14 = Edf(today,100. - 2.3267,'SEP-14')
edfDEC14 = Edf(today,100. - 2.3817,'DEC-14')
edfMAR15 = Edf(today,100. - 2.4367,'MAR-15')

swap4Y = Swap(settlementDate, 0.022875, '4Y')
swap5Y = Swap(settlementDate, 0.023750, '5Y')
swap6Y = Swap(settlementDate, 0.0246, '6Y')
swap7Y = Swap(settlementDate, 0.0253, '7Y')
swap8Y = Swap(settlementDate, 0.025825, '8Y')
swap9Y = Swap(settlementDate, 0.026225, '9Y')
swap10Y = Swap(settlementDate, 0.0266, '10Y')
swap12Y = Swap(settlementDate, 0.0272, '12Y')
swap15Y = Swap(settlementDate, 0.02785, '15Y')
swap20Y = Swap(settlementDate, 0.02765, '20Y')
swap25Y = Swap(settlementDate, 0.02715, '25Y')
swap30Y = Swap(settlementDate, 0.02675, '30Y')
