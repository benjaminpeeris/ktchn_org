import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from data import recipes_db

# TODAY = datetime.date

def get_startdate(weekoffset=0, fmt_as_code=False):
    day_offset = 5 - datetime.today().weekday()
    day_offset = day_offset + 7*weekoffset
    start_date = datetime.today() + timedelta(days=day_offset)
    if fmt_as_code:
        return start_date.strftime("%Y%m%d")
    return start_date.strftime("%d-%m-%Y")

# filter values in a df field.
def dd_options(field_name, df, date_fmt=False, sort_by_field=None):
    if sort_by_field:
        df_n = df[[field_name, sort_by_field]].groupby(field_name)[sort_by_field].sum().reset_index()\
            .sort_values(by=sort_by_field, ascending=False)
        print(df_n.head())
        return [{'label': optn[0], 'value': optn[0]} for optn in df_n.to_numpy()]

    df_n = df[[field_name]].drop_duplicates()
    if date_fmt:
        list = [{'label': np.datetime_as_string(optn[0], unit='D'), 'value': np.datetime_as_string(optn[0], unit='D')} for optn in df_n.sort_values(by=field_name).to_numpy()]
        return list
    return [{'label': optn[0], 'value': optn[0]} for optn in df_n.to_numpy()]


def dd_range_options(start, end, step=1):
    return [{'label': optn, 'value': optn} for optn in range(start, end+1, step)]


# filter table -- to modify this to remove the error catching. Just let the DF's go to zero.
def dynamic_filter(df, return_errors=False, **kwargs):
    fn_df = df.copy()
    err_msgs = []
    for key in kwargs:
        # to ignore if filter reduces dataset to below zero i.e. revert to original dataset
        tmp = fn_df.copy()
        fn_df = fn_df.loc[fn_df[key] == kwargs[key]]
        if fn_df.shape[0] == 0:
            fn_df = tmp
            if kwargs[key] is not None:
                print("Selection of {} = {} is ignored based on other selections. ".format(key, kwargs[key]))
                err_msgs.append("Selection of {} = {} is ignored based on other selections. ".format(key, kwargs[key]))
    if return_errors:
        return fn_df, err_msgs
    return fn_df


def get_rec_id(bk_cd, pg):
    return bk_cd + str(pg).zfill(3)


def valid_rec(book, page, name, servings, prep_time, cook_time):
    # 1. test whether all values filled
    if book is None or page is None or name is None or servings is None or prep_time is None or cook_time is None:
        print("Missing some necessary fields!")
        return False
    # 2. test whether code exists already
    rec_id = get_rec_id(book, page)
    if rec_id in list(recipes_db['RecipeCode'].unique()):
        print("Recipe Code Exists!")
        return False
    print("Recipe Valid!")
    return True
