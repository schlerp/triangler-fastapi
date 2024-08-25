from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla import ModelView

from triangler_fastapi import models
from triangler_fastapi.persistence import engine

admin = Admin(engine, title="Triangler FastAPI")

admin.add_view(ModelView(models.Experiment, icon="fas fa-flask"))
admin.add_view(ModelView(models.SampleFlight, icon="fas fa-list"))
admin.add_view(ModelView(models.Observation, icon="fas fa-comment"))
admin.add_view(ModelView(models.SampleFlightToken, icon="fas fa-id-card"))
