# Data

The data for this project comes from the M5 Forecasting Accuracy competition on Kaggle.

## Source
https://www.kaggle.com/competitions/m5-forecasting-accuracy/data

## What's used in this project

Place the following files in `data/raw/`:

| File | Description | Size |
|---|---|---|
| `sales_train_evaluation.csv` | Daily unit sales per SKU per store, 1,941 days ending in mid-2016 | ~120 MB |
| `calendar.csv` | Calendar metadata: day-of-week, events, SNAP food-stamp days | ~100 KB |
| `sell_prices.csv` | Weekly average selling price per SKU per store | ~200 MB |

The `sales_train_evaluation.csv` is the longer version used in the M5 competition's final round (1,941 days). It supersedes `sales_train_validation.csv` (1,913 days).

## Why the data is not in this repository
Raw data is gitignored (see `.gitignore` at the project root) because the files are several hundred MB combined — well past GitHub's recommended size limits.

## Reproducing this project
1. Create a free Kaggle account
2. Accept the competition rules on the data page (one-time click)
3. Download the three files listed above
4. Place them in `data/raw/`