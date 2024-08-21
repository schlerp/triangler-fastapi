from datetime import datetime
from datetime import timezone
from functools import partial

utcnow = partial(datetime.now, timezone.utc)
