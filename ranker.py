"""Rank candidates by blended suitability score."""
import pandas as pd


def rank_candidates(rows):
    """rows: iterable of dicts with at least 'name' and 'score'."""
    df = pd.DataFrame(rows).sort_values("score", ascending=False).reset_index(drop=True)
    df.insert(0, "rank", df.index + 1)
    return df
