from django import template
import re

register = template.Library()


@register.filter
def get_footer_part(content, part):
    if not content:
        return ""

    patterns = {
        "pretitle": r'<h3 class="column lg-12 section-header__pretitle text-pretitle">(.*?)</h3>',
        "primary": r'<div class="column lg-6 stack-on-1100 section-header__primary">(.*?)</div>',
        "secondary": r'<div class="column lg-6 stack-on-1100 section-header__secondary">(.*?)</div>',
    }

    if part in patterns:
        match = re.search(patterns[part], content, re.DOTALL)
        if match:
            return match.group(1).strip()
    return ""
