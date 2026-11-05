# AATD project — predicting product discounts

Notebook `AATD_Project.ipynb` contains only code and section titles, following the report structure
(data understanding / EDA, data preparation, modeling, results, conclusions). The report text is written separately.

## Run

1. Put `training.csv` and `test.csv` next to the notebook.
2. `pip install -r requirements.txt`
3. Run all cells. Set `TUNE = False` in the configuration cell for a quick run with default hyper-parameters.

## Outputs

Every block prints its result with a caption and saves it, so it can be pasted into the report:

* `tables/*.csv` and `tables/*.md` — one file per table (descriptive statistics, outliers, duplicates, preparation experiments,
  folds, tuned hyper-parameters, permutation importance...). The model comparison table (model, accuracy, recall, precision,
  F-measure) is `tables/model_comparison`.
* `figures/*.png` — every plot.
* `outputs/submission.csv` — `i,y` predictions for the test set.
* `outputs/cv_folds.csv` — fold assigned to each training row.
