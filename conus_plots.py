#%%
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import arcpy

#flowline=r"E:\copula\in_shapefile\nhd\indiana_nhd.shp"
flowline=r"C:\Users\aghangha\Documents\ratingcurve\nhdv2\NHDPlusNationalData\NHDPlusV21_National_Seamless_Flattened_Lower48.gdb\NHDFlowline_Network"

comid_values, length_km, stream_ord,ToNode,drainArea_sqkm, vpuid, rpuid =[str(int(row[0])) for row in arcpy.da.SearchCursor(flowline,['COMID'])],[row[0] for row in arcpy.da.SearchCursor(flowline,['LENGTHKM'])],[row[0] for row in arcpy.da.SearchCursor(flowline,['StreamOrde'])],[str(int(row[0])) for row in arcpy.da.SearchCursor(flowline,['ToNode'])],[row[0] for row in arcpy.da.SearchCursor(flowline,['TotDaSqKM'])],[row[0] for row in arcpy.da.SearchCursor(flowline,['VPUID'])],[row[0] for row in arcpy.da.SearchCursor(flowline,['RPUID'])]
df_stream=pd.DataFrame()
df_stream['COMID']=comid_values; df_stream['LENGTH']=length_km;df_stream['StreamOrder']=stream_ord; df_stream['ToNode']=ToNode;df_stream['DrainArea_sqkm']=drainArea_sqkm; df_stream['VPUID']=vpuid;df_stream['RPUID']=rpuid 

df2=pd.read_csv(r"E:\copula\nwm_outputs\conus\tau_table_stat_sig.csv",index_col=0)
#%%
df1=pd.read_csv(r"E:\copula\nwm_outputs\conus\tau_table.csv",index_col=0)
df2=pd.read_csv(r"E:\copula\nwm_outputs\conus\tau_table_stat_sig.csv",index_col=0)
df2=df2.iloc[:,1:] ## index column occurs twice in this file
df1=df1.dropna()
data=[df1.POM_tau,df2.POM_tau,df1.POT_tau,df2.POT_tau]

labels=['POM all','POM Sign.','POT all','POT Sign.']
plt.rcParams.update({'font.size': 22})
fig=plt.figure(figsize=(15,10))

ax=fig.add_axes([0,0,1,1])

bplot = ax.boxplot(data,
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels,
                     showmeans=True,
                     meanprops={'marker':'*',
                                'markerfacecolor':'white',
                                'markeredgecolor':'black',
                                'markersize':'15'})

ax.set_title('Kendalls Tau for confluences greater than 10 sqkm')
colors = ['darksalmon', 'lightsteelblue', 'lightsalmon','lightblue']
for patch, color in zip(bplot['boxes'],colors):
    patch.set_facecolor(color)

for median in bplot['medians']:
    median.set(color ='black',
               linewidth = 3)
plt.grid(axis='y',linewidth=1)
plt.ylabel("Kendall's Tau", size=26)
plt.show()


#fig=plt.figure(figsize=(15,10))
plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(15,10))
x=df2.DRAIN_ratio
y1=df2.POM_tau
y2=df2.POT_tau
ax=df2.plot.scatter(x="DRAIN_ratio",y="POM_tau",marker='o', c='none', edgecolors="DarkBlue", label="POM")
ax1=df1.plot.scatter(x="DRAIN_ratio",y="POT_tau",marker='v', c='none',edgecolors="DarkRed",label="POT",ax=ax)
ax.set_xscale('log')
plt.xlabel("Drainage Area Ratio")
plt.ylabel("Kendall's Tau")
plt.title("Statistically Significant")

plt.show()


##################

