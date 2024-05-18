from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph

from calculator_app import models
  # Імпортуємо ваші моделі Django

# Створюємо метадані бази даних з моделей Django
metadata = MetaData()

# Отримуємо таблиці з моделей Django
tables = [model.__table__ for model in [models.ProUser, models.CalculationHistory, models.ConversionHistory]]

# Додаємо таблиці до метаданих
for table in tables:
    table.tometadata(metadata)

# Створюємо граф структури бази даних
graph = create_schema_graph(metadata=metadata)

# Зберігаємо граф у файл
graph.write_png('database_schema.png')
