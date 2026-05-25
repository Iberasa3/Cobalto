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