data1=[df2[(df2.DRAIN_ratio>1) & (df2.DRAIN_ratio<=10)]['POM_tau'],df2[(df2.DRAIN_ratio>10) & (df2.DRAIN_ratio<=100)]['POM_tau'],df2[(df2.DRAIN_ratio>100) & (df2.DRAIN_ratio<=1000)]['POM_tau'],df2[(df2.DRAIN_ratio>1000) & (df2.DRAIN_ratio<=10000)]['POM_tau'], df2[(df2.DRAIN_ratio>10000)]['POM_tau']]
data2=[df2[(df2.DRAIN_ratio>1) & (df2.DRAIN_ratio<=10)]['POT_tau'],df2[(df2.DRAIN_ratio>10) & (df2.DRAIN_ratio<=100)]['POT_tau'],df2[(df2.DRAIN_ratio>100) & (df2.DRAIN_ratio<=1000)]['POT_tau'],df2[(df2.DRAIN_ratio>1000) & (df2.DRAIN_ratio<=10000)]['POT_tau'], df2[(df2.DRAIN_ratio>10000)]['POT_tau']]


fig,(ax1,ax2)=plt.subplots(nrows=1,ncols=2,figsize=(20,7))
fig.tight_layout()
plt.rcParams.update({'font.size': 22})
labels=['1-10','10-100','100-1000','1000-10000','>10000']
bplot1=ax1.boxplot(data1,
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels,
                     showmeans=True,
                     meanprops={'marker':'*',
                                'markerfacecolor':'white',
                                'markeredgecolor':'black',
                                'markersize':'15'})
ax1.set_title('Peak on Mainstream')
ax2.set_title('Peak on Tributary')
colors=['darkturquoise','khaki','seashell','lightsteelblue','plum']
bplot2=ax2.boxplot(data2,
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels,
                     showmeans=True,
                     meanprops={'marker':'*',
                                'markerfacecolor':'white',
                                'markeredgecolor':'black',
                                'markersize':'15'})
for bplot in (bplot1,bplot2):
    for patch,color in zip(bplot['boxes'],colors):
        patch.set_facecolor(color)
for bplot in (bplot1,bplot2):
    for median in bplot['medians']:
        median.set(color ='black',
                linewidth = 1.5)
for ax in [ax1,ax2]:
    ax.yaxis.grid('True')
    ax.set_xlabel('Drainage Area Ratio')
    ax.set_ylabel('Kendalls Tau')



####
df=pd.read_csv(r"E:\copula\nwm_outputs\conus\tau_table_stat_sig.csv",index_col=0)
huc_list=df.VPUID.unique()

d1=[]
d2=[]
for huc_id in huc_list:
    d1.append(df[df.VPUID==huc_id]['POM_tau'])
    d2.append(df[df.VPUID==huc_id]['POT_tau'])

fig,(ax1,ax2)=plt.subplots(nrows=2,ncols=1,figsize=(20,15),constrained_layout=True)
fig.tight_layout()
plt.rcParams.update({'font.size': 22})
plt.rcParams['figure.constrained_layout.use'] = True
labels=['1-10','10-100','100-1000','1000-10000','>10000']

colors=['burlywood','lavenderblush','gold','lemonchiffon','khaki','darkturquoise','mediumorchid','seashell','lightsteelblue','plum','darkseagreen','honeydew','lightcoral','slateblue','moccasin','lavender','orchid','mistyrose','slategrey','peru']
bplot1=ax1.boxplot(d1,
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=huc_list,
                     showmeans=True,
                     meanprops={'marker':'*',
                                'markerfacecolor':'white',
                                'markeredgecolor':'black',
                                'markersize':'15'})
ax1.set_title('Peak on Mainstream')
ax2.set_title('Peak on Tributary')
bplot2=ax2.boxplot(d2,
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=huc_list,
                     showmeans=True,
                     meanprops={'marker':'*',
                                'markerfacecolor':'white',
                                'markeredgecolor':'black',
                                'markersize':'15'})
for bplot in (bplot1,bplot2):
    for patch,color in zip(bplot['boxes'],colors):
        patch.set_facecolor(color)
for bplot in (bplot1,bplot2):
    for median in bplot['medians']:
        median.set(color ='black',
                linewidth = 1.5)
for ax in [ax2]:
    ax.yaxis.grid('True')
    ax.set_xlabel('Drainage Area Ratio')
    ax.set_ylabel('Kendalls Tau')
plt.show()
#######


plt.figure(figsize=(10,7),constrained_layout=True)
plt.rcParams.update({'font.size': 12})
ax=df.plot.scatter(x='DRAIN_ratio',y='POM_tau', c=a,cmap='copper')
ax.set_xscale('log')
plt.xlabel("Drainage Area Ratio")
plt.ylabel("Kendall's Tau")

#%%
###plot best fit regression line for different huc regions
df_regress=pd.read_csv("/Users/aghanghas/Downloads/regress_huc2_gtr10.csv")
df_regress=df_regress.drop([15]) ## row 15 is repeated (huc id =12 was repeated), check why
df_regress=df_regress.reset_index()

colors=['black','burlywood','lavenderblush','gold','lemonchiffon','khaki','darkturquoise','mediumorchid','seashell','lightsteelblue','plum','darkseagreen','honeydew','lightcoral','slateblue','moccasin','lavender','orchid','mistyrose','slategrey','peru']
huc_list=df_regress.HUC_ID
plt.rcParams.update({'font.size': 15})
def graph(equation,x_range, title='Best Fit Regression'):
    x=np.array(x_range)
    fig, (ax1) = plt.subplots(1, 1,figsize=(7,7))
    for i,huc in enumerate(huc_list):
        y=equation(x,i)
        ax1.plot(x,y,color=colors[i],label=huc)
    ax1.set_xscale('log')
    ax1.set_title(title)
    ax1.set_xlabel("Drainage Area Ratio")
    ax1.set_ylabel("Kendall's Tau")
    ax1.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.tight_layout()
    plt.show()

def equation(x,i):
    b=df_regress['Coeff_POM'][i]
    a=df_regress['Intercept_POM'][i]
    return(a+b*np.log(x))
############
#%%
data1=[df2[(df2.DRAIN_ratio>1) & (df2.DRAIN_ratio<=10)],df2[(df2.DRAIN_ratio>10) & (df2.DRAIN_ratio<=100)],df2[(df2.DRAIN_ratio>100) & (df2.DRAIN_ratio<=1000)],df2[(df2.DRAIN_ratio>1000) & (df2.DRAIN_ratio<=10000)], df2[(df2.DRAIN_ratio>10000)]]
huc_list=df2.VPUID.unique()
x_range=range(len(huc_list))
marker_list=['o','P','x','D','*']
labels=['1-10','10-100','100-1000','1000-10000','>10000']
fig, (ax1) = plt.subplots(1, 1,figsize=(15,7))
#colors=['burlywood','lavenderblush','gold','lemonchiffon','khaki','darkturquoise','mediumorchid','seashell','lightsteelblue','plum','darkseagreen','honeydew','lightcoral','slateblue','moccasin','lavender','orchid','mistyrose','slategrey','peru']
colors = ['black','darksalmon', 'lightsteelblue', 'lightsalmon','lightblue']
for i in range(len(data1)):
    data1=[df2[(df2.DRAIN_ratio>1) & (df2.DRAIN_ratio<=10)],df2[(df2.DRAIN_ratio>10) & (df2.DRAIN_ratio<=100)],df2[(df2.DRAIN_ratio>100) & (df2.DRAIN_ratio<=1000)],df2[(df2.DRAIN_ratio>1000) & (df2.DRAIN_ratio<=10000)], df2[(df2.DRAIN_ratio>10000)]]
    y=[data1[i][data1[i]['VPUID']==huc_id]['POM_tau'].median() for huc_id in huc_list]
    ax1.scatter(x_range,y,marker=marker_list[i],label=labels[i])

ax1.set_xticklabels(huc_list)
ax1.set_xlabel("HUC ID")
ax1.set_ylabel("Median Kendall's Tau")
ax1.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
