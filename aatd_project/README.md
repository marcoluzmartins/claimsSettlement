# AATD project — predicting product discounts

Notebook `AATD_Project.ipynb` follows the report structure
(Abstract, Introduction, Methodology [CRISP-DM], Results, Conclusions).

## Run

1. Put `training.csv` and `test.csv` next to the notebook.
2. `pip install -r requirements.txt`
3. Run all cells. Set `TUNE = False` in the configuration cell for a quick run with default hyper-parameters.

## Outputs

* `outputs/model_comparison.csv` / `.md` — table of model, accuracy, recall, precision and F-measure (mean over the outer CV folds)
* `outputs/submission.csv` — `i,y` predictions for the test set
* `outputs/cv_folds.csv` — fold assigned to each training row
* `figures/` — all plots used in the report
