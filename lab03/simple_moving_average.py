import project_utils as utils
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as fplt


def simple_moving_average(data, period):
    data_copy = data.copy()
    data_copy = data_copy.to_frame()
    data_copy['SMA'] = 0
    for i in range(period, len(data_copy.index)):
        data_copy.iloc[i, data_copy.columns.get_loc('SMA')] = \
            utils.period_average(data, i, period)
    return data_copy['SMA']


def test_indicator(file_name, start_date, end_date, figure_title, candlestick_width):
    csv_data = utils.load_data(file_name, "%Y.%m.%d %H:%M:%S")

    plot_data = csv_data.copy()

    print('Sample data:')
    plot_data['SMA'] = simple_moving_average(plot_data['Close'], 10)

    print(plot_data.tail(20))

    subplot_df1 = plot_data.drop(['Volume', 'SMA'], 1).loc[start_date:end_date]
    subplot_df2 = plot_data['SMA'].loc[start_date:end_date]

    df1_tuples = utils.candlestick_tuples(subplot_df1)

    fig, ax = plt.subplots()
    plt.xticks(rotation=45)
    plt.title(figure_title)

    fplt.candlestick_ochl(ax, df1_tuples, width=candlestick_width, colorup='g', colordown='r')
    subplot_df2.plot(ax=ax)

    plt.show()


m1_file_name = 'eurusd_m1_data.csv'
h1_file_name = 'eurusd_h1_data.csv'

start_date_h1 = '2019.3.25'
end_date_h1 = '2019.3.26'

end_date_m1 = '2019.3.25 01:30:00'
start_date_m1 = '2019.3.25 00:00:00'

figure_title_m1 = 'Minute OHLC  data'
figure_title_h1 = 'Hourly OHLC  data'

width_m1 = 0.0004
width_h1 = 0.02

# test_indicator(m1_file_name, start_date_m1, end_date_m1, figure_title_m1, width_m1)
# test_indicator(h1_file_name, start_date_h1, end_date_h1, figure_title_h1, width_h1)
