def calculate_stats():
    """
    code based on Ookla's Github repository tutorials
    https://github.com/teamookla/ookla-open-data/blob/master/tutorials
    calculates weighted average of the download and upload speeds and total tests

    Parameters
    ----------
    data : GeoDataFrame) 
        geo pandas dataframe to analyze
    group_fields : list
        list of fields to group by

    Returns
    ----------
    geopandas.GeoDataFrame
        GeoDataFrame with the calculated stats
    """
    
    return (
        data.groupby(group_fields)
        .apply(
            lambda x: pd.Series(
                {"avg_d_mbps_wt": np.average(x["avg_d_mbps"], weights=x["tests"]),
                "avg_u_mbps_wt": np.average(x["avg_u_mbps"], weights=x["tests"])
                }
            )
        )
        .reset_index()
        .merge(
            data.groupby(group_fields)
            .agg(tests=("tests", "sum"))
            .reset_index(),
            on=group_fields,
        )
    )