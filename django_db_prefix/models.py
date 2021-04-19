from django.conf import settings
from django.db.models.signals import class_prepared

def add_db_prefix(sender, **kwargs):
    prefix = getattr(settings, "DB_PREFIX", None)
    app_label = sender._meta.app_label.lower()
    app_label_wildcard = app_label + ".*"
    sender_name = sender._meta.object_name.lower()
    full_name = app_label + "." + sender_name
    replace_app_label = False
    if isinstance(prefix, dict):
        if full_name in prefix:
            prefix = prefix[full_name]
        elif app_label in prefix:
            prefix = prefix[app_label]
        elif app_label_wildcard in prefix:
            prefix = prefix[app_label_wildcard]
            replace_app_label = True
        else:
            prefix = prefix.get(None, None)

    if prefix:
        if replace_app_label:
            sender._meta.db_table = prefix + sender_name
        else:
            sender._meta.db_table = prefix + sender._meta.db_table

class_prepared.connect(add_db_prefix)
