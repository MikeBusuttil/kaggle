# Kaggle playground

https://www.kaggle.com/learn

## 2do

### 1-home-data

- see how others did it for my next attempt. Ie...
  - https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/discussion/83751
  - https://www.kaggle.com/code/erikbruin/house-prices-lasso-xgboost-and-a-detailed-eda

#### attempt #4

- drop highly correlated variables, keeping only the var with the highest correlation to sales price
  - investigate highly correlated columns for duplication. ie...
    - BldgType vs MSSubClass
    - PoolQC & OverallQual (did I screw up the imputation?)
- 8.3.3: consider removing vars:
  - absent in train or test set
  - have less than 10 1's
- take a couple rows and see how they've changed from the input csv

#### attempt #5

- use the lasso regression model
  - tune it right
- tune the xgboost model
- generate sale price with a weighted average where lasso has 2x weight
- fit/de-skew with unbounded Johnson distribution (ie. https://www.kaggle.com/code/jesucristo/1-house-prices-solution-top-1)
- consider de-skewing all numeric predictors

#### attempt #6

- don't get so cute with BsmtFinType1, BsmtFinType2 & just make them ordinal?
- don't get so cute with Masonry? ... idk, see how that compares
  - ie. set Masonry = dict('None'=0, 'BrkCmn'=0, 'BrkFace'=1, 'Stone'=2)
- Compare LandContour 1-hot vs ordinal
- make separate model for houses without LotFrontage, without garage, without basement
- handle that 1 house that has Sewage for Utilities
- handle that 1 house that doesn't have electrical
- when applying the median/mode for a given column, consider using median from just the training set vs median from train+test sets
- handle sale type & condition
- drop rows BEFORE splitting the data
- pull in how hot the market was at the time of sale (ie. inventory at the time, # bidders, etc.)
- automate the comparison of fitting techniques, fitting plans, and data set splitting
- investigate what to do with data (ie. NA's) that's in test data but not training data
- see which houses are off by the most and what they all have in common to see if there's a column that's throwing things off

## questions

- When should high correlations between one-hot-encoded and ordinal or numeric data result in dropping columns
- When encoding categorized data numerically (ie. Great: 2, average: 1, poor: 0)
  - Would it make a difference if I weighted the values (ie. Great: 2.5, average: 0.5, poor: 0.1)
- When given a data set that can be segmented in 2 (ie. houses with Garages vs houses without)
  - does it make sense to train 2 separate models?
- Why does changing the SalePrice to float increase the error?
- How do I choose the right number of estimators when different validation set splits yield wildly different number of rounds til stopping (+/- ~50%)
