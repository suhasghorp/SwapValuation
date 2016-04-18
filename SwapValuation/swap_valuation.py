from QuantLib import *
from pandas import *


calendar = JointCalendar(UnitedStates(UnitedStates.Settlement), UnitedKingdom(UnitedKingdom.Exchange),JoinHolidays)
calendar.addHoliday(Date(5,6,2012)) # Add Queens Jubilee Holiday
settlementDate = Date(6, May, 2014)
today = Date(15, April, 2016)
Settings.instance().evaluationDate = today

liborCurveDates = [today,
            Date(18,4,2016),
            Date(19,4,2016),
            Date(26,4,2016),
            Date(19,7,2016),
            Date(15,9,2016),
            Date(21,12,2016),
            Date(21,3,2017),
            Date(19,4,2017),
            Date(15,6,2017),
            Date(21,9,2017),
            Date(20,12,2017),
            Date(20,3,2018),
            Date(19,4,2018),
            Date(21,6,2018),
            Date(19,4,2019),
            Date(20,4,2020),
            Date(19,4,2021),
            Date(19,4,2022),
            Date(19,4,2023),
            Date(19,4,2024),
            Date(21,4,2025),
            Date(20,4,2026),
            Date(19,4,2028),
            Date(21,4,2031),
            Date(21,4,2036),
            Date(19,4,2041),
            Date(19,4,2046),
            Date(19,4,2056),
            Date(19,4,2066),
            Date(20,4,2076)
            ]

liborDiscFactors = [1.0,
                    0.99996828,
                    0.9999577,
                    0.99987964,
                    0.99835999,
                    0.9972,
                    0.9952,
                    0.9932,
                    0.99246553,
                    0.9911,
                    0.9886,
                    0.9863,
                    0.9838,
                    0.98289194,
                    0.9811,
                    0.97168339,
                    0.95841622,
                    0.94335344,
                    0.9263031,
                    0.90821659,
                    0.8891654,
                    0.86961426,
                    0.84990119,
                    0.8096009,
                    0.75166592,
                    0.66384082,
                    0.58916339,
                    0.52361497,
                    0.42087197,
                    0.34432198,
                    0.28166425
                    ]

oisCurveDates = [today, Date(19, 5, 2016), Date(20, 6, 2016), Date(19, 7, 2016), Date(19, 8, 2016), Date(19, 9, 2016),
                 Date(19, 10, 2016), Date(19, 1, 2017), Date(19, 4, 2017), Date(19, 11, 2017),
                 Date(19, 4, 2018), Date(19, 4, 2019), Date(20, 4, 2020), Date(19, 4, 2021),
                 Date(19, 4, 2023), Date(20, 4, 2026), Date(19, 4, 2028), Date(21, 4, 2031),
                 Date(21, 4, 2036), Date(19, 4, 2041), Date(19, 4, 2046), Date(19, 4, 2056), Date(19, 4, 2066)]

oisDiscFactors = [1.0, 0.99965897, 0.99932719, 0.99900473, 0.99864067, 0.99826878, 0.99787826, 0.99660892, 0.99525069, 0.99216604,
                  0.98876614, 0.98055096, 0.97049654, 0.95864420, 0.92981876, 0.88031097, 0.84570871, 0.79365875, 0.71413756,
                  0.64512344, 0.58506043, 0.48754892, 0.41305758]


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

df = DataFrame()

pmtDates = [settlementDate]
pmt = []
for i, cf in enumerate(swap.leg(1)):
    print '%-10s %2d  %-18s   %10.2f' % ('Floating', i+1, cf.date(), cf.amount())
    pmtDates.append(cf.date)
    pmt.append(cf.amount)



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


