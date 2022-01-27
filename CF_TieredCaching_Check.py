import requests
import getpass
import json
import csv
import os

# You can use this script as reference for some CF API automation.
# Robert John P. Canare | Jan 26, 2022

cloudflareEmail = input("Email: ")
cloudflareToken = input("API Token: ")
cloudflareAccountName = input("CF Account Name: ")
cloudflareID = input("CF Account ID: ")
file_object = open('ATC_StatusCheck_Output.txt', 'a')

header = {'X-Auth-Email': cloudflareEmail, 'X-Auth-Key': cloudflareToken, 'Content-Type': "application/json"}


def listDomainsTieredCachingValue():
    r = requests.get(
        url=f"https://api.cloudflare.com/client/v4/zones?account.id={cloudflareID}&account.name={cloudflareAccountName}&page=1&per_page=800&order=status&direction=desc&match=all",
        headers=header)
    jsonElements = json.loads(r.text)
    domain_names = jsonElements["result"]
    file_object.write(f"""{cloudflareAccountName}\n""")
    for i in domain_names:
        domain_id = i["id"]
        domain_name = i["name"]
        # print(domain_id)
        r = requests.get(url=f"https://api.cloudflare.com/client/v4/zones/{domain_id}/argo/tiered_caching",
                         headers=header)
        jsonElements = json.loads(r.text)
        tiered_caching = jsonElements["result"]["id"]
        tiered_value = jsonElements["result"]["value"]
        print(f"""{domain_name} {tiered_caching} {tiered_value}""")
        file_object.write(f"""{domain_name} {tiered_caching} {tiered_value}\n""")


listDomainsTieredCachingValue()
cwd = os.getcwd()

print(f"""Done, output it's on {cwd}.""")

file_object.close()
