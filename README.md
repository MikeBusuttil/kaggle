# Kaggle playground

https://www.kaggle.com/learn

## 2do

### 1-home-data

#### MVP

- try & compare different fitting plans
  - answer the questions below with the comparison
  - pose questions on forums if answers aren't sufficient
  - ie.
    - make commercially zoned just another 1-hot option
- try & compare a few different fitting techniques
- pick the best & submit

#### attempt #2

- make separate model for houses without LotFrontage, without garage, without basement
- handle that 1 house that has Sewage for Utilities
- handle that 1 house that doesn't have electrical
- handle sale type & condition
- drop rows BEFORE splitting the data
- pull in how hot the market was at the time of sale (ie. inventory at the time, # bidders, etc.)
- automate the comparison of fitting techniques, fitting plans, and data set splitting
- investigate what to do with data (ie. NA's) that's in test data but not training data

## questions

- When encoding categorized data numerically (ie. Great: 2, average: 1, poor: 0)
  - Would it make a difference if I weighted the values (ie. Great: 2.5, average: 0.5, poor: 0.1)
- When given a data set that can be segmented in 2
  - does it make sense to train 2 separate models?
