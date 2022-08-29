"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx9585

选股使用的过滤的脚本
"""
# !!!


from Config import *

['交易日期', '股票代码', '股票名称', '是否交易', '开盘价', '最高价', '最低价', '收盘价', '成交额',
       '流通市值', '总市值', '成交量', '上市至今交易天数', '申万一级行业名称', '下日_是否交易', '下日_开盘涨停',
       '下日_是否ST', '下日_是否S', '下日_是否退市', '下日_开盘买入涨跌幅', 'VWAP', '换手率', '5日均线',
       'bias', '5日累计涨跌幅', 'B_st_borrow@xbx', 'B_lt_loan@xbx',
       'B_bond_payable@xbx', 'B_noncurrent_liab_due_in1y@xbx',
       'R_operating_total_revenue@xbx', 'B_interest_payable@xbx',
       'B_charge_and_commi_payable@xbx', 'R_sales_fee@xbx', 'R_manage_fee@xbx',
       'R_rad_cost_sum@xbx', 'R_asset_impairment_loss@xbx',
       'C_depreciation_etc@xbx', 'C_intangible_assets_amortized@xbx',
       'C_lt_deferred_expenses_amrtzt@xbx', 'R_other_compre_income@xbx',
       'R_operating_taxes_and_surcharge@xbx', 'R_operating_cost@xbx',
       'R_np_atoopc@xbx', 'B_total_equity_atoopc@xbx', 'B_currency_fund@xbx',
       'B_total_current_liab@xbx', 'B_total_noncurrent_liab@xbx',
       'C_ncf_from_oa@xbx', 'R_np@xbx', 'R_operating_total_cost@xbx',
       'R_income_tax_cost@xbx', 'R_total_profit@xbx', 'C_ncf_from_oa_im@xbx',
       '归母PE(ttm)', '归母ROE(ttm)', '毛利率(ttm)', '企业倍数', '现金流负债比', '净利润现金含量',
       '申万二级行业名称', '涨跌幅', '下周期每天涨跌幅', '下周期涨跌幅', '归母EP(ttm)',
       '归母PE(ttm)_二级行业分位数', '归母PE(ttm)_分位数', '企业倍数_倒数', '企业倍数_分位数',
       '现金流负债比_分位数', '管理占净利润比', '管理占净利润比_分位数'],

def filter_and_rank(df, par):
    """
    通过财务因子设置过滤条件
    :param df: 原始数据
    :return: 返回 通过财务因子过滤并叠加量价因子的df
    """
    # ======根据各类条件对股票进行筛选

    # 计算归母PE(ttm) 在二级行业的分位数
    # 获取归母PE(ttm) 较小 的股票
    # 归母PE(ttm)会存在负数的情况 => 先求倒数，再从大到小排序
    df['归母EP(ttm)'] = 1 / df['归母PE(ttm)']
    df['归母PE(ttm)_二级行业分位数'] = df.groupby(['交易日期', '申万二级行业名称'])['归母EP(ttm)'].rank(ascending=False, pct=True)
    condition = (df['归母PE(ttm)_二级行业分位数'] <= 0.4)

    # 计算归母PE(ttm) 在所有股票的分位数
    # 获取归母PE(ttm) 较小的股票
    # 归母PE(ttm)会存在负数的情况 => 复用之前 PE(ttm) 的倒数 EP(ttm),再从大到小排序
    df['归母PE(ttm)_分位数'] = df.groupby(['交易日期'])['归母EP(ttm)'].rank(ascending=False, pct=True)
    condition &= (df['归母PE(ttm)_分位数'] > 0.1)
    condition &= (df['归母PE(ttm)_分位数'] <= 0.4)

    # 计算企业倍数 在所有股票的分位数
    # 获取企业倍数 较小 的股票
    # 企业倍数存在负数的情况 => 先求倒数，再从大到小排序
    df['企业倍数_倒数'] = 1 / df['企业倍数']
    df['企业倍数_分位数'] = df.groupby(['交易日期'])['企业倍数_倒数'].rank(ascending=False, pct=True)
    condition &= (df['企业倍数_分位数'] <= 0.4)

    # 计算现金流负债比 在所有股票的分位数
    # 获取现金流负债比 较大 的股票
    df['现金流负债比_分位数'] = df.groupby(['交易日期'])['现金流负债比'].rank(ascending=False, pct=True)
    condition &= (df['现金流负债比_分位数'] <= 0.4)
    df['管理占净利润比'] = df['R_np@xbx']/(df['R_sales_fee@xbx'])

    df['管理占净利润比_分位数'] =df.groupby(['交易日期', '申万二级行业名称'])['管理占净利润比'].rank(ascending=False, pct=True)
    # condition &= (df['管理占净利润比_分位数'] > 0.32)
    # condition &= (df['管理占净利润比_分位数'] < 0.54)
    condition &= (df['管理占净利润比_分位数'] > par[0])
    condition &= (df['管理占净利润比_分位数'] < par[1])
    condition &=  (df['换手率']>0.02)

    df['管理占净利润比'] = df['R_np@xbx']/df['R_manage_fee@xbx']

    
    df['非流动负债净利润比'] = 1/df['C_ncf_from_oa@xbx']/df['R_np@xbx']
    df['非流动负债净利润比'] =df.groupby(['交易日期', '申万二级行业名称'])['非流动负债净利润比'].rank(ascending=False, pct=True)
    # condition &= (df['非流动负债净利润比'] > par[0])
    # condition &= (df['非流动负债净利润比'] < par[1])

    # df['调试参数'] = 1/df[em]/df['R_np@xbx']
    # df['调试参数'] =df.groupby(['交易日期', '申万二级行业名称'])['调试参数'].rank(ascending=False, pct=True)
    # condition &= (df['调试参数'] > par[0])
    # condition &= (df['调试参数'] < par[1])
    condition &=  (df['换手率']>0.02)
    
    
    # 综上所有财务因子的过滤条件，选股
    df = df[condition]


    # 定义需要进行rank的因子
    factors_rank_dict = {
        '总市值': True,
        '归母ROE(ttm)': False,
        # 'B_bond_payable@xbx':False
    }
    # 定义合并需要的list
    merge_factor_list = []
    # 遍历factors_rank_dict进行排序
    for factor in factors_rank_dict:
        df[factor + '_rank'] = df.groupby('交易日期')[factor].rank(ascending=factors_rank_dict[factor], method='first')
        # 将计算好的因子rank添加到list中
        merge_factor_list.append(factor + '_rank')

    # 对量价因子进行等权合并，生成新的因子
    df['因子'] = df[merge_factor_list].mean(axis=1)
    # 对因子进行排名
    df['排名'] = df.groupby('交易日期')['因子'].rank(method='first')

    # 选取排名靠前的股票
    df = df[df['排名'] <= select_stock_num]

    return df

# !!!
