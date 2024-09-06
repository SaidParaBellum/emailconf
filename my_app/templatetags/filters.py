from django import template

register = template.Library()

@register.filter
def mask_email(email):
    try:
        username, domain = email.split('@')
        masked_username = f"{username[:2]}{'*' * (len(username) - 2)}"
        return f"{masked_username}@{domain}"
    except ValueError:
        return email