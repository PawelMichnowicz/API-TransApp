from providers.factory import get_providers
from celery_worker import reverse


print(reverse.delay("deeeEdsasfAAAA"))


a = {key: val.__name__ for key, val in get_providers().items()}

print(a)