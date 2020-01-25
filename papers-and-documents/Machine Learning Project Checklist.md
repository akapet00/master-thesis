## Machine Learning Project Checklist

From the [Hands-On Machine Learning with Scikit-Learn & Tensorflow](https://github.com/ageron/handson-ml) book by [Aurélien Geron](https://twitter.com/aureliengeron).

### 1. Frame the problem and look at the Big Picture

* define the objective in business terms
* solution end-goal, how it will be used?
* are there any current solutions/workaround - compare 
* framing the problem
    - supervised/unsupervised learning
    - regression/classification
    - online/offline
    - model based or not
    - ...
* how should performance be measured (cost function)
* what would be the minimum performance needed to reach the business objective
* what are comparable problems; can you reuse experience or tools?
* is there a way of solving a problem manually?
* list the assumptions
* verify the assumptions if possible

### 2. Get the data

Automate as much as possible so you it is easier to get fresh data.

* list the data you need and how much data you need
* find the document where you can get that data
* check how much space will it take (it will determine will it be batch or online learning)
* check legal obligations (licenses)
* (get authorizations)
* create a workspace with enough storage space
* get the data
* convert the data to a format you can easily manipulate (usually from csv to dataframe)
* sensitive info must be deleted or protected
* check the size and type of data (time series, samples, geographical and so on)
* sample a test set - put it aside - no data snooping

## 3. Explore the data

* create a copy of the data for exploration (sampling it down to a manageable size if necessary)
* create Jupyter Notebook to keep a record of EDA
* study each attribute and it characteristics:
    - name
    - type (categorical, int/float, bounded/unbounded, text, structured,...)
    - % of missing values
    - noisiness and type of noise (stohastic, outliers, rounding errors...)
    - possibly useful for the task?
    - type of statistical distribution
* identify the target attribute for supervised learning tasks
* visualize the data
* correlation between attributes
* identify the promissing transformations you may want to apply
* identify extra data that would be useful -> repeat 'get the data' process
* document conclusions

## 4. Prepare the data

Notes:
* always work on copies of the data (keep the original intact)
* write functions for all data transformations you apply:
    - easier preparation of the data next time you get a fresh data
    - easier application in future projects
    - to clean and prepare the test set 
    - to make easy to treat preparation choices as hyperparameters

* DATA CLEANING:
    - fix or remove outliers (optional)
    - fill in missing values (with zero/mean/median...) or drop their rows (or columns)

* FEATURE SELECTION:
    - drop the attributes that provide no useful info for the task

* FEATURE ENGINEERING, WHEN AND WHERE APPROPRIATE:
    - discretize continuous features
    - decompose features (categorical, date/time...)
    - add promising transformations of features (log, sqrt, pow...)
    - aggregate features into promising new features

4. FEATURE SCALING: STANDARDIZE or NORMALIZE features

## 5. Short-list promising models

Notes: if the data is huge, you may want to sample smaller training sets so you can train many different models in a reasonable time (this penalizes complex models such as large neural nets or Random Forests); also automate these steps as much as possible

* train many quick and dirty models from different categories using standard parameters

* measure and compare their performance 
    - for each model, use N-fold cross validation and compute the mean and standard deviation of the performance measure on the N folds

* analyze the mos significant variables for each algorithm

* analyze the types of errors that models make

* have a quick round of feature selection and engineering

* have one or two more quick iterations of the five previous steps

* short-list the top three to five most promising models, preferring models that make different types of errors

## 6. Fine-tune the system

Notes: use as much data as possible for this step, especially as you move toward to the end of fine-tuning; automate what you can

* fine-tune hyperparameters using cross-validation:
    - treat your data transformation choices as hyperparameters, especially when you are not sure about them
    - unless there are very few hyperparameter values to explore, prefer random search over grid search; if training is very long, you may prefer a Bayesian optimization approach

* try Ensemble methods

* measure model's performance on the test set to estimate the generalization error (don't tweak model after measuring the generalization error - danger of overfitting)

## 7. Present the solution

* document what you have done

* create a nice presentation - The Big Picture comes first

* explain why this solution achieves the business objective

* implement interesting points during the process 



