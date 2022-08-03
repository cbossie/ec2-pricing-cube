TERM_COL=0
UNIT_COL=1
PRICE_COL=2
LEN_COL=3
OPTION_COL=4
CLASS_COL=5
LOCAT_COL=6
INST_COL=7
CPU_COL=8
CLOCK_COL=9
RAM_COL=10
STORAGE_COL=11
NET_COL=12
TENAN_COL=13
OS_COL=14
IOP_COL=15
ENCH_COL=16
MODEL_COL=17
FINAL_COLS=["Location","Instance Type","vCPU","RAM (GB)","Max IOPs","Maximum Throughput Mb/s","Dedicated EBS Bandwidth",\
            "Clock Speed","Enchanced Networking","Network Perf", "Storage","Instc Store Disk","Instc Store GBs",\
            "OS","Tenancy","SQL Lic Model","Hourly OnDmd","Monthly OnDmd","1Yr OnDmd","3Yr OnDmd",\
            "All 1Yr Std AURI","All 3Yr Std AURI","All 1Yr Cnvt AURI","All 3Yr Cnvt AURI",\
            "Parital 1Yr Std AURI","Parital 3Yr Std AURI","Parital 1Yr Cnvt AURI","Parital 3Yr Cnvt AURI",\
            "No 1Yr Std AURI","No 3Yr Std AURI","No 1Yr Cnvt AURI","No 3Yr Cnvt AURI",]
COST_MAP={
    "standard1yrAll Upfront":20,
    "standard3yrAll Upfront":21,
    "standard1yrAllUpfront":20,
    "standard3yrAllUpfront":21,
    "convertible1yrAll Upfront":22,
    "convertible3yrAll Upfront":23,
    "convertible1yrAllUpfront":22,
    "convertible3yrAllUpfront":23,
    "standard1yrPartial Upfront":24,
    "standard3yrPartial Upfront":25,
    "standard1yrPartialUpfront":24,
    "standard3yrPartialUpfront":25,
    "convertible1yrPartial Upfront":26,
    "convertible3yrPartial Upfront":27,
    "convertible1yrPartialUpfront":26,
    "convertible3yrPartialUpfront":27,
    "standard1yrNo Upfront":28,
    "standard3yrNo Upfront":29,
    "standard1yrNoUpfront":28,
    "standard3yrNoUpfront":29,
    "convertible1yrNo Upfront":30,
    "convertible3yrNo Upfront":31,
    "convertible1yrNoUpfront":30,
    "convertible3yrNoUpfront":31,
}
LOCAT_MAP={
    "Africa (Cape Town)":"Africa Cape Town",
}
SORT_ORDER={
    "first":TENAN_COL, # Dedicated, Shared, Reversed, Host
    "sec":LOCAT_COL, # ex: Africa Cape Town
    "third":INST_COL, # ex: c5.12xlarge
    "forth":STORAGE_COL, # EBS only or some size like 4x600NVMe
    "fif":OS_COL, # Linux, Win, RHEL, RHEL-HA, SUSE
    "sixth":MODEL_COL, # BYOL, SQL Ent, SQL,Std, SQL Web
}

INVALID_INSTANCES={'c1.medium', 'c1.xlarge','c3.2xlarge', 'c3.4xlarge', 'c3.8xlarge', 'c3.large', 'c3.xlarge', 'c6gn.metal', 'cc2.8xlarge', 'cr1.8xlarge', 'd3en.12xlarge',\
                'd3en.2xlarge', 'd3en.4xlarge', 'd3en.6xlarge','d3en.8xlarge', 'd3en.xlarge', 'dl1.24xlarge', 'f1.16xlarge', 'f1.2xlarge', 'f1.4xlarge', 'g2.2xlarge', 'g2.8xlarge', \
                'g5.12xlarge', 'g5.16xlarge', 'g5.24xlarge', 'g5.2xlarge', 'g5.4xlarge', 'g5.8xlarge', 'g5.xlarge', 'g5.48xlarge','g5g.16xlarge', 'g5g.2xlarge', 'g5g.4xlarge', 'g5g.8xlarge',\
                'g5g.metal', 'g5g.xlarge', 'hs1.8xlarge', 'i2.large', 'i3p.16xlarge', 'm1.large', 'm1.medium', 'm1.small', 'm1.xlarge', 'm2.2xlarge', 'm2.4xlarge', 'm2.xlarge', \
                'm3.2xlarge', 'm3.large', 'm3.medium', 'm3.xlarge', 'mac2.metal', 'p3dn.24xlarge','p4de.24xlarge', 't1.micro', 'u-12tb1.112xlarge', 'u-12tb1.metal', 'u-18tb1.metal', \
                'u-24tb1.metal', 'u-3tb1.56xlarge', 'u-6tb1.metal', 'u-9tb1.112xlarge', 'u-9tb1.metal', 'vt1.24xlarge', 'vt1.3xlarge', 'vt1.6xlarge', 'x2iezn.12xlarge', 'x2iezn.2xlarge',\
                   'x2iezn.4xlarge', 'x2iezn.6xlarge', 'x2iezn.8xlarge','x2iezn.metal'}