Fabric script
=====================

vultr
---------------------
###Test api-key aceesss
```sh
fab -f vultr.py can_access:API-KEY
```
###Get server list (Get SUBID)
```sh
fab -f vultr.py get_server_by_id:API-KEY
```
###Get region list (Get DC ID)
```sh
fab -f vultr.py get_region_list
```
###Get plan list (Get plan ID)
```sh
fab -f vultr.py get_plan_list
```
###Test if region A available plan B
```sh
fab -f vultr.py is_region_available_plan:REGION_A_ID,PLAN_B_ID
```
###Get OS list (Get OS ID)
```sh
fab -f vultr.py get_os_list
```
###Create server (use parameter LABEL to set server name.)
```sh
fab -f vultr.py create_server:API_KEY,LABEL,DC_ID,PLAN_ID,OS_ID
```
###Wait until server installed and start success.
```sh
fab -f vultr.py wait_until_ok:API_KEY,LABEL
```
###Destroy server by LABEL
```sh
fab -f vultr.py destroy_server_by_label:API_KEY,LABEL
```
###Destroy server by SUBID
```sh
fab -f vultr.py destroy_server_by_id:API_KEY,SUBID
```
###Get ip by LABEL
```sh
fab -f vultr.py get_ip_by_label:API_KEY,LABEL
```

dnspod
---------------------
###Get domain list
```sh
fab -f dnspod.py get_domain_list:token_id,token,keyword=example.com
```

####param
* token_id
* token
* type, optional, default=all, other=mine/share/ismask/pause/vip/recent/share_out
* offset, optional, default=0
* length, optional
* group_id, optional
* keyword, optional

####return
* DOMAIN_ID
* STATUS: enable/pause/spam/lock
* RECORDS: number of records 
* DOMAIN_NAME
* OWNER

###Get record(sub domain) list
```sh
fab -f dnspod.py get_record_list:token_id,token,domain_name
```

####param
* token_id
* token
* domain_name
* offect, optional
* length, optional
* sub_domain, optional
* keyword, optional

####return
* domain_id
* name
* owner
* sub_domains: number of sub domains
* record_total: number of records
* RECORD_ID
* NAME
* LINE: 默认/国内/国外/电信/联通/搜索引擎/...
* TYPE: A/CNAME/TXT/NS/AAAA/MX/SRV/显性URL/隐性URL
* TTL
* MX
* ENABLED: "0": 禁用, "1": 启用 
* VALUE

###Create record(sub domain)
```sh
fab -f dnspod.py create_record:token_id,token,domain_name,sub_domain,record_type,value
```

####param
* token_id
* token
* domain_name
* sub_domain
* record_type: A/CNAME/TXT/NS/AAAA/MX/SRV/显性URL/隐性URL
* value: IPv4 address when record_type=A
* record_line, optional, default=默认, others; 默认/国内/国外/电信/联通/搜索引擎/...
* mx, required when record_type=MX, range 1 - 20
* ttl, optional, range 1 - 604800
* status, optional, default=enable, other: disable
* weight, optional, range 0 - 100

###Modify record(sub domain)
```sh
fab -f dnspod.py modify_record:token_id,token,domain_name,sub_domain_name,new_record_type,new_value
```

####param
* token_id
* token
* domain_name
* sub_domain_name
* new_record_type
* new_value
* new_record_line, optional, default=默认
* new_mx, optional
* new_ttl, optional
* new_status, optional
* new_weight, optional

ssh
---------------------