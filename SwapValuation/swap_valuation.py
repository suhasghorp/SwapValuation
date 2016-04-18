from QuantLib import *


today = Date(15, March, 2012)
settlementDate = Date(15, March, 2012)
dayCounter = Actual360()
calendar = JointCalendar(UnitedStates(), UnitedKingdom())
p3m = Period(3, Months)
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

print 'NPV LIBOR:%f' % (mvFixed - mvFRN)


