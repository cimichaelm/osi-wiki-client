#/usr/bin/python3

from xwikiclient import Client
import json
import replaceConfluence as rc

wikiurl = 'http://wiki.example.org/rest/'
username = "JohnDoe"
password = "TopSecret!"
# optional parameter: wiki defaults to "xwiki"
client = Client(wikiurl, username, password)

result = client.spaces()
print (json.dumps(result, sort_keys = True, indent = 4))

result = client.space_names()
print (result)

Short = False
Long = False

if Short:
    # optional parameters: page defaults to "WebHome", language defaults to None
    rc.fix_page(client, "TST.Test Home.Some.Structure - Templates.More Depth.My Page with a \. Dot")
elif Long:
    # optional parameters: page defaults to "WebHome", language defaults to None
    data = client.page("TST.Test Home.Some.Structure - Templates.More Depth.My Page with a \. Dot")
    content = data["content"]
    print(content)

    content = rc.replace_IncludeFirstParagraphWithoutHeading(content)
    content = rc.replace_IncludeDocument(content)
    print(content)
    #data["content"] = content
    #result = client.update_page(data)
    #print(result)
