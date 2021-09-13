import requests
import json
import re

from exception.exceptions import InvalidResponse


class WikimediaClient:
    def parse(self, url: str) -> dict:
        content = requests.get(url)
        json = content.json()

        if 'parse' not in json:
            raise InvalidResponse('Invalid response from url {}, parse information is missing'.format(url))

        return json

    def edit(self, endpoint: str, parameters: list):

        cookies = self.parse_cookie_file('cookie.txt')

        content = requests.post(endpoint, params=parameters, cookies=cookies)

        jsonArray = json.loads(content.json())

        if not 'edit' not in jsonArray and 'Success' not in jsonArray['edit']['result']:
            raise InvalidResponse('Invalid response from url {}, parse information is missing'.format(endpoint))

    def format_section_by_url(self, url: str) -> dict:
        content = self.parse(url)

        sections = {}

        level_cursor = 2
        section_title = ''

        for section in content['parse']['sections']:
            level = int(section['level'])
            line = section['line'].replace('<i>', ' ', ).replace('</i>', ' ').strip()

            if not section_title:
                section_title = line
            if level_cursor == level:
                pos = section_title.rfind('//')
                if pos == -1:
                    section_title = False
                else:
                    section_title = section_title[0:pos]
                if not section_title:
                    section_title = line
                else:
                    section_title += '//' + line
                sections[section_title] = section['index']
            elif level_cursor < level:
                section_title += '//' + line
                level_cursor = level
                sections[section_title] = section['index']
            else:
                for i in range(level, level_cursor + 1):
                    pos = section_title.rfind('//')
                    if pos == -1:
                        section_title = False
                    else:
                        section_title = section_title[0:pos]
                if not section_title:
                    section_title = line
                else:
                    section_title += '//' + line
                level_cursor = level
                sections[section_title] = section['index']

        return sections

    def parse_cookie_file(self, cookiefile):
        """Parse a cookies.txt file and return a dictionary of key value pairs
        compatible with requests."""

        cookies = {}
        with open(cookiefile, 'r') as fp:
            for line in fp:
                if not re.match(r'^\#', line):
                    line_fields = line.strip().split('\t')
                    cookies[line_fields[5]] = line_fields[6]
        return cookies
