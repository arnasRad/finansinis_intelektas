import matplotlib.dates as mdates


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
    date_copy = data.copy()
    date_copy = date_copy.reset_index()
    date_copy['Date'] = date_copy['Time'].apply(lambda d: mdates.date2num(d.to_pydatetime()))
    return [tuple(x) for x in date_copy[['Date', 'Open', 'Close', 'Low', 'High']].values]


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
