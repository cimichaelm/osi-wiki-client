import requests

class Client:
    def __init__(self, api_root, auth_user=None, auth_pass=None, wiki="xwiki"):
        self.api_root = api_root
        self.auth_user = auth_user
        self.auth_pass = auth_pass
        self.wiki = wiki

    def _build_url(self, path):
        url = self.api_root + "/".join(path)
        return url

    def _make_request(self, path, data):
        url = self._build_url(path)
        data['media'] = 'json'

        auth = None
        if self.auth_user and self.auth_pass:
            auth = self.auth_user,self.auth_pass

        response = requests.get(url, params=data, auth=auth)
        response.raise_for_status()
        return response.json()

    def _make_put(self, path, data):
        url = self._build_url(path)
        data['media'] = 'json'

        auth = None
        if self.auth_user and self.auth_pass:
            auth = self.auth_user,self.auth_pass

        response = requests.put(url, data=data, auth=auth)
        response.raise_for_status()
        return response.status_code

    def spaces(self):
        path = []
        if self.wiki:
            path.append('wikis')
            path.append(self.wiki)
        path.append('spaces')
        data = {}
        content = self._make_request(path, data)
        return content['spaces']

    def space_names(self):
        spaces = []
        result = self.spaces()
        for details in result: 
            spaces.append(details['name'])
        return spaces

    def pages(self, space):
        path = []
        if self.wiki:
            path.append('wikis')
            path.append(self.wiki)
        path.append('spaces')
        path.append(space)
        path.append('pages')
        data = {}
        content = self._make_request(path, data)
        return content['pageSummaries']

    def page_names(self, space):
        pages = []
        result = self.pages(space)
        for details in result: 
            pages.append(details['name'])
        return pages

    def calculate_path(self, space, page, language = None):
        path = []
        if self.wiki:
            path.append('wikis')
            path.append(self.wiki)
        space = space.replace("\.", "ESCAPED_DOT")
        for space in space.split("."):
            path.append("spaces")
            path.append(space.replace("ESCAPED_DOT", '.'))
        path.append("pages")
        path.append(page)
        if language:
            path.append("translations")
            path.append(language)
        return path

    def page(self, space, page = "WebHome", language = None):
        path = self.calculate_path(space, page, language)
        data = {}
        content = self._make_request(path, data)
        return content

    def tags(self):
        path = ['tags']
        data = {}
        content = self._make_request(path, data)
        return content['tags']

    def tag_names(self):
        tags = []
        result = self.tags()
        for details in result:
            tags.append(details['name'])
        return tags

    def pages_by_tags(self, tags):
        taglist = ",".join(tags)
        path = ['tags', taglist]
        data = {}
        content = self._make_request(path, data)
        return content['pageSummaries']

    def submit_page(self, space, page, content, title=None, parent=None, language=None):
        path = self.calculate_path(space, page, language)
        data = {'content': content}
        if title:
            data['title'] = title
        else:
            data['title'] = page

        if parent:
            data['parent'] = parent

        status = self._make_put(path, data)

        if status == 201:
            return "Created"
        elif status == 202:
            return "Updated"
        elif status == 304:
            return "Unmodified"

    def update_page(self, data):
        path = self.calculate_path(data["space"], data["name"], data["language"])

        status = self._make_put(path, data)

        if status == 201:
            return "Created"
        elif status == 202:
            return "Updated"
        elif status == 304:
            return "Unmodified"
