from background_task import background
from .models import Page
from datetime import datetime, timezone

# Expiration period in seconds
TIME_PERIOD = 24 * 60 * 60


def get_delta(page):
    now = datetime.now(timezone.utc)
    image_date = page.time
    return now - image_date


@background(schedule=5)
def delete_expired_images():
    print('Task started!')
    pages = Page.objects.all()
    for page in pages:
        delta = get_delta(page)
        if delta.total_seconds() > TIME_PERIOD:
            print('Image name: ', page.image.name)
            print('Total seconds: ', delta.total_seconds())
            print('Expiration period: ', TIME_PERIOD)
            page.image.delete(save=True)
            page.delete()
    print('Task end!')


