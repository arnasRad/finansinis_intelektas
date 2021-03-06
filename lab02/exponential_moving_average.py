import project_utils as utils
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as fplt


def exponential_moving_average(data, period):
    data_copy = data.copy()
    data_copy = data_copy.to_frame()
    data_copy['EMA'] = 0
    data_copy.iloc[period - 1, data_copy.columns.get_loc('EMA')] = \
        utils.period_average(data, period - 1, period)
    multiplier = (2 / (period + 1))
    for i in range(period, len(data_copy.index)):
        previous_ema = data_copy.iloc[i - 1, data_copy.columns.get_loc('EMA')]
        data_value = data_copy.iloc[i].drop('EMA').values[0]
        data_copy.iloc[i, data_copy.columns.get_loc('EMA')] = (data_value - previous_ema) * multiplier + previous_ema
    return data_copy['EMA']


def test_indicator(file_name, start_date, end_date, figure_title, candlestick_width):
    date_format = "%Y.%m.%d %H:%M:%S"
    csv_data = pd.read_csv(file_name)
    csv_data['Time'] = pd.to_datetime(csv_data['Time'], format=date_format)
    csv_data = csv_data.set_index('Time')
    csv_data = csv_data.iloc[::-1]

    plot_data = csv_data.copy()

    print('Sample data:')
    plot_data['EMA'] = exponential_moving_average(plot_data['Close'], 10)

    print(plot_data.tail(10))

    subplot_df1 = plot_data.drop(['Volume', 'EMA'], 1).loc[start_date:end_date]
    subplot_df2 = plot_data['EMA'].loc[start_date:end_date]

    df1_tuples = utils.candlestick_tuples(subplot_df1)

    fig, ax = plt.subplots()
    plt.xticks(rotation=45)
    plt.title(figure_title)

    fplt.candlestick_ochl(ax, df1_tuples, width=candlestick_width, colorup='g', colordown='r')
    subplot_df2.plot(ax=ax)

    plt.show()
