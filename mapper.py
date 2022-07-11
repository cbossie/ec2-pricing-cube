import argparse
import pandas as pd
import numpy as np
import re

from const import *
parser = argparse.ArgumentParser(
        description="Given an input list of servers, this script optimizes dedicated host placement for the servers.")
parser.add_argument('--input-file', '-i', required=True,
                        action="store", dest="input_file_path")
parser.add_argument('--output-file', '-o', required=False,
                        action="store", dest="output_file_path")
parser.add_argument('--windows-server-entitlements', '-w', required=False,
                        action="store", dest="ws_entitlements_cpus", type=int)
args = parser.parse_args()
with open(args.input_file_path) as f:
    
    df = pd.read_csv(f,skiprows=5)

#fixing column names
df.columns = df.columns.str.replace('\n',' ')
df.columns = df.columns.str.replace('  ',' ')

df.drop(['SKU','EffectiveDate','OfferTermCode','RateCode','Currency','serviceCode','Location Type','Processor Architecture'\
              ,'Storage Media','Volume Type','Max Volume Size','Max IOPS/volume','Max IOPS Burst Performance',\
            'Max throughput/volume','Provisioned','From Location Type','usageType','operation','Processor Features', \
         'Product Type', 'Region Code', 'Resource Type','serviceName', 'SnapshotArchiveFeeType', 'To Region Code',\
       'Volume API Name', 'VPCNetworkingSupport','Group Description','Transfer Type','From Location','To Location',\
         'To Location Type','Physical Cores','Group', 'MarketOption','instanceSKU','From Region Code', \
         'Intel AVX2 Available', 'Elastic Graphics Type','Intel AVX Available', 'Intel Turbo Available',\
         'ClassicNetworkingSupport','AvailabilityZone','Normalization Size Factor', 'EBS Optimized','instanceSKU',\
        'StartingRange','EndingRange','Instance Capacity - 10xlarge', 'Instance Capacity - 12xlarge',\
       'Instance Capacity - 16xlarge', 'Instance Capacity - 18xlarge','Current Generation',\
       'Instance Capacity - 24xlarge', 'Instance Capacity - 2xlarge',"PriceDescription","License Model",\
       'Instance Capacity - 32xlarge', 'Instance Capacity - 4xlarge',\
       'Instance Capacity - 8xlarge', 'Instance Capacity - 9xlarge',\
       'Instance Capacity - large', 'Instance Capacity - medium',\
       'Instance Capacity - metal', 'Instance Capacity - xlarge','RelatedTo']\
        , axis=1,inplace=True)

df["Location"]=df["Location"].apply(lambda x: re.split('\)|\(',x) if type(x)==str else x)
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
    elif pd.isna(row[STORAGE_COL]):
        continue
    elif row[TENAN_COL]=="Host" and row[PRICE_COL]==0:
        continue
    if row[TENAN_COL] not in grouper:
        grouper[row[TENAN_COL]]={}
    temp=grouper[row[TENAN_COL]]
    
    if row[LOCAT_COL] not in temp:
        temp[row[LOCAT_COL]]={}
    temp=temp[row[LOCAT_COL]]
    
    if row[INST_COL] not in temp:
        temp[row[INST_COL]]={}
    temp=temp[row[INST_COL]]
    
    if row[STORAGE_COL] not in temp:
        temp[row[STORAGE_COL]]={}
    temp=temp[row[STORAGE_COL]]
    
    if row[OS_COL] not in temp:
        temp[row[OS_COL]]={}
    temp=temp[row[OS_COL]]
    
    if row[MODEL_COL] not in temp:
        temp[row[MODEL_COL]]=[0]*32
    temp=temp[row[MODEL_COL]]
        
    if temp[0]==0:
        temp[0]=row[LOCAT_COL]
        temp[1]=row[INST_COL]
        temp[2]=row[CPU_COL]
        temp[3]=row[RAM_COL]
        temp[7]=row[CLOCK_COL]
        temp[8]=row[ENCH_COL]
        temp[9]=row[NET_COL]
        stor=row[STORAGE_COL]
        temp[10]=stor
        if stor!="EBS only":
            if not pd.isna(stor):
                temper=stor.split()
                temp[11]=temper[len(temper)-1]
                temp[12]=int(temper[0])*int(temper[2])
            else:
                temp[11]=np.NaN
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
            temp[COST_MAP[row[CLASS_COL]+row[LEN_COL]+row[OPTION_COL]]]+=int(row[PRICE_COL])*8760*int(row[LEN_COL][0])
        else:
            temp[COST_MAP[row[CLASS_COL]+row[LEN_COL]+row[OPTION_COL]]]+=int(row[PRICE_COL])


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

t = [ [] for i in range(32)]
for a in grouper["keys"]:
    for b in grouper[a]["keys"]:
        for c in grouper[a][b]["keys"]:
            for d in grouper[a][b][c]["keys"]:
                for e in grouper[a][b][c][d]["keys"]:
                    for f in grouper[a][b][c][d][e]["keys"]:
                        for i in range(32):
                            t[i].append(grouper[a][b][c][d][e][f][i])

new_df=pd.DataFrame(t[0],columns=["Location"])
for i in range(1,32):
    new_df[FINAL_COLS[i-1]]=t[i]
new_df.to_csv("mapped_output.csv", index = False)