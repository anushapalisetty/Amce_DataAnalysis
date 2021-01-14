import pandas as pd
class summary_stats():

    def summary_quan(self,df_quan):
        df_desc=df_quan.describe()
        df_trans=df_desc.transpose()
        df_trans_rename=df_trans.rename(columns={'count':'Count','min':'Min','std':'Std. Dev.','25%':'1st Qrt.','mean':'Mean','50%':'Median','75%':'3rd Qrt.','max':'Max' })
        df_trans_rename['Card.']=df_quan.nunique()
        df_trans_rename['% Miss.']=df_quan.isnull().sum()/df_trans['count']*100
        df_summ_quan=df_trans_rename[['Count','% Miss.','Card.','Min','1st Qrt.','Mean','Median','3rd Qrt.','Max','Std. Dev.']]
        return df_summ_quan

    
    def summary_cat(self,df_cat):
        ##calculate summary table values
        df_trans=df_cat.describe().transpose()
        miss_val=df_cat.isnull().sum()
        miss_val_per=miss_val/df_trans['count']*100
        df_trans["% Miss."]=miss_val_per
        mode_per=df_trans['freq']/df_trans['count']*100
        df_trans["Mode %"]=mode_per
        df_trans_rename=df_trans.rename(columns={'count':'Count','unique':'Card.','top':'Mode','freq':'Mode Freq.' })
        ##calculate 2nd mode and its frequency
        count=pd.DataFrame()
        df_val=pd.DataFrame()
        for (name,series) in df_cat.iteritems():
            count = df_cat[name].value_counts().nlargest(n=2).iloc[[1]]
            df_val=df_val.append(count)

        df_re_n=pd.DataFrame(df_val.sum()).reset_index().rename(columns={'index':'2nd Mode',0:'2nd Mode Freq.'},
                                                        index={0:"truckingcompanyid",1:"productid",2:"source",3:"destination"})
        result=pd.concat([df_trans_rename, df_re_n], axis=1, ignore_index=False)

        ##calculating 2nd mode freq percentile
        mode2_per=result['2nd Mode Freq.']/result['Count']*100
        result['2nd Mode %']=mode2_per
        result=result[['Count','% Miss.','Card.','Mode','Mode Freq.','Mode %','2nd Mode','2nd Mode Freq.','2nd Mode %']]
        return result

    def change_datatype(self,df,col_name,datatype):
        return df[col_name].astype(datatype)
    
    
    def extract_num_cat(self,df):
        ## Changing the datatype of truckingcompanyid and productid
        df['truckingcompanyid']=self.change_datatype(df,'truckingcompanyid',str)
        df['productid']=self.change_datatype(df,'productid',str)
        #Extract Numeric and Categorical data
        df_quan=df.select_dtypes(exclude='object')
        df_cat=df.select_dtypes(include='object')
        return df_quan,df_cat
    
    def sample_mean_std_avg(self,df,sample_size,num_iter):
        s1_mean=[0,0,0]
        s1_std=[0,0,0]
        for i in range(num_iter):
            s1_mean+=self.summary_quan(df.sample(sample_size))['Mean']
            s1_std+=self.summary_quan(df.sample(sample_size))['Std. Dev.']
        df_quan_s=pd.DataFrame([s1_mean/num_iter,s1_std/num_iter]).transpose()
        return df_quan_s

    def calc_diff_orig_sample(self,df,sample_size_list,num_iter):
        df_mean_err=pd.DataFrame()
        df_std_err=pd.DataFrame()
        df_mean_err['Orig_Mean']=self.summary_quan(df)['Mean']
        df_std_err['Orig_StdDev']=self.summary_quan(df)['Std. Dev.']
        for i in sample_size_list:
            df_quan_s=self.sample_mean_std_avg(df,i,num_iter)
            df_mean_err['Mean_Err_'+str(i)]= df_mean_err['Orig_Mean']-df_quan_s['Mean']
            df_std_err['Std_Dev_Err'+str(i)]=df_std_err['Orig_StdDev']-df_quan_s['Std. Dev.']
        return df_mean_err,df_std_err
    

