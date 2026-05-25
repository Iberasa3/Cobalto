# Data Source

## Primary Dataset Candidate

The initial dataset candidate is LendingClub loan data.

## Why This Dataset

LendingClub data is suitable for a credit risk decision engine because it contains real loan-level information, borrower attributes, loan terms, credit history variables, and repayment outcomes.

## ML Target

The initial target will be default risk.

Possible positive class:

- Charged Off
- Default
- Late loans beyond a defined threshold

Possible negative class:

- Fully Paid


## Column Meanings and Comments

This section documents the meaning of each column in the raw dataset and initial modeling comments.

| Column | Meaning | Modeling Comments |
|---|---|---|
| `id` | Unique identifier for each loan record. | Identifier only. Do not use as a model feature. Useful for traceability. |
| `issue_d` | Loan issue date. | Useful for temporal splits, validation design, and monitoring over time. Avoid using it directly as a raw feature. |
| `revenue` | Borrower's reported income or revenue. | Important affordability feature. Check missing values, outliers, and skew. |
| `dti_n` | Debt-to-income ratio. | Core credit risk feature. Higher values may indicate lower repayment capacity. |
| `loan_amnt` | Requested or granted loan amount. | Important exposure feature. Later useful for expected loss and policy simulation. |
| `fico_n` | Borrower's FICO credit score or normalized FICO variable. | Strong creditworthiness feature. Check range and distribution. |
| `experience_c` | Borrower's experience category. | Categorical feature. Needs encoding before modeling. |
| `emp_length` | Borrower's employment length. | Stability indicator. May need cleaning and ordinal encoding. |
| `purpose` | Stated purpose of the loan. | Categorical feature. Useful for risk segmentation. |
| `home_ownership_n` | Borrower's home ownership status. | Categorical or encoded feature. Confirm values before modeling. |
| `addr_state` | Borrower's state. | Geographic categorical feature. May capture regional patterns; use carefully. |
| `zip_code` | Borrower's ZIP code or partial ZIP code. | High-cardinality geographic feature. Risk of overfitting and fairness concerns. Exclude initially or aggregate later. |
| `Default` | Binary target variable indicating whether the loan defaulted. | Prediction target. Must never be used as an input feature. |
| `title` | Short borrower-provided loan title. | Text feature. Exclude from first baseline; possible later NLP feature. |
| `desc` | Borrower-provided loan description. | Longer text feature. Likely sparse/noisy. Exclude from first baseline; possible later NLP feature. |

## Initial EDA Notes

### `id`

The `id` column is used only as a unique loan identifier.

Initial checks show that there are no duplicated IDs in the raw dataset. This column will not be used as a model feature, but it can be kept for traceability, debugging, and joining predictions back to original records.

### `addr_state` and `zip_code`

The `addr_state` and `zip_code` columns contain geographic information about the borrower.

Although these variables could contain predictive signal, they may introduce legal, ethical, and fairness concerns when used for credit decisions. Geographic variables can act as proxies for sensitive socioeconomic or demographic characteristics.

For the initial modeling baseline, both columns will be excluded from the feature set:

- `addr_state`
- `zip_code`

They may still be used for aggregate monitoring or bias analysis, but not for deciding whether to grant a loan.


## Leakage Risks

Columns created after loan issuance must not be used as model inputs.

Examples of risky columns:

- recoveries
- collection_recovery_fee
- last_pymnt_d
- last_pymnt_amnt
- total_pymnt
- total_rec_prncp
- total_rec_int
- loan_status if used as feature
- next payment or post-origination fields

## Storage Plan

Raw files will be stored under:

data/raw/

Processed training datasets will be stored under:

data/processed/

Raw data should never be modified in place.