# -*- coding: utf-8 -*-
# @Author: wow00
# @Date:   2017-08-29 19:29:02
# @Last Modified by:   wow00
# @Last Modified time: 2017-08-29 19:37:37

# coding:utf-8
# @Author:bianxuesheng

from numpy import *
from pandas import *

if __name__ == '__main__':
    data = read_csv('消费记录.csv')
    students = {}
    out = {}
    index = 0
    for i in range(data.shape[0]):
        students.setdefault(data.iloc[i, index], -1)
        students[data.iloc[i, index]] += 1
        out.setdefault(data.iloc[i, index],
                       pandas.DataFrame(columns=data.columns))
        out[data.iloc[i, index]].loc[
            students[data.iloc[i, index]]] = data.loc[i]

    out = list(out.values())
    count = 0
    for i in out:
        count += 1
        i.to_csv('./split_data/' + str(count) + '.csv')
