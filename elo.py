from math import log

K = 32
y = 2
l = 1 + log(2) / log(K)
D = 400


def calculate_rank_change(rank1, rank2, score1: int, score2: int):
    score_diff = score1 - score2
    expected = 1 / (1 + 10 ** ((rank2 - rank1) / D))
    actual = 1 if score1 > score2 else 0.5 if score1 == score2 else 0
    margin = log(abs(score_diff) + 1) * (2.2 / ((rank1 - rank2) * 0.001 + 2.2))
    rank_diff = K * margin * (actual - expected)
    return round(rank_diff)
