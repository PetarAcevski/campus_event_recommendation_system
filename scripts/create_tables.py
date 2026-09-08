from backend.database import Base, engine
import backend.models

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")