# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery_config import app as celery_app

all = ('celery_app',)

# brew services start redis
# brew services info redis
# brew services stop redis