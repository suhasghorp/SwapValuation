from QuantLib import *
from math import log, exp
import pandas as pd
from scipy import interpolate
from datetime import date


calendar = JointCalendar(UnitedStates(UnitedStates.Settlement), UnitedKingdom(UnitedKingdom.Exchange),JoinHolidays)
calendar.addHoliday(Date(5,6,2012)) # Add Queens Jubilee Holiday
settlementDate = Date(6, May, 2014)
today = Date(15, April, 2016)
Settings.instance().evaluationDate = today
maturityDate = Date(6, 5, 2034)
notional = 1650000.0
fixedRate = 0.03310500
fixedLegDayCount = Thirty360()
floatingLegDayCount = Actual360()

liborCurveDates = [Date(16, 4, 2016),
                   Date(18, 4, 2016),
                   Date(19, 4, 2016),
                   Date(26, 4, 2016),
                   Date(19, 7, 2016),
                   Date(15, 9, 2016),
                   Date(21, 12, 2016),
                   Date(21, 3, 2017),
                   Date(15, 6, 2017),
                   Date(21, 9, 2017),
                   Date(20, 12, 2017),
                   Date(20, 3, 2018),
                   Date(21, 6, 2018),
                   Date(23, 4, 2019),
                   Date(21, 4, 2020),
                   Date(19, 4, 2021),
                   Date(19, 4, 2022),
                   Date(19, 4, 2023),
                   Date(19, 4, 2024),
                   Date(22, 4, 2025),
                   Date(20, 4, 2026),
                   Date(19, 4, 2028),
                   Date(21, 4, 2031),
                   Date(22, 4, 2036),
                   Date(23, 4, 2041),
                   Date(19, 4, 2046),
                   Date(19, 4, 2056),
                   Date(19, 4, 2066),
                   Date(20, 4, 2076) ]
liborZeroRates = [0.0038097,
                  0.0038088,
                  0.0038088,
                  0.0039412,
                  0.0062247,
                  0.0063501,
                  0.0068152,
                  0.007195,
                  0.0074916,
                  0.0077988,
                  0.0080705,
                  0.0083555,
                  0.0086404,
                  0.0094206,
                  0.0104417,
                  0.0114788,
                  0.0125598,
                  0.013539,
                  0.0144499,
                  0.0152657,
                  0.0159983,
                  0.0173084,
                  0.0187003,
                  0.020124,
                  0.020792,
                  0.0211892,
                  0.0212766,
                  0.021006,
                  0.0208285]
calcYF = [floatingLegDayCount.yearFraction(today, x) for x in liborCurveDates]
calcDF = [1./(1. + (r * yf)) for r, yf in zip(liborZeroRates, calcYF)]
print calcDF
liborDiscFactors = [1.0,
                    0.999989,
                    0.999968,
                    0.999958,
                    0.99988,
                    0.99836,
                    0.997307,
                    0.995282,
                    0.993234,
                    0.991182,
                    0.988724,
                    0.986343,
                    0.98381,
                    0.981073,
                    0.971582,
                    0.958396,
                    0.943398,
                    0.92639,
                    0.90836,
                    0.889377,
                    0.869866,
                    0.850278,
                    0.810206,
                    0.752613,
                    0.665168,
                    0.590692,
                    0.525476,
                    0.42256,
                    0.345407,
                    0.282258]



oisCurveDates = [today, Date(19, 4, 2016), Date(19, 5, 2016), Date(20, 6, 2016), Date(19, 7, 2016), Date(19, 8, 2016), Date(19, 9, 2016),
                 Date(19, 10, 2016), Date(19, 1, 2017), Date(19, 4, 2017),
                 Date(19, 4, 2018), Date(22, 4, 2019), Date(20, 4, 2020), Date(19, 4, 2021),
                 Date(19, 4, 2023), Date(20, 4, 2026), Date(19, 4, 2028), Date(21, 4, 2031),
                 Date(21, 4, 2036), Date(22, 4, 2041), Date(19, 4, 2046), Date(19, 4, 2056), Date(19, 4, 2066)]

oisDiscFactors = [1.0, 0.99995805,0.99963983,0.9992989,0.99899593,0.99855369,0.99820806,0.99777454,
                    0.99650212,0.99511013,0.98871444,0.97989867,0.96970703,0.95767071,0.92849575,
                    0.8785243,0.84585957,0.791129,0.71144439,0.64560551,0.58139812,0.48863201,0.41385967]

