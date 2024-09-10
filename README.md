# Kaggle playground

https://www.kaggle.com/learn

## 2do

### 1-home-data

- see how others did it for my next attempt. Ie...
  - https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/discussion/83751
  - https://www.kaggle.com/code/erikbruin/house-prices-lasso-xgboost-and-a-detailed-eda

#### attempt #4

- write function to impute the mode
  - and apply everywhere (ie. KitchenQual, Functional, Exterior1st, Exterior2nd, SaleType, ...)
- If pool quality (PoolQC) isn't defined but PoolArea is, get PoolQC from overall house quality
- find median LotFrontage in each neighborhood and apply that to any NA's
- try defaulting GarageYrBlt to YearBuilt (instead of YearRemodAdd) when NA
- try adding back YearBuilt
- fix garage for house 2127:
  - Calculate mode for GarageCond, GarageQual, GarageFinish and apply to house 2127
- house 2577 appears to not actually have a garage, fix that for GarageCars, GarageArea, GarageType
- Fix (9-13) houses with only 1-2 missing basement variable by imputing with mode for column
- Fix houses that appear to not actually have a basement or basement bathroom
- Fix house 2611 that has Masonry Vaneer area but no type: impute the mode
- don't get so cute with BsmtFinType1, BsmtFinType2 & just make them ordinal?
- don't get so cute with Masonry? ... idk, see how that compares
  - ie. set Masonry = dict('None'=0, 'BrkCmn'=0, 'BrkFace'=1, 'Stone'=2)
- for MSZoning, see how it compares when imputing the mode for the 4 NA's
- Compare LandContour 1-hot vs ordinal
- include year & month sold as 1-hot encoded
- 7.1: create a TotalBaths from the sum of full baths + 0.5x half baths
- 7.2:
  - create remodeled: Y/N
  - create Age: Year Sold - YearRemodAdd
  - create IsNew: Y/N if year sold == year built
- 7.4: create a RichNeighborhood ordinal:
  - 2 for the 3 richest
  - 0 for the 3 poorest
  - 1 for the rest
- 7.5: create totalSqFeet = GrLivArea + TotalBsmtSF
  + remove crazy outliers
- drop highly correlated variables, keeping only the var with the highest correlation to sales price
- 8.3.3: consider removing vars:
  - absent in train or test set
  - have less than 10 1's
- ... continue from 8.1 of https://www.kaggle.com/code/erikbruin/house-prices-lasso-xgboost-and-a-detailed-eda

#### attempt #5

- use the lasso regression model
  - tune it right
- tune the xgboost model
- generate sale price with a weighted average where lasso has 2x weight
- fit/de-skew with unbounded Johnson distribution (ie. https://www.kaggle.com/code/jesucristo/1-house-prices-solution-top-1)

#### attempt #6

- make separate model for houses without LotFrontage, without garage, without basement
- handle that 1 house that has Sewage for Utilities
- handle that 1 house that doesn't have electrical
- handle sale type & condition
- drop rows BEFORE splitting the data
- pull in how hot the market was at the time of sale (ie. inventory at the time, # bidders, etc.)
- automate the comparison of fitting techniques, fitting plans, and data set splitting
- investigate what to do with data (ie. NA's) that's in test data but not training data
- see which houses are off by the most and what they all have in common to see if there's a column that's throwing things off

## questions

- When encoding categorized data numerically (ie. Great: 2, average: 1, poor: 0)
  - Would it make a difference if I weighted the values (ie. Great: 2.5, average: 0.5, poor: 0.1)
- When given a data set that can be segmented in 2 (ie. houses with Garages vs houses without)
  - does it make sense to train 2 separate models?
- Why does changing the SalePrice to float increase the error?
- How do I choose the right number of estimators when different validation set splits yield wildly different number of rounds til stopping (+/- ~50%)
