
# create_tables.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from core.database import engine
from core.models import Base
from core.models import OrderAction
# This will create all tables defined in models.py
Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")
