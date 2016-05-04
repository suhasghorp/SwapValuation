__author__ = 'sghorp'

from QuantLib import *
import pandas as pd
import datetime as dt

from curveinstruments import Depo, Edf

ref_date = Date(17, 9, 2008)

def qldate_to_pydate(qldate):
        return dt.date(qldate.year(), qldate.month(), qldate.dayOfMonth())

depo1 = Depo(ref_date, 0.04427547, '1D', Date())
rows = [depo1.get_df_row()]
depo2 = Depo(ref_date, 0.0436875, '1W', Date())
rows.append(depo2.get_df_row())
depo3 = Depo(ref_date, 0.0303, '1M', depo2.end_date)
rows.append(depo3.get_df_row())
depo4 = Depo(ref_date, 0.033, '2M', depo3.end_date)
rows.append(depo4.get_df_row())
depo5 = Depo(ref_date, 0.0333, '3M', depo4.end_date)
rows.append(depo5.get_df_row())
#edf1 = Edf(ref_date, 96.855, 'DEC-08')
#rows.append(edf1.get_df_row())


df = pd.DataFrame(rows, columns=['Type', 'Desc', 'Begin_Date', 'End_Date', 'Interval_Begin_Date', 'Interval_End_Date', 'Offset', 'YF', 'Quote', 'Cap_Factor'])
df.ix[0,'Cap_Factor'] = 1.00024263
writer = pd.ExcelWriter('frame.xls')
df.to_excel(writer, 'Curve')
writer.save()



