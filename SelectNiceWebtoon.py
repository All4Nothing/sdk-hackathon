import pandas as pd
import numpy as np

rating=pd.read_csv('./rating.csv')

def SelectNIceWebtoon(f_var, g_var):
    formatOption = rating['format'] == f_var
    genreOption = rating['genre'] == g_var
    selectedWebtoon = rating[formatOption & genreOption]
    sortedWebtoon=selectedWebtoon.sort_values(['rating'])
    NiceSortedWebtoon=sortedWebtoon[-3:]
    return NiceSortedWebtoon['title']