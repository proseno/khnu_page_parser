import requests
from bs4 import BeautifulSoup
import config

media_url = config.media_url


def get_html(url: str):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')


def validate_img(imgs: list):
    images = []
    for img in imgs:
        if img.startswith('data:image'):
            images.append(img)
        else:
            images.append(media_url + img)
    return images


def get_img_src(html):
    img_tags = html.findAll('img')
    src = []
    for img_tag in img_tags:
        src.append(img_tag.attrs['src'])
    return validate_img(src)


def get_a_href(html):
    a_tags = html.findAll('a')
    href = []
    for a_tag in a_tags:
        href.append(a_tag.attrs['href'])
    return validate_href(href)


def validate_href(hrefs: list):
    result = []
    for href in hrefs:
        if href.startswith('http'):
            result.append(href)
        else:
            result.append(media_url + href)
    return result


def prepare_data(url: str):
    html = get_html(url)
    response = 'The result of parsing page: ' + config.site_url + ' \n'
    if (config.images):
        image_urls = get_img_src(html)
        img_count = set_img_links(image_urls)
        response += 'Image tag count = ' + str(img_count) + ' ,details in img_links.txt\n'
    if (config.links):
        links = get_a_href(html)
        links_count = set_href(links)
        response += 'Links tag count = ' + str(links_count) + ' , details in links.txt'

    return response


def prepare_img_response(imgs: list):
    response = 'Image urls on the matched page: \n'
    for img in imgs:
        response += img + '\n'
    return response


def prepare_href_response(hrefs: list):
    response = 'Links on the matched page: \n'
    for href in hrefs:
        response += href + '\n'
    return response


def set_img_links(imgs: list):
    file = open('var/img_links.txt', 'w')
    content = prepare_img_response(imgs)
    file.write(content)
    file.close()
    return len(imgs)


def set_href(hrefs: list):
    file = open('var/links.txt', 'w')
    content = prepare_href_response(hrefs)
    file.write(content)
    file.close()
    return len(hrefs)
