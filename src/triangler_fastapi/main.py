from triangler_fastapi.entrypoints import get_application
from triangler_fastapi.persistence import run_migrations

run_migrations()
app = get_application()
