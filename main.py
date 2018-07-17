# coding:utf-8

import pandas as pd
import easygui as g
import numpy as np

# 参数设置
file_sign = 0   #标题行判断标志
special_list = ['具体签约时间', '本年收入贡献（万元）', '本年收入贡献（万元）（11%+6%服务金额）', \
                '产业互联网项目类型', '政企部统计签约行业', '备注', '项目编号', '总部部门', '签约部门', \
                '服务收入（万元）']

month = ['1月', '2月', '3月', '4月', '5月', '6月']

correct = {'月份': ['1月', '2月', '3月', '4月', '5月', '6月', np.NaN], \
           '新签/变更': ['新签', '变更', np.NaN], \
           '项目来源（内部/外部）': ['内部', '外部', np.NaN], \
           '行业属性（下拉可选）': ['政务', '国防军事', '环保', '金融', '医疗', '教育', \
                          '交通', '旅游', '农业', '住建业', '制造业', '其他', np.NaN], \
           '签约主体': ['集成总部', '集成分', '省地市', '集成子公司', np.NaN], \
           '实施主体': ['集成总部', '集成分', '省地市', '集成子公司', np.NaN], \
           '省份': ['广东', '河南', '山东', '江苏', '山西', '自营', '辽宁', '海南', '四川', '广西', '贵州', \
                  '天津', '黑龙江', '河北', '重庆', '浙江', '湖北', '吉林', '北京', '湖南', '福建', '新疆', \
                  '青海', '陕西', '上海', '内蒙', '安徽', '云南', '江西', '西藏', '宁夏', '甘肃', '江苏', '自营', np.NaN], \
           '项目实施方式': ['自主实施', '部分自主实施', '非自主实施', np.NaN], \
           '是否为投资类项目': ['是', '否', np.NaN], \
           '产品线属性（下拉可选）': ['系统集成服务', '软件服务', '外包服务', '专业服务', '知识服务', '设备销售', '其他服务', np.NaN], \
           }

product = {'系统集成服务': ['环保应用', '电子政务', '智能楼宇', '视频业务', '涉密集成', '弱电及综合布线', '网络集成', '智慧工地', np.NaN], \
           '软件服务': ['内部商城', '网格化产品', '移动办公', '大数据', np.NaN], \
           '外包服务': ['外包服务', np.NaN], \
           '专业服务': ['安全运维服务', '等保测评服务', '安全咨询服务', '安全培训服务', np.NaN], \
           '知识服务': ['知识服务', np.NaN], \
           '设备销售': ['设备销售', np.NaN], \
           '其他服务': ['其它', np.NaN], \
           }


#子函数is_nan：检查内容空值
def is_nan(string):
    line_num = [index + 2 + file_sign for index,each in enumerate(f[string].isnull()) if each]
    if line_num != []:
        print('错误！：',string,': 第',line_num,'行为空！')

#子函数is_repeat：检查内容是否重复
def is_repeat(string):
    line_num = [index + 2 + file_sign for index,each in enumerate(f.duplicated(string,keep = False)) if each]
    if line_num != []:
        print('错误！：',string,': 第',line_num,'行为重复值！请核实！')

#子函数is_correct：检查数据有效性
def is_correct(string):
    line_num = [index + 2 + file_sign for index,each in enumerate(f[string]) if each not in correct[string]]
    if line_num != []:
        print('错误！：',string,': 第',line_num,'内容填写错误！')

#子函数is_right：检查内容是否为空、格式是否正确
def is_right(string):
    line_num = []
    i = 0

    #检查是否为空值
    if string.find('计收') == -1 and string.find('其中') == -1 and string.find('CT') == -1:
        is_nan(string)

    #月份检查
    if string == '月份':
        #检查填写是否符合要求
        is_correct(string)
        
        #告警
        for each in f[string]:
            if each in month:
                month.remove(each)
        if month!=[]:
            print('警告！：',string,': ',month,'没有新签合同，请核实！')

    #项目名称检查
    elif string == '项目名称':

        #检查是否重复
        is_repeat(string)

    #合同额、计收检查
    elif string.find('万元') != -1:

        #检查数字格式
        try:
            f[string].astype(np.float64)
        except ValueError:
            print('错误！：',string,'：填写的内容有非数字！请核实！')

        
    #检查毛利
    elif string.find('毛利率') != -1:
        for each in f[string]:
            try:
                if float(each) > 1 or float(each) < 0:
                    line_num.append(i + 2 + file_sign)
            except ValueError:
                print('错误！：',string,'： 第',i+2,'行填写的内容非数字！请核实！')
            i += 1
        if line_num != []:
            print('错误！：',string,': 第',line_num,'毛利率大于1！')

    #新签变更、内部外部、行业属性、省份、项目实施方式检查
    elif string.find('变更') != -1 or string.find('项目来源') != -1 \
         or string.find('行业') != -1 or string.find('产品线') != -1\
         or string.find('省份') != -1 or string.find('项目实施方式') != -1\
         or string.find('是否为投资类项目') != -1 or string.find('签约主体') != -1\
         or string.find('实施主体') != -1:

        #检查数据是否有效
        is_correct(string)

    #检查产品属性与产品线对应情况
    elif string.find('产品属性') != -1:
        for each in range(row_len):
            try:
                cp = f['产品属性（下拉可选）'][each]
                cpx = f['产品线属性（下拉可选）'][each]
                if type(cp)!=str or type(cpx)!=str:
                    continue
                elif cp not in product[cpx]:
                    line_num.append(each + 2 + file_sign)
            except KeyError:
                continue
        if line_num != []:
            print('错误！: 第',line_num,'产品线属性与产品属性对应错误！请核实！')
            print("标准对应模板：")
            for each in product:
                print(each,product[each][:-1])

#主函数
if __name__ == '__main__':
    path = g.fileopenbox('Open the excel', 'EXCEL核对',filetypes=['*.xlsx','*.xls'])

    while True:
        f = pd.read_excel(path, header = file_sign, index_col = None)
        if f.columns[0] != '月份':
            file_sign += 1
        else:
            break

        if file_sign >= 10:
            print("请核实文件内容，空余行较多")
            break

    col_len = len(f.columns)
    row_len = len(f.index)

    # 去掉columns中的空格、回车
    for each in range(col_len):
        f.rename(columns={f.columns[each]: ''.join(f.columns[each].split())}, inplace=True)

    #清洗空行
    while True:
        if str(f.loc[row_len - 1]['项目名称']) == 'nan' and str(f.loc[row_len - 1]['项目编号']) == 'nan':
            f = f.drop(row_len - 1)
            row_len -= 1
        else:
            break

    # 检查内容格式
    for each in f.columns:
        if each not in special_list and each.find('Unname') == -1:
            print('------------', each, '-----------')
            is_right(each)