import simple_moving_average as sma
import exponential_moving_average as ema
import accumulation_distribution_line as acl
import Williams_R as willR
import chaikin_oscillator as cho

m1_file_name = 'eurusd_m1_data.csv'
h1_file_name = 'eurusd_h1_data.csv'
d1_file_name = 'eurusd_d1_data.csv'

end_date_m1 = '2019.3.25 01:30:00'
start_date_m1 = '2019.3.25 00:00:00'

start_date_h1 = '2019.3.25'
end_date_h1 = '2019.3.26'

start_date_d1 = '2019.2.15'
end_date_d1 = '2019.4.07'

figure_title_m1 = 'Minute OHLC  data'
figure_title_h1 = 'Hourly OHLC  data'
figure_title_d1 = 'Daily OHLC  data'

width_m1 = 0.0004
width_h1 = 0.02
width_d1 = 0.5

sma.test_indicator(m1_file_name, start_date_m1, end_date_m1, figure_title_m1, width_m1)
# sma.test_indicator(h1_file_name, start_date_h1, end_date_h1, figure_title_h1, width_h1)
# sma.test_indicator(d1_file_name, start_date_d1, end_date_d1, figure_title_d1, width_d1)
#
ema.test_indicator(m1_file_name, start_date_m1, end_date_m1, figure_title_m1, width_m1)
# ema.test_indicator(h1_file_name, start_date_h1, end_date_h1, figure_title_h1, width_h1)
# ema.test_indicator(d1_file_name, start_date_d1, end_date_d1, figure_title_d1, width_d1)
#
acl.test_indicator(m1_file_name, start_date_m1, end_date_m1, figure_title_m1, width_m1)
# acl.test_indicator(h1_file_name, start_date_h1, end_date_h1, figure_title_h1, width_h1)
# acl.test_indicator(d1_file_name, start_date_d1, end_date_d1, figure_title_d1, width_d1)
#
willR.test_indicator(m1_file_name, start_date_m1, end_date_m1, figure_title_m1, width_m1)
# willR.test_indicator(h1_file_name, start_date_h1, end_date_h1, figure_title_h1, width_h1)
# willR.test_indicator(d1_file_name, start_date_d1, end_date_d1, figure_title_d1, width_d1)
#
cho.test_indicator(m1_file_name, start_date_m1, end_date_m1, figure_title_m1, width_m1)
# cho.test_indicator(h1_file_name, start_date_h1, end_date_h1, figure_title_h1, width_h1)
# cho.test_indicator(d1_file_name, start_date_d1, end_date_d1, figure_title_d1, width_d1)
