from fastapi import FastAPI
from app.core.config import settings
from app.api.routes import staff_controller, shift_controller, schedule_controller

app = FastAPI(title=settings.APP_NAME)

app.include_router(staff_controller.router, prefix=f"{settings.API_V1_PREFIX}/staff", tags=["Staff"])
app.include_router(shift_controller.router, prefix=f"{settings.API_V1_PREFIX}/shifts", tags=["Shifts"])
app.include_router(schedule_controller.router, prefix=f"{settings.API_V1_PREFIX}/schedule", tags=["Schedule"])
