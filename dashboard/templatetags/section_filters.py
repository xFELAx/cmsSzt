from django import template
import re
from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def get_header_part(content, part):
    try:
        soup = BeautifulSoup(content, 'html.parser')
        if part == 'pretitle':
            return soup.select_one('.section-header__pretitle').get_text(strip=True)
        elif part == 'primary':
            return soup.select_one('.section-header__primary h2').get_text(strip=True)
        elif part == 'secondary':
            return soup.select_one('.section-header__secondary p').get_text(strip=True)
    except:
        return ''

@register.filter
def get_list_items(content):
    try:
        soup = BeautifulSoup(content, "html.parser")
        items = []
        for item in soup.select(".list-block__item"):
            # Get the title text
            title_element = item.select_one(".list-block__title h3")
            # Get the content HTML including the <p> tag
            content_element = item.select_one(".list-block__text")

            if title_element and content_element:
                items.append(
                    {
                        "title": title_element.get_text(strip=True),
                        "content": "".join(
                            str(tag) for tag in content_element.contents
                        ).strip(),
                    }
                )
        return items
    except Exception as e:
        print(f"Error parsing list items: {e}")
        return []


@register.filter
def get_footer_part(content, part):
    """Enhanced footer part extraction"""
    if not content:
        return ""

    patterns = {
        "pretitle": r'<h3[^>]*class="[^"]*section-header__pretitle[^"]*"[^>]*>(.*?)</h3>',
        "primary": r'<div[^>]*class="[^"]*section-header__primary[^"]*"[^>]*>(.*?)</div>',
        "secondary": r'<div[^>]*class="[^"]*section-header__secondary[^"]*"[^>]*>(.*?)</div>',
    }

    if part in patterns:
        match = re.search(patterns[part], content, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""
