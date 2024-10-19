# Kaggle playground

https://www.kaggle.com/learn

## Prerequisites

- Poetry

## Quick Start

- poetry install

## 2do

### 1-home-data

#### ask domain expert questions

- do you think a property being classed "2-STORY 1945 & OLDER" vs "2-STORY 1946 & NEWER" would have significant bearing on the price?
  - looking at the data might answer this question

#### attempt #5

- why the discrepancy with Erik's?
  - generate the output multiple times (on both sides) and see if it changes each time
  - write script that gets both training CSV's to the same order & look for differences
- submit
- clean up transformation functions:
  - kill garage_year and other functions which can instead rely on the improved "apply" transformation
  - find more readable way of grouping similar approaches
    - maybe even a computed table
    - or a "diff":
      - how columns with the same name differ
      - what columns 1 has vs the other
- submit with stopping rounds = average from CV, best from CV and see which Kaggle likes best

#### attempt #6

- attempt improvements over Erik and see if score improves:
  - fix the issue of overvalued cheap houses and undervalued expensive houses (dirty hack or better SalesPrice scaling)
  - make sqft of each finish type (instead of 1hot + sqft columns for each)
  - don't integerize or round everything, keep full precision
  - impute the quality thingie using slope of a line
  - blend & stack models: https://www.kaggle.com/competitions/house-prices-advanced-regression-techniques/discussion/83751 2nd link
  - when fixing skew, should you not apply the transformation obtained from the test set only?
    - see https://datascience.stackexchange.com/a/39933
  - when cross-validating, you can get a sense of your accuracy by continually redrawing the lines and averaging
    - but perhaps this isn't worth the runtime trade-off

#### attempt #7

- figure out why my cross-validation implementation doesn't judge as well as Kaggle & Caret's
- test dropping different number of columns brute force overnight to see which combo gives the best error estimate

#### Read Scikit Learn docs for possible improvements

- https://scikit-learn.org/stable/modules/preprocessing.html :
  - [Scaling data with outliers](https://scikit-learn.org/stable/modules/preprocessing.html#scaling-data-with-outliers)
  - [Map to Uniform or Gaussian distribution](https://scikit-learn.org/stable/modules/preprocessing.html#non-linear-transformation)

#### Do a write-up & presentation

- credit the sources (with version #s)
- look at accuracy of the different models vs house price to explain how multiple models makes things better
  - ie. 1 model being way off will be brought back to reality 
- make comment on [Erik's](https://www.kaggle.com/code/erikbruin/house-prices-lasso-xgboost-and-a-detailed-eda) with some suggestions AFTER write-up & presentation:
  - line 1416: `'40'='1 story unf attic'` should be `'40'='1 story fin attic'`
  - spelling mistakes (ie. line 2482 - 2484 "paid of", "definitly", "inproved")
  - Here's where to improve these results (use findings from attempt #6)
- attempt to learn scikit-learn's API to see if there's value there (for readability perhaps & CV runtime I bet)
  - xgb cv model for HPO
- attempt to learn PyCaret's API (for readability & dev speed)

#### attempt #7

- look for conditions that lead to 1 of the high % error outliers yielding a low % error
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
- write a more efficient 1-hot function that is totally unreadable but uses binary to encode in the most column-efficient manner (but can still be readable when it doesn't matter) 

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
