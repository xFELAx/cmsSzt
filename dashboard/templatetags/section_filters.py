from django import template
import re
from bs4 import BeautifulSoup

register = template.Library()

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
