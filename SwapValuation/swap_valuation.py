from QuantLib import *
import pandas as pd


calendar = JointCalendar(UnitedStates(UnitedStates.Settlement), UnitedKingdom(UnitedKingdom.Exchange),JoinHolidays)
calendar.addHoliday(Date(5,6,2012)) # Add Queens Jubilee Holiday
settlementDate = Date(6, May, 2014)
today = Date(15, April, 2016)
Settings.instance().evaluationDate = today

liborCurveDates = [today,
                   Date(16, 4, 2016),
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


liborCurve = YieldTermStructureHandle(DiscountCurve(liborCurveDates, liborDiscFactors, Actual360(), calendar ))
oisCurve = YieldTermStructureHandle(DiscountCurve(oisCurveDates, oisDiscFactors, Actual360(), calendar ))

maturityDate = Date(6, 5, 2034)
floatSchedule = Schedule (settlementDate, maturityDate,
                              Period(3, Months), calendar,
                              ModifiedFollowing, ModifiedFollowing,
                              DateGeneration.Forward, False)
fixedSchedule = Schedule(settlementDate, maturityDate,
                              Period(6, Months), calendar,
                              ModifiedFollowing, ModifiedFollowing,
                              DateGeneration.Forward, False)

libor3M_index = USDLibor(Period(3, Months), liborCurve)
libor3M_index.addFixing(Date(1, 5, 2014), 0.0022285)
libor3M_index.addFixing(Date(4, 8, 2014), 0.0023710)
libor3M_index.addFixing(Date(4, 11, 2014), 0.0023185)
libor3M_index.addFixing(Date(4, 2, 2015), 0.0025510)
libor3M_index.addFixing(Date(1, 5, 2015), 0.0027975)
libor3M_index.addFixing(Date(4, 8, 2015), 0.0030110)
libor3M_index.addFixing(Date(4, 11, 2015), 0.0033660)
libor3M_index.addFixing(Date(4, 2, 2016), 0.0062020)

notional = 1650000.0
fixedRate = 0.03310500
fixedLegDayCount = Thirty360()
floatingLegDayCount = Actual360()

swap = VanillaSwap(VanillaSwap.Receiver, notional, fixedSchedule,
               fixedRate, fixedLegDayCount, floatSchedule,
               libor3M_index, 0, floatingLegDayCount )
swapEngine = DiscountingSwapEngine(oisCurve)
swap.setPricingEngine(swapEngine)


pmtDates = [settlementDate]
pmt = []
for i, cf in enumerate(swap.leg(1)):
    print '%-10s %2d  %-18s   %10.2f' % ('Floating', i+1, cf.date(), cf.amount())
    pmtDates.append(cf.date())
    pmt.append(cf.amount())
pmtBegin = pmtDates[0:len(pmtDates)-1]
pmtEnd = pmtDates[1:len(pmtDates)]

df = pd.DataFrame(index=range(len(pmtDates)-1))
df['Pmt Begin'] = pmtBegin
df['Pmt End'] = pmtEnd;

for i, cf in enumerate(swap.leg(0)):
    print '%-10s %2d  %-18s   %10.2f' % ('Fixed', i+1, cf.date(), cf.amount())


print '%-20s: %20.3f' % ('Net Present Value', swap.NPV())
swap.fairSpread()
swap.fairRate()
swap.fixedLegBPS()
swap.floatingLegBPS()
accrualFixed = notional * fixedRate * (today - Date(6,11,2015))/360.
accrualFloating = notional * 0.0062020 * (today - Date(8, 2, 2016))/360.

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


