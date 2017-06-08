'''
    Austin Fouch
    CMPS 367 - Python Programming
    Homework #3
'''
# imported for median() function
import statistics

# class RainfallTable
class RainfallTable:
    # method __init__()
    #   initializes the RainfallTable class
    def __init__(self, filename):
        self.RainfallTable = self.load_table(filename)
    # method __init__()

    # method load_table()
    #   returns dict that contains the parsed and split input file
    def load_table(self, filename):
        years = dict()
        f = open(filename, 'r')
        for year in f:
            year_record = self.make_year_tuple(year)
            years[year_record[0]] = year_record[1]
        f.close()
        return years
    # method load_table()

    # method make_year_tuple()
    #   returns given line as a tuple
    def make_year_tuple(self, year_line):  
        tokens = year_line.split()
        year = int(tokens[0])
        rainfall = [float(x) for x in tokens[1:]]
        return (year, rainfall)
    # method make_year_tuple()

    # method get_rainfall()
    #   returns rainfall data for given month and year
    def get_rainfall(self, year, month):
        result = ()
        try:
            for key in self.RainfallTable:
                if key == year:
                    year = key
                    month = self.RainfallTable[year][month - 1]
            return month
        except IndexError:
            print("\nInvalid month/year combination, please enter a year between 1895-2014 and a month between 1-12")
    # method get_rainfall()

    # method get_average_rainfall_for_month()
    #   returns average rainfall for given month over all years
    def get_average_rainfall_for_month(self, month):
        try:
           all_years = [self.RainfallTable[y][month-1] for y in self.RainfallTable]
           return sum(all_years) / len(all_years)
        except IndexError:
            print("\nInvalid month, please enter a month between 1-12")
    # method get_average_rainfall_for_month()

    # method get_min_year()
    #   returns first year of rainfall data recording
    def get_min_year(self):
        return min(list(self.RainfallTable.keys())[:])
    # method get_min_year()

    # method get_max_year()
    #   returns last year of rainfall data recording
    def get_max_year(self):
        return max(list(self.RainfallTable.keys())[:])
    # mthod get_max_year()

    # method get_median_rainfall_for_month()
    #   returns median rainfall for given month over all years
    def get_median_rainfall_for_month(self, month):
        try:
            all_years = [self.RainfallTable[y][month-1] for y in self.RainfallTable]
            return statistics.median(all_years)
        except IndexError:
            print("\nInvalid month, please enter a month between 1-12")
    # method get_median_rainfall_for_month()

    # method get_average_rainfall_for_year()
    #   returns the average rainfall over all the months in a given year
    def get_average_rainfall_for_year(self, year):
        try:
            all_months = [self.get_rainfall(year, m) for m in range(12)]
            return sum(all_months) / len(all_months)
        except IndexError:
            print("\nInvalid year, please enter a year between 1895-2014")
    # method get_average_rainfall_for_year()

    # method get_median_rainfall_for_year()
    #   returns the median rainfall over all the months in a given year
    def get_median_rainfall_for_year(self, year):
        try:
            all_months = [self.get_rainfall(year, m) for m in range(12)]
            return statistics.median(all_months)
        except IndexError:
            print("\nInvalid year, please enter a year between 1895-2014")
    # method get_median_rainfall_for_year()

    # gnerator get_all_by_year()
    #   generator method that yields rainfall data for every month in the given year
    def get_all_by_year(self, year):
        try:
            all_months = [self.get_rainfall(year, m) for m in range(12)]
            for i in all_months:
                yield i
        except IndexError:
            print("\nInvalid year, please enter a year between 1895-2014")
     # gnerator get_all_by_year()

    # generator get_all_by_month()
    #   generator method that yields rainfall for a month over all time
    def get_all_by_month(self, month):
        try:
            all_years = [self.RainfallTable[y][month-1] for y in self.RainfallTable]
            for i in all_years:
                yield i
        except IndexError:
            print("\nInvalid month, please enter a month between 1-12")
    # generator get_all_by_month()

    # method get_droughts()
    #   returns list of drought periods
    #       a drought period is defined as at least 3 months where the rainfall 
    #       of each month is below that month's all time median rainfall
    def get_droughts(self) :
        all_droughts = []
        curr_drought = []
        drought_count = 0
        for year in range(self.get_min_year(), self.get_max_year()+1):
            for month in range(12):
                if self.get_rainfall(year, month) < (self.get_median_rainfall_for_month(month) - (self.get_median_rainfall_for_month(month) * 0.05)):
                # is drought month
                    drought_count = drought_count + 1
                    tmp = str(month+1) + "/" + str(year)
                    curr_drought.append(tmp)
                else:   
                # is not drought month
                    if drought_count >= 3: 
                    # was in a drought period
                        tmp = str(curr_drought[0]) + "-" + str(curr_drought[-1])
                        all_droughts.append(tmp)
                        drought_count = 0
                        curr_drought = []
                    else:                   
                    # was not in a drought period
                        curr_drought = []
                        drought_count = 0
        return all_droughts
    # method get_droughts()
# class RainfallTable

# Main
table = RainfallTable("njrainfall.txt")
print(table.get_rainfall(1996, 6))
print(table.get_average_rainfall_for_month(6))

for year in range(table.get_min_year(), table.get_max_year()+1) :
    print("Average rainfall in ", year, "=", table.get_average_rainfall_for_year(year))
    print("Median rainfall in ", year, "=", table.get_median_rainfall_for_year(year))
    print("="*30)
    for rain in table.get_all_by_year(year):
        print(rain, end='\t')
    print("\n", "="*30)

for month in range(1, 13) :
    print("Average rainfall in month", month, "=", table.get_average_rainfall_for_month(month))
    print("Median rainfall in month", month, "=", table.get_median_rainfall_for_month(month))
    print("="*30)
    for rain in table.get_all_by_month(month):
        print(rain, end='\t')
    print("\n", "="*30)

for d in table.get_droughts() :
    print("Drought:  ", d)
# Main