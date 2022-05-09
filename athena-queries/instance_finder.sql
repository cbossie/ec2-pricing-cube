CREATE OR REPLACE VIEW "instance_finder" AS 
SELECT DISTINCT
  pc.Location "Location"
, pc.instance_type "Instance Type"
, pc."vcpu" "vCPU"
, pc."memory" "RAM (GB)"
, '?' "Max IOPS"
, '?' "Maximum Throughput Mb/s"
, pc.dedicated_ebs_throughput "Dedicated EBS Bandwidth"
, pc.clock_speed "Clock Speed"
, pc.enhanced_networking_supported "Enhanced Networking"
, pc.network_performance "Network Perf"
, pc.storage "Storage"
, pc.instance_store_disk_type "Instance Store Disk"
, pc.total_instance_store___gb "Instance Store GB"
, pc.operating_system "OS"
, pc.tenancy "Tenancy"
, pc.license_model "SQL Lic Model"
, pc.pricingkey "Pricing Key"
FROM
  "pricing_cube_final" pc
