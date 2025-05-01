import pandas as pd
from main_prediction.regions_name_map import region_map


def prepare_region(pred_df):
    pred_df = pd.get_dummies(pred_df, columns=['region_id'], drop_first=False)

    pred_df = pred_df.rename(columns={
        f"region_id_{i}": region_map[i]
        for i in region_map
        if f"region_id_{i}" in pred_df.columns
    })

    if "Simferopol" in pred_df.columns:
        pred_df = pred_df.drop(columns=["Simferopol"])

    expected_columns = [region_map[i] for i in range(2, 27)]
    for col in expected_columns:
        if col not in pred_df.columns:
            pred_df[col] = False

    return pred_df[expected_columns]


def merge_prediction_dataset(region_id, weather_df, isw_df, other_alarm_percent, expected_columns):
    isw_df = pd.concat([isw_df] * 24, ignore_index=True)

    pr = pd.concat([weather_df, isw_df], axis=1)

    pr['region_id'] = region_id
    pr['other_regions_with_alarm_percent'] = other_alarm_percent

    p = prepare_region(pr)
    pr = pd.concat([pr, p], axis=1)

    pred_columns = set(pr.columns)
    missing_columns = set(expected_columns) - pred_columns
    extra_columns = pred_columns - set(expected_columns)

    for col in missing_columns:
        pr[col] = 0

    pr.drop(columns=extra_columns, inplace=True)

    return pr[expected_columns]