from xwikiclient import Client
import re

def replace_IncludeFirstParagraphWithoutHeading(content):
    while True:
        excerptInclude = '{{excerpt-include nopanel="true" 0=""/}}'
        m = re.search(f'\[\[doc:([^\]]*)\]\]\n\n{excerptInclude}', content)
        if m:
            page = m.groups(1)[0]
            content = content.replace(
                f'[[doc:{page}]]\n\n{excerptInclude}',
                '{{' + f'include reference="{page}" section="HInclude" excludeFirstHeading="true"/' + '}}\n')
        else:
            break
    return content

def replace_IncludeDocument(content):
    while True:
        excerptInclude = '{{excerpt-include 0=""/}}'
        m = re.search(f'\[\[doc:([^\]]*)\]\]\n\n{excerptInclude}', content)
        if m:
            page = m.groups(1)[0]
            content = content.replace(
                f'[[doc:{page}]]\n\n{excerptInclude}',
                '{{' + f'include reference="{page}"/' + '}}\n')
        else:
            break
    return content

def fix_page(client, path):
    data = client.page(path)
    content = data["content"]
    print(content)

    content = replace_IncludeFirstParagraphWithoutHeading(content)
    content = replace_IncludeDocument(content)
    print(content)
    data["content"] = content
    result = client.update_page(data)
    print(result)
