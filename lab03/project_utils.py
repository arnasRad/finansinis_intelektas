import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from matplotlib.ticker import FuncFormatter


def get_lowest_lows(data, period):
    data_copy = data.copy()
    data_copy['Lowest low'] = 0
    hh_index = period
    for i in range(period, len(data_copy.index)):
        min_value = data.iloc[i-period+1:i+1].min()['Low']
        data_copy.iloc[hh_index, data_copy.columns.get_loc('Lowest low')] = min_value
        hh_index += 1
    return data_copy


def get_highest_highs(data, period):
    data_copy = data.copy()
    data_copy['Highest high'] = 0
    hh_index = period
    for i in range(period, len(data_copy.index)):
        max_value = data.iloc[i-period+1:i+1].max()['High']
        data_copy.iloc[hh_index, data_copy.columns.get_loc('Highest high')] = max_value
        hh_index += 1
    return data_copy


def money_flow_multiplier(close, low, high):
    return ((close - low) - (high - close)) / (high - low)


def money_flow_volume(mfm, volume):
    return mfm * volume


def candlestick_tuples(data):
    data_copy = data.copy()
    data_copy = data_copy.reset_index()
    data_copy['Date'] = data_copy['Time'].apply(lambda d: mdates.date2num(d.to_pydatetime()))
    return [tuple(x) for x in data_copy[['Date', 'Open', 'Close', 'Low', 'High']].values]


def reset_date_index(data):
    data_copy = data.copy()
    data_copy = data_copy.reset_index()
    data_copy['Date'] = data_copy['Time'].apply(lambda d: mdates.date2num(d.to_pydatetime()))
    data_copy = data_copy.drop(['Time'], 1)
    data_copy = data_copy.set_index('Date')
    return data_copy


# period_sum = data.iloc[i - period + 1:i + 1].sum()
def period_average(data, index, period):
    return data.iloc[index - period + 1: index + 1].sum() / period


def load_data(file_name, date_format):
    csv_data = pd.read_csv(file_name)
    csv_data['Time'] = pd.to_datetime(csv_data['Time'], format=date_format)
    csv_data = csv_data.set_index('Time')
    csv_data = csv_data.iloc[::-1]
    return csv_data


def equidate_ax(fig, ax, dates, fmt="%Y-%m-%d", label="Date"):
    """
    Sets all relevant parameters for an equidistant date-x-axis.
    Tick Locators are not affected (set automatically)

    Args:
        fig: pyplot.figure instance
        ax: pyplot.axis instance (target axis)
        dates: iterable of datetime.date or datetime.datetime instances
        fmt: Display format of dates
        label: x-axis label
    Returns:
        None

    """
    N = len(dates)

    def format_date(index, pos):
        index = np.clip(int(index + 0.5), 0, N - 1)
        return dates[index].strftime(fmt)

    ax.xaxis.set_major_formatter(FuncFormatter(format_date))
    ax.set_xlabel(label)
    fig.autofmt_xdate()