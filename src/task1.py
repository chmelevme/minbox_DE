import pandas as pd
import numpy as np


def get_session_df(df, timedelta: int = 3, inplace=False):
    if not inplace:
        df = df.copy()
    df['timestamp_lag'] = df.sort_values(by=['timestamp'], ascending=True) \
        .groupby(['customer_id'])['timestamp'].shift(1, fill_value=pd.to_datetime(0))
    df['timestamp_diff'] = df['timestamp'] - df['timestamp_lag']
    df['session_start'] = df['timestamp_diff'].dt.total_seconds() > timedelta * 60  # timedelta минут
    df['session_id'] = df.sort_values(by=['timestamp'], ascending=True).groupby(['customer_id'])['session_start'] \
        .apply(pd.Series).cumsum()
    df.drop(['timestamp_lag', 'timestamp_diff', 'session_start'], axis=1, inplace=True)
    if not inplace:
        return df


if __name__ == '__main__':
    ts = pd.date_range(start='26/10/2022', periods=8, freq='4T').union(
        pd.date_range(start='26/10/2022', periods=8, freq='6T')) \
        .union(pd.date_range(start='26/10/2022', periods=8, freq='7T')).sort_values() \
        .union((pd.date_range(start='27/10/2022', periods=8, freq='4T').union(
        pd.date_range(start='26/10/2022', periods=8, freq='6T')) \
                .union(pd.date_range(start='27/10/2022', periods=8, freq='7T'))).sort_values())
    df = pd.DataFrame({"customer_id": ([1] * int(len(ts) / 2)) + ([2] * int(len(ts) / 2)),
                       "product_id": np.arange(len(ts)),
                       "timestamp": ts})
    new_df = get_session_df(df)
    print(new_df)
