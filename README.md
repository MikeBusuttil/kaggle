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

#### attempt #6

- attempt improvements over Erik and see if score improves:
  - see how it compares when combining all combinable vars.  Ie.
    - kitchenQuality + #kitchens => "Excellent Kitchens", "Good Kitchens", "Typical Kitchens", etc
    - fireplacesQu + fireplaces
    - PoolQC + PoolArea
    - basement SF stuff
    - garage SF stuff
  - optimize parameters for each model(pay for remote compute over night)
  - what is this "MICE" suggestion: https://www.kaggle.com/code/agehsbarg/top-10-0-10943-stacking-mice-and-brutal-force
  - when fixing skew & imputing, should you not apply the transformation obtained from the test set only?
    - see https://datascience.stackexchange.com/a/39933
  - remove OverallQual and GrLivArea outliers
- go over all the transformation decisions 1 more time to see if there are any worth doing differently
  - ie. make Fence ordinal
  - combine building type & MSSubclass

#### attempt #7

- figure out why my cross-validation implementation doesn't judge as well as Kaggle & Caret's
- test dropping different number of columns brute force overnight to see which combo gives the best error estimate

#### Read Scikit Learn docs for possible improvements

- https://scikit-learn.org/stable/modules/preprocessing.html :
  - [Scaling data with outliers](https://scikit-learn.org/stable/modules/preprocessing.html#scaling-data-with-outliers)
  - [Map to Uniform or Gaussian distribution](https://scikit-learn.org/stable/modules/preprocessing.html#non-linear-transformation)

#### Do a write-up & presentation

- credit the sources (with version #s)
- code clean up:
  - any step that takes a long time to complete should be a separate ipynb that saves it's output for other steps to consume
  - kill garage_year and other transformation functions which can instead rely on the improved "apply" transformation
  - find more readable way of grouping similar transformation approaches
    - maybe even a computed table
    - or a "diff":
      - how columns with the same name differ
      - what columns 1 has vs the other
- look at accuracy of the different models vs house price to explain how multiple models makes things better
  - ie. 1 model being way off will be brought back to reality 
- make comment on [Erik's](https://www.kaggle.com/code/erikbruin/house-prices-lasso-xgboost-and-a-detailed-eda) with some suggestions AFTER write-up & presentation:
  - line 1416: `'40'='1 story unf attic'` should be `'40'='1 story fin attic'`
  - spelling mistakes (ie. line 2482 - 2484 "paid of", "definitly", "inproved")
  - Here's where to improve these results (use findings from attempt #6)
- attempt to learn scikit-learn's API to see if there's value there (for readability perhaps & CV runtime I bet)
  - xgb cv model for HPO
- attempt to learn PyCaret's API (for readability & dev speed)
- ask why there's a clear trend of overvalued cheap houses and undervalued expensive houses...
  - but all my attempts to correct for it fail

#### attempt #7

- think about pulling out specific data from MSSubClass & HouseStyle & dropping the columns:
  - isPUD
  - NumberStories
  - UnfinishedSQFT
  - isSplitFoyer
  - isDuplex
- Compare LandContour 1-hot vs ordinal
- attempt dropping more sparsely populated columns
- make separate model for houses without LotFrontage, without garage, without basement
- handle that 1 house that has Sewage for Utilities
- handle that 1 house that doesn't have electrical
- when applying the median/mode for a given column, consider using median from just the training set vs median from train+test sets
- handle sale type & condition
- drop rows BEFORE splitting the data
- write a more efficient 1-hot function that is totally unreadable but uses binary to encode in the most column-efficient manner (but can still be readable when it doesn't matter) 

## ML questions

- why do my XGB predictions (from Python) differ so wildly from Erik's (from R) (up to 15%-20% depending on training parameters)
- why does my custom CV differ so wildly from Python's built-in CV
  - clean it up and publish it asking for help.
- why does Lasso alpha depend so heavily on number of CV splits &/or random_state?
  - the difference in alpha swings price disagreements up to 20%
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
