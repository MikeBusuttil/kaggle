# Kaggle playground

https://www.kaggle.com/learn

## Prerequisites

- Poetry

## Quick Start

- poetry install

## 2do

### 1-home-data

- see how others did it for my next attempt. Ie...
  - https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/discussion/83751
  - https://www.kaggle.com/code/erikbruin/house-prices-lasso-xgboost-and-a-detailed-eda

#### ask domain expert questions

- do you think a property being classed "2-STORY 1945 & OLDER" vs "2-STORY 1946 & NEWER" would have significant bearing on the price?
  - looking at the data might answer this question

#### attempt #5

- implement what others have done and see how it compares
  - kill all columns Erik kills
    - compare with Rmd results
  - ensure Erik's values are the same as mine
  - ensure Erik & I agree on RMSE scoring results
- clean up transformation functions:
  - kill garage_year and other functions which can instead rely on the improved "apply" transformation
  - find more readable way of grouping similar approaches
    - maybe even a computed table
    - or a "diff":
      - how columns with the same name differ
      - what columns 1 has vs the other
- use the lasso regression model
  - tune it right
- tune the xgboost model
- generate sale price with a weighted average where lasso has 2x weight
- consider de-skewing all numeric predictors
- look at highly correlated columns
- look at those problematic rows to see if anything stands out

#### attempt #6

- figure out why my cross-validation implementation doesn't judge as well as Kaggle
- test dropping different number of columns brute force overnight to see which combo gives the best error estimate

#### attempt #7

- think about pulling out specific data from MSSubClass & HouseStyle & dropping the columns:
  - isPUD
  - NumberStories
  - UnfinishedSQFT
  - isSplitFoyer
  - isDuplex
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

## ML questions

- How can I fit/de-skew with unbounded Johnson distribution (ie. https://www.kaggle.com/code/jesucristo/1-house-prices-solution-top-1)
  - when close to the lower bound it predicts NaN for price
- How might I empirically answer these questions since cross-validated error differs by ~20%
  - ie. how does removing GarageYrBlt perform relative to removing Age vs keeping both
  - 1 option would be to try every possible cross-validation slicing but that would factorial runtime and surely infeasible
- When should high correlations between one-hot-encoded and ordinal or numeric data result in dropping columns
- When encoding categorized data numerically (ie. Great: 2, average: 1, poor: 0)
  - Would it make a difference if I weighted the values (ie. Great: 2.5, average: 0.5, poor: 0.1)
- When given a data set that can be segmented in 2 (ie. houses with Garages vs houses without)
  - does it make sense to train 2 separate models?
- Why does changing the SalePrice to float increase the error?
- How do I choose the right number of estimators when different validation set splits yield wildly different number of rounds til stopping (+/- ~50%)
- Is there a good way to get a measure of confidence with each prediction from a model (ie. SalePrice for house 123 could be off by 5%, SalePrice for house 456 could be off by like %50)