liborFixings = []
liborFixings.append((Date(4, 8, 2014).serialNumber(), 0.0023710))
liborFixings.append((Date(1, 5, 2014).serialNumber(), 0.0022285))
liborFixings.append((Date(4, 11, 2014).serialNumber(), 0.0023185))
liborFixings.append((Date(4, 2, 2015).serialNumber(), 0.0025510))
liborFixings.append((Date(1, 5, 2015).serialNumber(), 0.0027975))
liborFixings.append((Date(4, 8, 2015).serialNumber(), 0.0030110))
liborFixings.append((Date(4, 11, 2015).serialNumber(), 0.0033660))
liborFixings.append((Date(4, 2, 2016).serialNumber(), 0.0062020))
liborFixings.sort(key=lambda tup: tup[0])

liborInterpolator = interpolate.interp1d([float(x.serialNumber()) for x in liborCurveDates], [log(x) for x in liborDiscFactors], kind='cubic')
oisInterpolator = interpolate.interp1d([float(x.serialNumber()) for x in oisCurveDates], [log(x) for x in oisDiscFactors], kind='cubic')
zeroInterpolator = interpolate.interp1d([float(x.serialNumber()) for x in liborCurveDates], liborZeroRates, kind='cubic')


floatSchedule = Schedule (settlementDate, maturityDate,
                              Period(3, Months), calendar,
                              ModifiedFollowing, ModifiedFollowing,
                              DateGeneration.Forward, False)
fixedSchedule = Schedule(settlementDate, maturityDate,
                              Period(6, Months), calendar,
                              ModifiedFollowing, ModifiedFollowing,
                              DateGeneration.Forward, False)




def getPeriods(beginDates, endDates):
    period = []
    counter = 0
    for x, y in zip(beginDates, endDates):
        if x <= today <= y:
            counter = 1
        elif x < today and y < today:
            pass
        elif x > today and y > today:
            counter += 1
        period.append(counter)
    return period

def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')
def buildFloatingLeg():

    def getForward(x):
        discount_before = dfFloating[dfFloating['Pmt End'] == x].iloc[0]['LiborDiscount']
        discount_now = dfFloating[dfFloating['Pmt Begin'] == x].iloc[0]['LiborDiscount']
        yf = dfFloating[dfFloating['Pmt Begin'] == x].iloc[0]['YF']
        forward = ((discount_before / discount_now) - 1) * (1.0 / yf)
        return forward

    def getFixing(x):
        fixingDate = calendar.advance(x, Period(-2, Days), ModifiedFollowing).serialNumber()
        index = [i for i, v in enumerate(liborFixings) if v[0] == fixingDate]
        return liborFixings[index[0]][1]
    pmtDates = []
    for d in floatSchedule:
        pmtDates.append(d)
    pmtBegin = pmtDates[0:len(pmtDates)-1]
    pmtEnd = pmtDates[1:len(pmtDates)]
    dfFloating = pd.DataFrame(index=range(len(pmtDates)-1))
    dfFloating['Pmt Begin'] = pmtBegin
    dfFloating['Pmt End'] = pmtEnd
    dfFloating['Period'] = getPeriods(pmtBegin, pmtEnd)
    dfFloating['YF'] = [floatingLegDayCount.yearFraction(x,y) for x, y in zip(pmtBegin, pmtEnd)]
    dfFloating['LiborDiscount'] = [exp(liborInterpolator(x.serialNumber())) if x >= today else 0 for x in pmtEnd ]
    dfFloating['OISDiscount'] = [exp(oisInterpolator(x.serialNumber())) if x >= today else 0 for x in pmtEnd ]
    dfFloating['Forward'] = [getFixing(x) if x < today else getForward(x) for x in pmtBegin]
    dfFloating['Floating Proj Pmt'] = notional * dfFloating['Forward'] * dfFloating['YF']
    dfFloating['Floating PV Disc'] = dfFloating['Floating Proj Pmt'] * dfFloating['OISDiscount']
    return dfFloating

