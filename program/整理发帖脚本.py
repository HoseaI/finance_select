"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx9585

财务数据选股专属代码

发帖脚本
"""
import pandas as pd
import re

from Config import *

p = re.compile(r'# !!!(.*)# !!!', re.S)


def read_file(path):
    with open(path, 'r', encoding='utf8') as f:
        content = f.read()
        res = p.findall(content)
        return res[0].strip()


def write_file(content):
    with open(root_path + '/program/发帖脚本/发帖文件.md', 'w', encoding='utf8') as f:
        f.write(content)


# 读取config文件
config_str = read_file(root_path + '/program/Config.py')

# 读取CalcFactor文件
factor_str = read_file(root_path + '/program/CalcFactor.py')

# 读取Filter文件
filter_str = read_file(root_path + '/program/Filter.py')

# 策略回测表现
rtn = pd.read_csv(root_path + '/data/output/策略结果/策略评价_%s.csv' % period_type, encoding='gbk')
rtn.columns = ['指标', '表现']
rtn_str = rtn.to_markdown(index=False)

# 年度同期表现
year_rtn = pd.read_csv(root_path + '/data/output/策略结果/策略评价_year_%s.csv' % period_type, encoding='gbk')
year_rtn.columns = ['交易日期', '策略收益', '指数收益', '超额收益']
year_rtn_str = year_rtn.to_markdown(index=False)

with open(root_path + '/program/发帖脚本/发帖模板.md', 'r', encoding='utf8') as file:
    template = file.read()
    template = template % (config_str, factor_str, filter_str, rtn_str, year_rtn_str)
    print(template)
    write_file(template)
