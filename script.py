# Daily avarage of four NOAA GML Baseline observatories
# CO2 is expressed as a mole fraction in dry air, micromol/mol, abbreviated as ppm
import time
import ciso8601
import re
from contextlib import closing
import urllib.request as request

from matplotlib import pyplot as plt



# class DataPoint:
#     def __init__(self,timestamp, cycle, trend):
#         self.timestamp = timestamp
#         self.cycle = cycle
#         self.trend= trend
    
#     def __str__(self):
#         return f't: {self.timestamp}, c: {self.cycle}, t: {self.trend}'
#     def __repr__(self) -> str:
#         return self.__str__()


def get_numbers(data_string):
    return re.findall(r'\d+\.\d+|\d+',data_string)

def format_data(lines):
    return [get_numbers(bstr.decode('utf-8').replace('\n','')) for bstr in lines]

#Save ftp response to a txt file
def get_ftp_data():
    with closing(request.urlopen('ftp://aftp.cmdl.noaa.gov/products/trends/co2/co2_trend_gl.txt')) as r:
        return format_data(r.file.readlines()[60:])


def date_to_unix(date_lst):
    return time.mktime(ciso8601.parse_datetime(date_lst[0]+f'{int(date_lst[1]):02d}'+f'{int(date_lst[2]):02d}').timetuple())


def get_data():
    return [('/'.join(line[2::-1]),float(line[3]),float(line[4])) for line in get_ftp_data()]

def plot_data():
    data = get_data()

    ts,c,tr = zip(*data)
    
    fig, ax = plt.subplots()
    ax.plot(ts,c,tr)
    ax.set_xticks([0,len(ts)/2,len(ts)-1]) 

    plt.title(f'Today: {data[-1][2]} \nLast year: {data[-366][2]}',fontsize='15',color='red')
    plt.ylabel('ppm CO2 in atmosphere')
    plt.savefig('./graph.png')


if __name__=="__main__":
    get_data()
    plot_data()
    markdown = "![Graph](./graph.png)\n# A graph showing the the avarage amounts of CO2 in the atmosphere \n ##measured by four NOAA observatories based in: \n *Barrow, Alaska *Mauna Loa, Hawaii; *American Samoa;  *South Pole, Antarctica."
    open("./README.md", "w", encoding="utf-8").write(markdown)
