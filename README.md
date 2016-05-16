Fabric script
=====================
vultr
---------------------
######Test api-key aceesss
fab -f vultr.py can_access:API-KEY

######Get server list (Get SUBID)
fab -f vultr.py get_server_by_id:API-KEY

######Get region list (Get DC ID)
fab -f vultr.py get_region_list

######Get plan list (Get plan ID)
fab -f vultr.py get_plan_list

######Test if region A available plan B
fab -f vultr.py is_region_available_plan:REGION_A_ID,PLAN_B_ID

######Get OS list (Get OS ID)
fab -f vultr.py get_os_list

######Create server (use parameter LABEL to set server name.)
fab -f vultr.py create_server:API_KEY,LABEL,DC_ID,PLAN_ID,OS_ID

######Wait until server installed and start success.
fab -f vultr.py wait_until_ok:API_KEY,LABEL

######Destroy server by LABEL
fab -f vultr.py destroy_server_by_label:API_KEY,LABEL

######Destroy server by SUBID
fab -f vultr.py destroy_server_by_id:API_KEY,SUBID

######Get ip by LABEL
fab -f vultr.py get_ip_by_label:API_KEY,LABEL


ssh
=====================