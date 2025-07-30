from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla import ModelView

from triangler_fastapi.data import models
from triangler_fastapi.data import persistence

admin = Admin(persistence.get_engine(), title="Triangler FastAPI")

admin.add_view(ModelView(models.Experiment, icon="fas fa-flask"))
admin.add_view(ModelView(models.SampleFlight, icon="fas fa-list"))
admin.add_view(ModelView(models.Response, icon="fas fa-comment"))
admin.add_view(ModelView(models.SampleFlightToken, icon="fas fa-id-card"))
