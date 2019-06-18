import matplotlib.pyplot as plt
import mpl_finance as fplt
import project_utils as utils


def calculate_williams_r(data):
    data_copy = data.copy()
    data_copy['%R'] = 0
    mask = (data_copy['Highest high'] != 0) & (data_copy['Lowest low'] != 0) & \
           ((data_copy['Highest high'] - data_copy['Lowest low']) != 0)
    data_copy.loc[mask, '%R'] = (data_copy['Highest high'] - data_copy['Close']) / \
                                (data_copy['Highest high'] - data_copy['Lowest low']) * -100
    return data_copy


def williams_r(data, period):
    data_copy = data.copy()
    data_copy['Highest high'] = utils.get_highest_highs(data, period)['Highest high']
    data_copy['Lowest low'] = utils.get_lowest_lows(data, period)['Lowest low']
    return calculate_williams_r(data_copy)


def test_indicator(file_name, start_date, end_date, figure_title, candlestick_width):
    csv_data = utils.load_data(file_name, "%Y.%m.%d %H:%M:%S")

    # print("Sample data:")
    # print(csv_data.head(10))

    plot_data = williams_r(csv_data, 14)

    # print("")
    # print(plot_data.tail(20))

    subplot_df1 = plot_data.drop(['Volume', '%R', 'Highest high', 'Lowest low'], 1).loc[start_date:end_date]
    subplot_df2 = plot_data['%R'].loc[start_date:end_date]

    df1_tuples = utils.candlestick_tuples(subplot_df1)
    subplot_df2 = utils.reset_date_index(subplot_df2)

    # subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='col')

    # fig.set_size_inches(8, 8)
    ax1.xaxis_date()
    # ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax1.set_title(figure_title)
    for tick in ax1.get_xticklabels():
        tick.set_rotation(45)
    ax1.grid()
    fplt.candlestick_ochl(ax1, df1_tuples, width=candlestick_width, colorup='g', colordown='r')

    subplot_df2.plot(ax=ax2)
    for tick in ax2.get_xticklabels():
        tick.set_rotation(90)
    ax2.grid(which='minor', linestyle='--')
    ax2.grid(which='major', linestyle='-')
    fig.subplots_adjust(hspace=0.0)
    fig.show()
    plt.close()