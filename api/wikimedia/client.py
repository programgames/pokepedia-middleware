import requests
import json

from api.wikimedia import wikimedia_session
from exception.exceptions import InvalidResponse


class WikimediaClient:

    def parse(self, url: str) -> dict:
        content = requests.get(url)
        json = content.json()

        if 'parse' not in json:
            raise InvalidResponse('Invalid response from url {}, parse information is missing'.format(url))

        return json

    def edit(self, endpoint: str, parameters: dict):

        content = wikimedia_session.post(endpoint, data=parameters)

        result = json.loads(content.content)

        if 'error' in result:
            raise InvalidResponse('Invalid response from url {} , error {}'.format(endpoint, result))

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
                    section_title = line
                else:
                    section_title = section_title[0:pos + 2] + line
                sections[section_title] = section['index']
            elif level_cursor < level:
                section_title += '//' + line
                level_cursor = level
                sections[section_title] = section['index']
            else:
                for i in range(level, level_cursor + 1):
                    pos = section_title.rfind('//')
                    if pos == -1:
                        section_title = ''
                    else:
                        section_title = section_title[0:pos]
                if not section_title:
                    section_title = line
                else:
                    section_title += '//' + line
                level_cursor = level
                sections[section_title] = section['index']

        return sections