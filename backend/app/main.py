from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.organization import router as organization_router
from app.routers.lines import router as lines_router
from app.routers.line_assignment import router as line_assignment_router
from app.routers.line_status import router as line_status_router
from app.routers.layouts import router as layouts_router
from app.routers.layout_machines import router as layout_machines_router

app = FastAPI(
    title="SFMS API",
    description="Sewing Floor Management System",
    version="1.0.0",
)


app.include_router(organization_router)
app.include_router(lines_router)
app.include_router(line_assignment_router)
app.include_router(line_status_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(layouts_router)
app.include_router(layout_machines_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "SFMS API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }