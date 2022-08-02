import argparse
import pandas as pd
import numpy as np
import re
import boto3
import timeit


from const import *

parser = argparse.ArgumentParser(
        description="Given an input list of servers, this script optimizes dedicated host placement for the servers.")
parser.add_argument('--input-file', '-i', required=True,
                        action="store", dest="input_file_path")
parser.add_argument('--input_skip_num', '-n', required=True,
                        action="store", dest="input_skip_num")
args = parser.parse_args()

with open(args.input_file_path) as f:
    df = pd.read_csv(f,skiprows=int(args.input_skip_num))

#fixing column names
df.columns = df.columns.str.replace('\n',' ')
df.columns = df.columns.str.replace('  ',' ')

#grab only needed cols
df=df[['TermType', 'Unit', 'PricePerUnit', 'LeaseContractLength',
       'PurchaseOption', 'OfferingClass', 'Location','Instance Type', 'vCPU',
       'Clock Speed', 'Memory', 'Storage', 'Network Performance', 'Tenancy',
       'Operating System','Dedicated EBS Throughput', 'Enhanced Networking Supported','Pre Installed S/W']]


all_instances=set(df[df["Instance Type"].notna()]["Instance Type"].unique())
all_instances=all_instances.difference(INVALID_INSTANCES)
all_instances=list(all_instances)
IOPS_match={}

for i in range(int(np.ceil(len(all_instances)/100))):
    test= boto3.client('ec2')
    cap= min(((i+1)*100), len(all_instances))

    test2=test.describe_instance_types(
        DryRun=False,
        InstanceTypes=all_instances[(i*100):cap],

    )
    for i in test2["InstanceTypes"]:
        if i['EbsInfo']['EbsOptimizedSupport']=="unsupported":
            continue
        temp=i['EbsInfo']['EbsOptimizedInfo']
        IOPS_match[i['InstanceType']]=[temp['BaselineIops'],temp['MaximumThroughputInMBps'],temp['MaximumBandwidthInMbps']]

# rename/mapping variable names for multiple columns 
df["Location"]=df["Location"].apply(lambda x: x if x not in LOCAT_MAP else LOCAT_MAP[x])
df["Location"]=df["Location"].apply(lambda x: re.split('\)|\(',x) if (type(x)==str and ')' in x) else x)
df["Location"]=df["Location"].apply(lambda x:  x if (type(x)!= list) else ("Gov "+x[1] if ("GovCloud" in x[0])\
                     else (x[1] if (x[2] =='') else x[1]+x[2])))
df["Location"]=df["Location"].apply(lambda x:  x if (type(x)!= str) else (x if ("N." not in x) else (x.replace("N. Virginia","Virginia") if ("N. Virginia" in x)\
                    else x.replace("N. California","NorCal"))))


df["Storage"]= df["Storage"].apply(lambda x:  x if (type(x)!= str) else (x if ("NVMe" not in x) else 
                        "1 x "+x[:len(x)-4] if ('x' not in x) else x[:len(x)-4]))



df["Operating System"] = df["Operating System"].apply(lambda x: x if (type(x)!= str) else \
             ("Win" if (x=="Windows") else \
              ("RHEL-HA" if (x[:3]=="Red") else x)))


df["Memory"] = df["Memory"].apply(lambda x: x if (type(x)!= str) else float(x.split()[0]))


df["Enhanced Networking Supported"] = df["Enhanced Networking Supported"].apply(lambda x:\
                                    x if (type(x)!= str) else ("Y" if (x=="Yes") else "N"))


df['Pre Installed S/W'] = df['Pre Installed S/W'].apply(lambda x: "BYOL" if (type(x)!= str) else x)

df['Network Performance'] = df['Network Performance'].apply(lambda x: x if (type(x)!= str) else \
            (x[5:].replace(" Gigabit","gbs") +"(<=)" if (x[:5]=="Up to" and "Gigabit" == x[len(x)-7:]) else \
            (x[5:].replace(" Megabit","mbs") +"(<=)" if (x[:5]=="Up to" and "Megabit" == x[len(x)-7:]) else \
            (x.replace(" Gigabit","gbs") if ("Gigabit" == x[len(x)-7:]) else\
            (x.replace(" Megabit","mbs") if ("Megabit" == x[len(x)-7:]) else\
            ("Mod" if (x=="Moderate") else x))))))

df['LeaseContractLength']=df['LeaseContractLength'].apply(lambda x: x if (type(x)!= str) else x.replace(" ",""))