def buildFixedLeg():
    pmtDates = []
    for d in fixedSchedule:
        pmtDates.append(d)
    pmtBegin = pmtDates[0:len(pmtDates) - 1]
    pmtEnd = pmtDates[1:len(pmtDates)]
    dfFixed = pd.DataFrame(index=range(len(pmtDates) - 1))
    dfFixed['Pmt Begin'] = pmtBegin
    dfFixed['Pmt End'] = pmtEnd
    dfFixed['Period'] = getPeriods(pmtBegin, pmtEnd)
    dfFixed['YF'] = [fixedLegDayCount.yearFraction(x, y) for x, y in zip(pmtBegin, pmtEnd)]
    dfFixed['LiborDiscount'] = [exp(liborInterpolator(x.serialNumber())) if x >= today else 0 for x in pmtEnd]
    dfFixed['OISDiscount'] = [exp(oisInterpolator(x.serialNumber())) if x >= today else 0 for x in pmtEnd]
    dfFixed['Fixed Proj Pmt'] = notional * fixedRate * dfFixed['YF']
    dfFixed['temp'] = notional * dfFixed['YF'] * dfFixed['OISDiscount']
    dfFixed['Fixed PV Disc'] = dfFixed['Fixed Proj Pmt'] * dfFixed['OISDiscount']
    return dfFixed

dfFloating = buildFloatingLeg()
dfFixed = buildFixedLeg()
currentFloatingPmtBeginDate = dfFloating[dfFloating['Period'] == 1].iloc[0]['Pmt Begin']
currentFixedPmtBeginDate = dfFixed[dfFixed['Period'] == 1].iloc[0]['Pmt Begin']

accrualFixed = notional * fixedRate * (today - currentFixedPmtBeginDate)/360.
accrualFloating = notional * 0.0062020 * (today - currentFloatingPmtBeginDate)/360.

mvFixed = dfFixed['Fixed PV Disc'].sum(axis=0)
mvFloating = dfFloating['Floating PV Disc'].sum(axis=0)
npv = mvFixed - mvFloating

beRate = mvFloating/dfFixed['temp'].sum(axis=0)

dfFloating['Pmt Begin'] = dfFloating['Pmt Begin'].apply(lambda x: date(x.year(), x.month(), x.dayOfMonth()))
dfFloating['Pmt End'] = dfFloating['Pmt End'].apply(lambda x: date(x.year(), x.month(), x.dayOfMonth()))
dfFixed['Pmt Begin'] = dfFixed['Pmt Begin'].apply(lambda x: date(x.year(), x.month(), x.dayOfMonth()))
dfFixed['Pmt End'] = dfFixed['Pmt End'].apply(lambda x: date(x.year(), x.month(), x.dayOfMonth()))

writer = pd.ExcelWriter('frame.xls')
dfFloating.to_excel(writer, 'Floating')
dfFixed.to_excel(writer, 'Fixed')
writer.save()





print accrualFixed - accrualFloating #accrued
principal = swap.NPV() - (accrualFixed - accrualFloating) # clean MV
premiumOrPrice = principal/notional
print premiumOrPrice



















'''p3m = Period(3, Months)
endDate = today + 8 * p3m
dates = []
schedule = Schedule( today,
                     endDate,
                     Period(Quarterly),
                     calendar,
                     Unadjusted,
                     Unadjusted,
                     DateGeneration.Backward,
                     False)
for d in schedule:
    dates.append(d)
yf = []
dd = []
dates.insert(0, today)
for i in range(1, len(dates)):
    df = dates[i] - dates[i-1]
    dd.append(df)
    t = df/360.
    print df, t
    yf.append(t)


tempDiscFactors = [1., 0.998724, 0.994915, 0.987925, 0.979152, 0.969457, 0.958690, 0.946531, 0.933045]
impFwdRates = []
for i in range(1, len(tempDiscFactors)):
    impFwdRates.append((tempDiscFactors[i-1]/tempDiscFactors[i] - 1.) * (1./yf[i]))
discFactors = tempDiscFactors[1:]
yf = yf[1:]
#impFwdRates = [0.005, 0.014981, 0.027989, 0.035840, 0.039132, 0.043949, 0.050818, 0.057815]

sum = 0
for i in range(0, len(discFactors)):
    sum += impFwdRates[i] * yf[i] * discFactors[i]
sum += discFactors[-1]
mvFRN = (100000000. * sum)
print mvFRN

sum = 0
for i in range(0, len(discFactors)):
    sum += yf[i] * discFactors[i]
mvFixed = 100000000. * ((0.0526 * sum) + discFactors[-1])
print mvFixed

print 'NPV LIBOR:%f' % (mvFixed - mvFRN)'''


