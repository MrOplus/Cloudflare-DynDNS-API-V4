import sys
from argparse import ArgumentParser
from typing import Optional
import requests


class HttpWrapper(object):
    def __init__(self, token, email) -> None:
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.headers = {
            "X-Auth-Email": email,
            "X-Auth-Key": token,
            "Content-Type": "application/json"
        }

    def get(self, url):
        res = requests.get(self.base_url + url, headers=self.headers)
        return res.json()

    def put(self, url, payload):
        res = requests.put(self.base_url + url, json=payload, headers=self.headers)
        return res.json()


class CloudFlare(object):
    def __init__(self, secret, email) -> None:
        self.http = HttpWrapper(secret, email)

    def get_user(self):
        res = self.http.get("/user")
        if res["success"]:
            return res["result"]
        else:
            return None

    def get_zone_id(self, zone) -> Optional[str]:
        res = self.http.get("/zones")
        if res["success"]:
            zones = res["result"]
            for z in zones:
                if z["name"] == zone:
                    return z["id"]

        return None

    def get_domain_id(self, zone_id, domain):
        res = self.http.get("/zones/{0}/dns_records".format(zone_id))
        if res["success"]:
            records = res["result"]
            for r in records:
                if r["name"] == domain:
                    return r["id"]

        return None

    def update_record(self, zone_id, domain_id, ipaddress, proxy):
        record = self.http.get("/zones/{0}/dns_records/{1}".format(zone_id, domain_id))
        if record["success"]:
            proxied = proxy
            if proxy is None:
                proxied = record["proxied"]
            record = record["result"]
            payload = {
                "type": record["type"],
                "name": record["name"],
                "content": ipaddress,
                "ttl": 1,
                "proxied": proxied
            }
            res = self.http.put("/zones/{0}/dns_records/{1}".format(zone_id, domain_id), payload)
            if res["success"]:
                return res["result"]
            return None


def fatal(msg):
    print(msg, file=sys.stderr)
    exit(255)


def start(args):
    cf = CloudFlare(args.secret, args.email)
    ipaddress = requests.get("http://ip-api.com/json").json()["query"]
    if cf.get_user() is None:
        fatal("[!] Invalid API Token")
    zone_id = cf.get_zone_id(args.zone)
    if zone_id is None:
        fatal("[!] Invalid Zone Name")
    domain_id = cf.get_domain_id(zone_id, args.domain)
    if domain_id is None:
        fatal("[!] Invalid Domain Name")
    record = cf.update_record(zone_id, domain_id, ipaddress, False)
    if record is not None:
        print("[+] Updated", record, sep="\n")
    else:
        fatal("[-] Unable to update record")


def opt_parser():
    parser = ArgumentParser()
    parser.add_argument("-s", "--secret", dest="secret",
                        help="API Secret Key", required=True)
    parser.add_argument("-e", "--email", dest="email",
                        help="Email Address", required=True)
    parser.add_argument("-z", "--zone", dest="zone",
                        help="Zone Name", required=True)
    parser.add_argument("-d", "--domain", dest="domain",
                        help="Domain Name", required=True)
    return parser.parse_args()


def main():
    args = opt_parser()
    start(args)


if __name__ == "__main__":
    main()
