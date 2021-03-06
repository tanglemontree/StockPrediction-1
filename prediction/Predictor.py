#! /usr/bin/env python3
# -*- coding: utf-8 -*-


import sys

import numpy as np
import pandas as pd
from sklearn import cross_validation as cv


class Predictor:
    def __init__(self, clf):
        self.clf = clf

    def prediction(self, file_name, samples):
        # ファイルを読むのです
        date_, adj_end = self.load_data(file_name)

        # pandas.Series に変換するのです
        adj_end = self.convert_data(adj_end)

        # 学習データを作るのです。
        train_x, train_y = self.create_train_data(adj_end, samples)

        # 交差検証するのです。
        score = self.verify(train_x, train_y)

        # 学習して予測するのです!!
        self.clf.fit(train_x, train_y)
        last_data = adj_end.ix[len(adj_end) - samples - 1:len(adj_end)].values
        return self.clf.predict([last_data])[0], score

    # ファイルを読み込むのです
    def load_data(self, file_name):
        lines = [line[:-1] for line in open(file_name, 'r', encoding='utf-8')]
        split = [line.split('\t') for line in lines if
                 not (line.startswith('#') or len(line) == 0)]
        return [line[0] for line in split], [float(line[6]) for line in split]

    # pandas.Series に変換するのです
    def convert_data(self, values):
        returns = pd.Series(values).pct_change()  # 騰落率を出すのです
        ret_index = (1 + returns).cumprod()  # 累積積を出すのです。
        ret_index[0] = 1.0  # 最初の値は 1 なのです。
        return ret_index

    # 学習データを作るのです。
    def create_train_data(self, arr, samples):
        train_x = []
        train_y = []
        # サンプルのデータを学習、 1 サンプルずつ後ろにずらしていく
        for i in np.arange(0, len(arr) - samples - 1):
            s = i + samples  # samplesサンプル間の変化を素性にする
            feature = arr.ix[i:s]
            if feature[s - 1] < arr[s]:
                # 上がった
                train_y.append(1)
            else:
                # 上がらなかった
                train_y.append(0)
            train_x.append(feature.values)

        # 上げ下げの結果と教師データのセットを返す
        return np.array(train_x), np.array(train_y)

    def verify(self, train_x, train_y):
        x, t_x, y, t_y = cv.train_test_split(train_x, train_y, test_size=0.2)
        self.clf.fit(x, y)
        return self.clf.score(t_x, t_y)


if __name__ == '__main__':
    from sklearn import linear_model as lm
    from sklearn import tree
    from sklearn import svm

    if len(sys.argv) != 3:
        print("USAGE: DecisionTree.py [FILE] [SPAN]")
        exit()

    file_name_ = sys.argv[1]
    samples_ = int(sys.argv[2])

    pred = Predictor(lm.SGDClassifier())
    result_, score_ = pred.prediction(file_name_, samples_)
    print(file_name_, "score:", score_, "上がるぞぉぉぉ" if result_ == 1 else "下がるぞぉぉぉ")

    pred = Predictor(tree.DecisionTreeClassifier())
    result_, score_ = pred.prediction(file_name_, samples_)
    print(file_name_, "score:", score_, "上がるぞぉぉぉ" if result_ == 1 else "下がるぞぉぉぉ")

    pred = Predictor(svm.SVC())
    result_, score_ = pred.prediction(file_name_, samples_)
    print(file_name_, "score:", score_, "上がるぞぉぉぉ" if result_ == 1 else "下がるぞぉぉぉ")
