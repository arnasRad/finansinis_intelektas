import matplotlib.pyplot as plt
import pandas as pd
import mpl_finance as fplt
import project_utils as utils

# >> NOTE: import from web
# import pandas.io.data as web
#
# df = web.DataReader("aapl", 'yahoo', datetime(2008, 8, 15), datetime(2008, 10, 15))
# <<


def accumulation_distribution_line(data):
    mfm = utils.money_flow_multiplier(data['Close'],
                                data['Low'],
                                data['High'])

    mfv = utils.money_flow_volume(mfm, data['Volume'])
    return mfv.cumsum()


def test_indicator(file_name, start_date, end_date, figure_title, candlestick_width):
    date_format = "%Y.%m.%d %H:%M:%S"
    csv_data = pd.read_csv(file_name)
    csv_data['Time'] = pd.to_datetime(csv_data['Time'], format=date_format)
    csv_data = csv_data.set_index('Time')
    csv_data = csv_data.iloc[::-1]

    print("Sample data:")
    print(csv_data.head(10))

    plot_data = csv_data.copy()

    plot_data['ADL'] = accumulation_distribution_line(plot_data)

    print(plot_data.tail(10))

    subplot_df1 = plot_data.drop(['Volume', 'ADL'], 1).loc[start_date:end_date]
    subplot_df2 = plot_data['ADL'].loc[start_date:end_date]

    df1_tuples = utils.candlestick_tuples(subplot_df1)
    subplot_df2 = utils.reset_date_index(subplot_df2)

    # subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex='col')

    ax1.xaxis_date()
    ax1.set_title(figure_title)
    # for tick in ax1.get_xticklabels():
    #     tick.set_rotation(45)
    ax1.grid()
    fplt.candlestick_ochl(ax1, df1_tuples, width=candlestick_width, colorup='g', colordown='r')

    subplot_df2.plot(ax=ax2)
    for tick in ax2.get_xticklabels():
        tick.set_rotation(45)
    ax2.grid(which='minor', linestyle='--')
    ax2.grid(which='major', linestyle='-')
    fig.subplots_adjust(hspace=0.0)
    fig.show()
    plt.close()
