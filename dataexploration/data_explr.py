import pandas as pd
from scipy.stats import chisquare,chi2_contingency,chi2

class DataExploration():
    def rel_cat_chisquare(self,df,columns):
        df_chi=pd.DataFrame()
        cat_1=[]
        cat_2=[]
        test_stat=[]
        pval=[]
        stat_sig=[]
        pval_sig=[]
        for i in range(len(columns)):
            for j in columns[i+1:]:
                table=pd.crosstab(df[columns[i]], df[j])
                stat, p, dof, expected = chi2_contingency(table)
                cat_1.append(columns[i])
                cat_2.append(j)
                test_stat.append(stat)
                pval.append(p)
                # interpret test-statistic
                prob = 0.95
                critical = chi2.ppf(prob, dof)
                if abs(stat) >= critical:
                    stat_sig.append('Reject H0')
                else:
                    stat_sig.append('Fail to Reject H0')
                # interpret p-value
                alpha = 1.0 - prob
                if p <= alpha:
                    pval_sig.append('Reject H0')
                else:
                    pval_sig.append('Fail to Reject H0')
        df_chi['Categorical_1']=cat_1
        df_chi['Categorical_2']=cat_2
        df_chi['Test_Statistic']=test_stat
        df_chi['P-Value']=pval
        df_chi['Statis_Signf']=stat_sig
        df_chi['Pval_Signf']=pval_sig
        return df_chi
