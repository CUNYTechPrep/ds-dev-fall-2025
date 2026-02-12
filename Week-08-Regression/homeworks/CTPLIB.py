import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.api import qqplot
from statsmodels.stats.outliers_influence import variance_inflation_factor



def check_linearity(df, independent_variables, dependent_variable):
    for col in independent_variables:
        sns.jointplot(x=col, y=dependent_variable, data=df, kind="reg");


##########################################################################
def check_normality(model, X, y):
    print('#'*79)
    print('Checking Normality')
    # predictions
    y_pred = model.predict(X)

    # the truth - the prediction
    residuals =  y.values - y_pred.values 

    # histogram
    sns.histplot(residuals)
    plt.show()


    # qq plot
    qqplot(residuals, line='q');
    plt.show()
    print('#'*79)

    

##########################################################################
def plot_homo(model):
    plt.scatter(model_runs_scored.fittedvalues, model_runs_scored.resid, alpha=0.5)
    plt.xlabel('Fitted Values')
    plt.ylabel('Residuals')
    plt.axhline(y = 0, color = 'r')
    plt.show()


##########################################################################    
def plot_correlation(df, independent_variables):
    plt.figure(figsize = (3,3))

    ax = sns.heatmap( df[independent_variables].corr(numeric_only=True), 
                annot=True, 
                cmap='coolwarm',
                vmin=-1, vmax=1);
    plt.show()
    

##########################################################################
def get_vif(X):
    vif = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    vif_df = pd.DataFrame(columns=X.columns, data=[vif])
    print('#'*79)
    print('Variance Inflaction Factors')
    print(vif_df)
    print('#'*79)
    return vif_df



##########################################################################
def build_and_validate_LR(df, independent_variables, dependent_variable):
    X = df[independent_variables]

    y = df[dependent_variable]

    X = sm.add_constant(X)
    model = sm.OLS(y, X).fit()
    
    print(model.summary())
    
    check_linearity(df, independent_variables, dependent_variable)
    
    plot_correlation(df, independent_variables)
    
    vif_df = get_vif(X)
    
    check_normality(model, X, y)