# -*- encoding: utf-8 -*-
from __future__ import division, print_function
import numpy as np
import random
import math
from itertools import chain


# セッティングを関数化
def settings(m, n):
    # 受験者(=proposer)の人数(m), 大学(=respondent ?)の数(n)

    # 受験者, 大学のリスト
    props = list(range((m)))
    resps = list(range((n)))

    # 受験者と大学の選好表を作成
    prop_choice = list(range((n+1)))
    resp_choice = list(range((m+1)))
    prop_prefs = [random.sample(prop_choice, n+1) for i in props]
    resp_prefs = [random.sample(resp_choice, m+1) for i in resps]

    # 大学の収容可能人数を(0 〜 proposerの総人数 までの範囲で適当に決める)
    caps = list(range((n)))
    for i in caps:
        caps[i]=random.randint(0, m)

    return prop_prefs, resp_prefs, caps


def array_to_dict(array):
    dict = {}
    for x, y in enumerate(array):
        dict[x] = list(y)
    return dict


def deferred_acceptance(prop_prefs, resp_prefs, caps=None):
    # 選好表を辞書に変換
    props = array_to_dict(prop_prefs)
    resps = array_to_dict(resp_prefs)

    # 選好表の行数、列数をチェック（それぞれの選好表毎の行数・列数は揃っていると信じる）
    prop_row = len(prop_prefs)
    prop_col = len(prop_prefs[0])
    resp_row = len(resp_prefs)
    resp_col = len(resp_prefs[0])

    # 受験者、大学の数を代入（アンマッチ・マークは含まない数）
    prop_size = prop_row
    resp_size = resp_row

    if (prop_row != resp_col - 1) or (resp_row != prop_col - 1):
        print("2つの選好表の行列数が不適切です")
        exit(-1)

    # アンマッチ・マーク（これよりも選好表の後ろ側にいる大学には入らない！というマーク）
    # は、選好表の1列の中で一番大きな数字を採用（m列なら、配列は0から始まるので、m-1がアンマッチ・マーク）
    prop_unmatched_mark = prop_col - 1
    resp_unmatched_mark = resp_col - 1

    # capsが空なら、入学定員は全て1にする
    if caps is None:
        non_caps_flag = True
        caps = np.ones(resp_size, dtype=int)

    else:
        non_caps_flag = False

    # 受験者側をkeyとしたマッチングリストだけだと辛いので、大学側をkeyとしたマッチングリストも作りましょう
    # prop_matchesは、受験者をkey、大学をvalueとした、{prop1: resp3, prop2: resp1,...} という辞書。
    # resp_matchesは、大学をkey、受験者（のリスト）をvalueとした、{resp1: [prop0, prop2, prop3,...], ...}という辞書。
    # 最初はそれぞれ空文字をいれておく。未マッチングの場合はアンマッチ・マークが入る。
    prop_matches = {}
    resp_matches = {}
    for i in range(prop_size):
        prop_matches[i] = ""

    for i in range(resp_size):
        resp_matches[i] = []

    # 未処理の受験者の集合（初期状態では、全ての受験者）
    # 入学先が見つかるか、行きたい大学全てに申し込んで断られたら、消去する
    unsettled = list(range(prop_size))

    # 未処理の受験者がいる限り、繰り返す。
    while len(unsettled) != 0:

        # 未処理の受験者の集合から1人ずつとりだして、処理をする
        for i in unsettled:

            # iの選好表から、（今までフラれていない中で）一番好きな大学をとり出す
            candidate = props[i].pop(0)

            # もし取り出したcandidateがアンマッチ・マークなら、iはアンマッチで処理終了
            # マッチングにはprop_unmatched_markをいれる
            if candidate == prop_unmatched_mark:
                prop_matches[i] = prop_unmatched_mark
                unsettled.remove(i)

            else:
                pref = resps[candidate]
                if len(resp_matches[candidate]) < caps[candidate]:
                    if pref.index(i) < pref.index(resp_unmatched_mark):
                        unsettled.remove(i)
                        prop_matches[i] = candidate
                        resp_matches[candidate].append(i)

                else:
                    # すみません、ここのコード大分間違ってました……
                    worst_matched = max(resp_matches[candidate], key=lambda x: pref.index(x))
                    worst_matched_rank = pref.index(worst_matched)
                    i_rank = pref.index(i)

                    if worst_matched_rank > i_rank:
                        unsettled.remove(i)
                        unsettled.append(worst_matched)
                        prop_matches[i] = candidate
                        resp_matches[candidate].remove(worst_matched)
                        resp_matches[candidate].append(i)

    if non_caps_flag:
        prop_matching = list(prop_matches.values())
        resp_matching = list(chain.from_iterable([v if v else [resp_unmatched_mark] for v in resp_matches.values()]))
        return prop_matching, resp_matching

    prop_matching = list(prop_matches.values())
    resp_matching = list(chain.from_iterable(resp_matches.values()))
    len_list = np.array([len(values) for values in resp_matches.values()])
    indptr = np.r_[0, np.cumsum(len_list)]

    return prop_matching, resp_matching, indptr

                
if __name__ == "__main__":

    #prop_prefs, resp_prefs, caps = settings(59, 30)
    m_unmatched = 3
    prop_prefs = [[0, 1, 2, m_unmatched],
                        [2, 0, 1, m_unmatched],
                        [1, 2, 0, m_unmatched],
                        [2, 0, 1, m_unmatched]]

    f_unmatched = 4
    resp_prefs = [[2, 0, 1, 3, f_unmatched],
                        [0, 1, 2, 3, f_unmatched],
                        [2, f_unmatched, 1, 0, 3]]


    caps = np.array([1, 1, 1])
    
    print("受験者の選好表は")
    print(prop_prefs)

    print("大学の選好表は")
    print(resp_prefs)

    print("大学の受け入れ可能人数は")
    print(caps)

    print( deferred_acceptance(resp_prefs, prop_prefs, caps) )


