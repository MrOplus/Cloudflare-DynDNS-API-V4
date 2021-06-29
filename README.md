# Cloudflare DynDNS (API v4)
Update Cloudflare DNS Record with client's IP Address using IP-API and Cloudflare API V4  


## Parameters :  
```
-s/--secret API Secret Key  
-e/--email Email Address  
-z/--zone Zone Name ( ex : koorosh.dev )  
-d/--domain Domain Name ( ex : test.koorosh.dev )  
```

## Required Packages :  
```
requests
```

## Installation :  
```
*/5 * * * * $(which python3) /opt/Cloudflare-DynDNS-API-V4/Cloudflare.py -s ************** -e admin@local.com -z whatever.com -d record.whatever.com
```
