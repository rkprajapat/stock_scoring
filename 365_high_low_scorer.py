# -*- coding: utf-8 -*-
def compute_yearly_high_low_scores(df):
    df['52WH_Score'] = 0.0
    df['52WL_Score'] = 0.0
    df = df.tail(365)

    highest_value = df['Close'].max()
    lowest_value = df['Close'].min()
    current_value = df['Close'].tail(1).values[0]
        
    gap_2_highest = round(((highest_value - current_value)/current_value)*100,2)
    gap_2_lowest = round(((current_value - lowest_value)/current_value)*100, 2)
        
    return gap_2_highest, gap_2_lowest
    
def compute_yearly_high(df):
    df = df.tail(365)
    highest_value = df['Close'].max()
    return highest_value
    
def compute_yearly_low(df):
    df = df.tail(365)
    lowest_value = df['Close'].min()
    return lowest_value
