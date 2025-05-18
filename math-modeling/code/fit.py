import numpy as np
from scipy.optimize import curve_fit

year = 2010

def growth_curve(x, a, b, c):
    return a * x**2 + b * x + c

years = np.array([2007, 2009, 2015, 2016, 2019])
capacities = np.array([8, 15, 55, 60, 82])

params, _ = curve_fit(growth_curve, years, capacities)
capacity = growth_curve(year, *params)

print(f"{capacity:.2f} million tons in {year}")