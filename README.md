# Kaggle playground

https://www.kaggle.com/learn

## 2do

### 1-home-data

#### MVP

- implement the remaining planned transformations (planned xlsx file)
- look at test data and see if there are any 1hot/ordinal options that don't exist in the training data
  - ie. Agriculture-zoned
- devise simple plan for remaining transformations
- implement remaining transformations
- try & compare different fitting plans
  - answer the questions below with the comparison
  - pose questions on forums if answers aren't sufficient
  - ie.
    - make commerially zoned just another 1-hot option
    - don't make a separate model for those with or without LotFrontage (try impute +)
- try & compare a few different fitting techniques
- pick the best & submit

#### attempt #2

- automate the comparison of fitting techniques, fitting plans, and data set splitting

## questions

- When encoding categorized data numerically (ie. Great: 2, average: 1, poor: 0)
  - Would it make a difference if I weighted the values (ie. Great: 2.5, average: 0.5, poor: 0.1)
- When given a data set that can be segmented in 2
  - does it make sense to train 2 separate models?
