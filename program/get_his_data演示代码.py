from Function_fin import get_his_data
from Config import finance_data_path
import pandas as pd

pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

df = pd.read_csv(finance_data_path + '/sh600000/sh600000_商业银行.csv', encoding='gbk', skiprows=1,
                 parse_dates=['publish_date', 'report_date'],
                 usecols=['publish_date', 'report_date', 'B_central_bank_cash_and_deposit@xbx', 'B_interbank_storage@xbx'])
df, columns_ = get_his_data(df, ['B_central_bank_cash_and_deposit@xbx', 'B_interbank_storage@xbx'], span='q')

print(df)
print(columns_)
