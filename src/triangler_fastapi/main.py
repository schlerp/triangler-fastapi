from triangler_fastapi.data import persistence
from triangler_fastapi.entrypoints import get_application

persistence.run_migrations()
app = get_application()
