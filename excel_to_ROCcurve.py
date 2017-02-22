#
# エクセルファイルよりROCカーブを算出
# 有料ソフトがライセンス切れしたのを期に作った
# 探したけどこのよなのは無かった
# 
# by namuyan
# 
# ver 0.01


import argparse
import math
import xlrd
import xlwt
import numpy as np
#import pprint as pp


def main(inputf, index=0):
    # Open excel file
    print("# open ", inputf)
    book = xlrd.open_workbook(inputf)
    print("# sheet: ", book.nsheets)
    print("# sheet name:")
    i = 0
    for n in book.sheet_names():
        print("# index=",i ,":name=", n)
        i += 1
    print("#    select index -> ", index)
    sheet = book.sheet_by_index(index)
    print("")

    # 前処理
    data_array = np.array(sheet._cell_values)
    #pp.pprint(data_array)

    # 本処理
    n_ndim = data_array.shape
    n_ndim = n_ndim[1]
    print("# dimentions: ", n_ndim / 2)
    roc_curve_sum = np.array([])
    for q in range(0, n_ndim, 2):
        print("# dim: ", data_array[0][q])
        n_float = q
        n_int = q + 1
        result = get_roc_element(data_array, n_float=n_float, n_int=n_int)
        roc_curve = np.array([[data_array[0][q], ""],["", ""]], dtype=np.float32) #1
        roc_curve = np.concatenate((roc_curve, [["FP rate", "TP rate"]]), axis=0) #2
        for p in result:
            TP = p[1]
            FP = p[2]
            TN = p[3]
            FN = p[4]
            try:
                roc_curve = np.concatenate((roc_curve, [[FP / (FP + FN), TP / (TP + TN)]]), axis=0)
            except:
                #print("# Error: divide by zero.")
                print("TP FP TN FN:", p)
        #pp.pprint(roc_curve)
        auc = 0
        for r in range(len(result)):
            try:
                auc += math.fabs(float(roc_curve[r + 3, 0]) - float(roc_curve[r + 4, 0])) * float(roc_curve[r + 3, 1])
            except:
                roc_curve[1, 0] = round(auc * 100, 2)
                #print("# AUC ", auc)
                break
        if q == 0:
            roc_curve_sum = roc_curve
        else:
            roc_curve_sum = np.concatenate((roc_curve_sum, roc_curve), axis=1)

    # 書き込み
    write2xls(inputf, roc_curve_sum)
    print("# ")


def write2xls(fname, data):
    write_name = fname + ".result.xls"
    print("# Write")
    book = xlwt.Workbook(write_name)
    newSheet = book.add_sheet('result')
    for p in range(0, len(data) - 1):
        # p行、q列目にデータを書き込み
        for q in range(0, len(data[p]) ):
            newSheet.write(p, q, data[p][q])
    book.save(write_name)

def get_roc_element(data_array, n_range=500, n_float=0, n_int=1):
    result = []
    for sensitive in range(0, n_range):
        sensitive /= n_range
        TP = 0
        FP = 0
        TN = 0
        FN = 0
        for p in data_array:
            try:
                d_float = float(p[n_float])
                d_label = int(float(p[n_int]))
                if d_float >= sensitive and d_label == 1:# TP
                    TP += 1
                elif d_float >= sensitive and d_label != 1:# FP
                    FP += 1
                elif d_float < sensitive and d_label == 1:  # TN
                    TN += 1
                elif d_float < sensitive and d_label != 1:  # FN
                    FN += 1
            except:
                continue
        result.append([sensitive, TP, FP, TN, FN])
    #pp.pprint(result)
    return result

if __name__ == '__main__':
    # コマンドライン引数
    parser = argparse.ArgumentParser(description='python3 ROCcurve.py [option]')
    parser.add_argument('--input', '-i', type=str, default="", help='入力ファイル')
    parser.add_argument('--index', '-x', type=int, default=0, help='sheet index')
    args = parser.parse_args()
    main(args.input, args.index)

