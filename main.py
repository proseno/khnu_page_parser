import html_parser
import config


def parse(url: str):
    response = html_parser.prepare_data(url)
    return response


print(parse(config.site_url))
