import math

def uniqueYearCalculator (data):
    uniqueYear = set()
    for date in data['Date'].unique():
        if type(date) == float and not math.isnan(date):
            uniqueYear.add(int(date))
        elif type(date) == str and date[-4:].isdigit():
            uniqueYear.add(int(date[-4:]))
    return sorted(uniqueYear)