# starts sorting all rows into correct path
grouper={}
for i in df.iterrows():
    num=i[0]
    row=i[1]

    if pd.isna(row[LOCAT_COL]):
        continue
    elif pd.isna(row[CPU_COL]):
        continue
    elif pd.isna(row[TENAN_COL]):
        continue

    if row[SORT_ORDER["first"]] not in grouper:
        grouper[row[SORT_ORDER["first"]]]={}
    temp=grouper[row[SORT_ORDER["first"]]]
    
    if row[SORT_ORDER["sec"]] not in temp:
        temp[row[SORT_ORDER["sec"]]]={}
    temp=temp[row[SORT_ORDER["sec"]]]
    
    if row[SORT_ORDER["third"]] not in temp:
        temp[row[SORT_ORDER["third"]]]={}
    temp=temp[row[SORT_ORDER["third"]]]
    
    if row[SORT_ORDER["forth"]] not in temp:
        temp[row[SORT_ORDER["forth"]]]={}
    temp=temp[row[SORT_ORDER["forth"]]]
    
    if row[SORT_ORDER["fif"]] not in temp:
        temp[row[SORT_ORDER["fif"]]]={}
    temp=temp[row[SORT_ORDER["fif"]]]
    
    if row[SORT_ORDER["sixth"]] not in temp:
        temp[row[SORT_ORDER["sixth"]]]=[np.nan]*15+[0]*17
    temp=temp[row[SORT_ORDER["sixth"]]]
        
    if temp[0]==0:
        temp[0]=row[LOCAT_COL]
        temp[1]=row[INST_COL]
        temp[2]=row[CPU_COL]
        temp[3]=row[RAM_COL]
        if row[INST_COL] in IOPS_match:
            temp[4]=float(IOPS_match[row[INST_COL]][0])
            temp[5]=float(IOPS_match[row[INST_COL]][1])
            temp[6]=float(IOPS_match[row[INST_COL]][2])
        temp[7]=row[CLOCK_COL]
        temp[8]=row[ENCH_COL]
        temp[9]=row[NET_COL]
        stor=row[STORAGE_COL]
        temp[10]=stor
        if stor!="EBS only" and not pd.isna(stor):
            temper=stor.split()
            temp[11]=temper[len(temper)-1]
            temp[12]=int(temper[0])*int(temper[2])

        else:
            temp[11]=np.NaN
            temp[12]=np.NaN
        temp[13]=row[OS_COL]
        temp[14]=row[TENAN_COL]
        temp[15]=row[MODEL_COL]
    if row[TERM_COL]=="OnDemand":
        cost=row[PRICE_COL]
        if cost!=0:
            temp[16]=cost
            temp[17]=cost*730
            temp[18]=cost*8760
            temp[19]=cost*26280
    else:

        if row[UNIT_COL]=="Hrs":
            temp[COST_MAP[row[CLASS_COL]+row[LEN_COL]+row[OPTION_COL]]]+=row[PRICE_COL]*8760*int(row[LEN_COL][0])
        else:
            temp[COST_MAP[row[CLASS_COL]+row[LEN_COL]+row[OPTION_COL]]]+=row[PRICE_COL]

# sort each subgroup
for a in grouper:
    for b in grouper[a]:
        for c in grouper[a][b]:
            for d in grouper[a][b][c]:
                for e in grouper[a][b][c][d]:
                    grouper[a][b][c][d][e]["keys"]=sorted(grouper[a][b][c][d][e].keys())
                grouper[a][b][c][d]["keys"]=sorted(grouper[a][b][c][d].keys())
            grouper[a][b][c]["keys"]=sorted(grouper[a][b][c].keys())
        grouper[a][b]["keys"]=sorted(grouper[a][b].keys())
    grouper[a]["keys"]=sorted(grouper[a].keys())
grouper["keys"]=sorted(grouper.keys())

# add each row in order to a list
t = [ [] for i in range(32)]
for a in grouper["keys"]:
    for b in grouper[a]["keys"]:
        for c in grouper[a][b]["keys"]:
            for d in grouper[a][b][c]["keys"]:
                for e in grouper[a][b][c][d]["keys"]:
                    for f in grouper[a][b][c][d][e]["keys"]:
                        for i in range(32):
                            t[i].append(grouper[a][b][c][d][e][f][i])

# put the list in a df and save as csv
new_df=pd.DataFrame(t[0],columns=[FINAL_COLS[0]])
for i in range(1,32):
    new_df[FINAL_COLS[i]]=t[i]
new_df.to_csv("mapped_output.csv", index = False)
