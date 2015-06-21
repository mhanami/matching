#-------------------------------------------------------------------------------
# Name:        gs_one.py
# Purpose:     GS Algorithm; "one-to-one" case
#
# Author:      Hanami Maeda, Atsushi Yamagishi
#
# Created:     21/06/2015
#-------------------------------------------------------------------------------

# coding: UTF-8
from __future__ import division
import numpy as np
"""
m_prefs=np.array([[4,0,1,2,3],[2,1,0,3,4],[0,1,3,2,4]])
f_prefs=np.array([[0,1,2,3],[1,0,3,2],[1,2,0,3],[0,3,2,1]])
"""
def array_to_dict(array):
    dict = {}
    for x, y in enumerate(array):
        dict[x] = list(y)
    return dict

def deferred_acceptance(m_prefs, f_prefs):
    # 辞書に変換
    males = array_to_dict(m_prefs)
    females = array_to_dict(f_prefs)
    #男性に対し、ペアの女性を返す辞書。とりあえずペアがないから、空の状態
    matches = {}
    for i in range(len(m_prefs)):
        matches[i] = ""
    # 独身男性の集合
    unsettled = range(len(m_prefs))
    # 独身男性がいる限り、繰り返す。
    while len(unsettled) != 0:
        for i in unsettled:
            # プロポーズ済の人を候補者から消す
            # 好みランクが最も高い人にプロポーズする。
            candidate = males[i].pop(0)
            # 好みランクが最も高い人にプロポーズする。
            # 好みの人がもうおらず、一人でいたい場合
            if candidate == (len(f_prefs)):
                matches[i] = candidate
                unsettled.remove(i)
            # まだ誰とも結婚してなければ自分のもの
            elif candidate not in matches.values():
                pref = females[candidate]
                # 一人の方がマシじゃなければ成立
                if pref.index(i) < pref.index(len(m_prefs)):
                    matches[i] = candidate
                    unsettled.remove(i)
            # 誰かと結婚していれば、女性の好みにより成否が決定
            else:
                # ペアについて、女性から男性を返す辞書
                matches_inv = {v:k for k, v in matches.items()}
                # 今の夫
                matched_male = matches_inv[candidate]
                # 女性の好み
                pref = females[candidate]
                # より好み＝好みで上位にランクされてるなら、略奪成功
                if pref.index(i) < pref.index((matched_male)):
                    # 妻を奪われ独身に戻る
                    matches[matched_male] = ""
                    unsettled.append(matched_male)
                    matches[i] = candidate
                    unsettled.remove(i)
                    unsettled.sort()
    # 結果の辞書を一次元配列に変換
    stable_mf = []
    for i in matches.keys():
        stable_mf.append(matches[i])
    # 女性から男性へのマッチングのリストも作る
    stable_fm = []
    for i in range(len(f_prefs)):
        if i in stable_mf:
            stable_fm.append(stable_mf.index(i))
        else:
            stable_fm.append(len(m_prefs))
    return stable_mf, stable_fm
