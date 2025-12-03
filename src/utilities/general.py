from datetime import datetime

def quarter_start(year: int, q: int) -> datetime:
    '''
    calculates the datetime representing the start of a quarter
    code based on Ookla's Github repository tutorials
    https://github.com/teamookla/ookla-open-data/blob/master/tutorials

    Parameters
    ----------
    year : int
        year
    q : int
        quarter

    Returns
    ----------
    datetime
        datetime object representing the start of a quarter
    '''
    
    if not 1 <= q <= 4:
        raise ValueError("Quarter must be within [1, 2, 3, 4]")

    month = [1, 4, 7, 10]

    return datetime(year, month[q - 1], 1)

def find_best_match(data1, data2, priority_vars):
    '''
    find the best pair between two columns with different names
    best pair based on columns values
    
    Parameters
    ----------
    data1 : pandas.DataFrame
        dataframe with columns of interest
    data2 : pandas.DataFrame
        dataframe with columns of interest
    priority_vars: list
        list of variables to prioritize match
        order of elements in list defines priority order 
    
    Returns
    -------
    best_match_pair : tuple
        pair of columns with the highest score (data1,data2)
    '''
    
    # Start parameters
    best_match_pair = None
    max_score       = 0

    # Priority scores
    npriority       = len(priority_vars) + 1
    priority_scores = reversed(range(npriority))
    priority_scores = dict(zip(priority_vars,)) 

    # Iterate over each column in each dataframe
    for col1 in data1.columns:
        for col2 in data2.columns:
            # Get unique values from both columns
            unique_values1 = set(data1[col1].dropna().unique())
            unique_values2 = set(data2[col2].dropna().unique())

            # Calculate intersection of unique values
            intersection      = unique_values1.intersection(unique_values2)
            intersection_size = len(intersection) / len(unique_values2) if unique_values2 else 0

            # Calculate score based on intersection size and column priority
            # Note: default priority is 0.5 if col2 is not in `priority_vars`
            score = intersection_size * priority_scores.get(col2, 0.5)  

            # Check if best match based on score
            if score > max_score:
                max_score = score
                best_match_pair = (col1, col2)

    # Pair of columns with the highest score
    return best_match_pair

def normalize_text(text):
    '''
    normalize text

    Parameters
    ----------
    text : str
        text without normalize

    Returns
    -------
    text : str
        normalized text
    '''
    
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8').lower()