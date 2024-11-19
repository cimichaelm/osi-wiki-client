#/usr/bin/python3

import requests
import argparse

from xwikitools.xwikiclient import Client
import json

from requests.auth import HTTPBasicAuth

class xwikitool:
    def __init__(self, api_root, auth_user=None, auth_pass=None, wiki="xwiki"):

        self.api_root = api_root
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.wiki = wiki

        self.client = None

    def get_pages(self, url, username, password):
        response = requests.get(f"{url}/rest/wikis/xwiki/spaces", auth=HTTPBasicAuth(username, password))
        response.raise_for_status()
        return response.json()
    
    def create_hierarchy(self, page_title):
        components = page_title.split('/')
        hierarchy = {}
        current_level = hierarchy
        for component in components:
            current_level[component] = {}
            current_level = current_level[component]
        return hierarchy
    
    def process(self):
        """
        """
        
        # optional parameter: wiki defaults to "xwiki"
        client = Client(self.api_root, self.auth_user, self.auth_pass)
        if client:
            self.client = client
        
            result = client.spaces()
            if result:
                print (json.dumps(result, sort_keys = True, indent = 4))
            
            result = client.space_names()
            if result:
                print (result)
        
        if False:
            pages = get_pages(args.url, args.username, args.password)
        
            for page in pages['spaces']:
                page_title = page['name']
                if '/' in page_title:
                    hierarchy = create_hierarchy(page_title)
                    print(f"Hierarchy for {page_title}: {hierarchy}")
    
def main():
    """
    """
        
    parser = argparse.ArgumentParser(description="Scan XWiki pages and create a hierarchy of sub pages.")
    parser.add_argument('--url', required=True, help='URL of the XWiki')
    parser.add_argument('--username', required=True, help='Username for XWiki')
    parser.add_argument('--password', required=True, help='Password for XWiki')
    
    args = parser.parse_args()
    
    wt = xwikitool(args.url, args.username, args.password )
    wt.process()

if __name__ == "__main__":
    main()
