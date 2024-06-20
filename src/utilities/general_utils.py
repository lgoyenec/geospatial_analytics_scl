def quarter_start(year: int, q: int) -> datetime:
    """
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
    """
    
    if not 1 <= q <= 4:
        raise ValueError("Quarter must be within [1, 2, 3, 4]")

    month = [1, 4, 7, 10]
    return datetime(year, month[q - 1], 1)