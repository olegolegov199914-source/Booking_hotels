import csv
import io
import json
from datetime import datetime
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.users.dependencies import get_current_user
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings

router = APIRouter(prefix="/import", tags=["Импорт"])

TABLE_MODEL_MAP = {
    "hotels": Hotels,
    "rooms": Rooms,
    "bookings": Bookings,
}

# Поля, которые нельзя вставлять вручную (генерируемые)
SKIP_COLUMNS = ["id", "total_cost", "total_days"]

# Поля, которые нужно преобразовывать в числа
NUMERIC_COLUMNS = [
    "hotel_id", "price", "rooms_quantity", "image_id", "quantity",
    "room_id", "user_id"
]


@router.post("/{table_name}", status_code=status.HTTP_201_CREATED)
async def import_csv(
    table_name: str,
    file: UploadFile,
    local_kw: str = None,
    session: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    # 1. Проверка, что таблица существует
    model = TABLE_MODEL_MAP.get(table_name.lower())
    if not model:
        raise HTTPException(400, detail="Таблица не поддерживается")
    
    # 2. Чтение CSV
    content = await file.read()
    
    # Обработка кодировки
    try:
        csv_content = content.decode("utf-8")
    except UnicodeDecodeError:
        csv_content = content.decode("windows-1251")
    
    csv_file = io.StringIO(csv_content)
    reader = csv.DictReader(csv_file, delimiter=";")
    
    # 3. Преобразуем строки в список словарей
    rows = list(reader)
    if not rows:
        raise HTTPException(400, detail="Файл пуст")
    
    # 4. Преобразуем данные перед вставкой
    processed_rows = []
    for row in rows:
        processed_row = {}
        for key, value in row.items():
            # Пропускаем генерируемые поля
            if key in SKIP_COLUMNS:
                continue
            
            # Преобразуем числовые поля
            if key in NUMERIC_COLUMNS:
                if value and value.strip():
                    processed_row[key] = int(value)
                else:
                    processed_row[key] = None
            
            # Преобразуем даты
            elif key in ["date_from", "date_to"] and value:
                try:
                    # Пробуем формат DD.MM.YYYY
                    parsed_date = datetime.strptime(value, "%d.%m.%Y").date()
                    processed_row[key] = parsed_date
                except ValueError:
                    try:
                        # Пробуем формат YYYY-MM-DD
                        parsed_date = datetime.strptime(value, "%Y-%m-%d").date()
                        processed_row[key] = parsed_date
                    except ValueError:
                        # Если ничего не получилось, оставляем как есть
                        processed_row[key] = value
            
            # Преобразуем JSON-поля
            elif key in ["services", "servisces"] and value:
                try:
                    # Пробуем распарсить как JSON
                    json.loads(value)
                    processed_row[key] = value
                except json.JSONDecodeError:
                    # Если не получилось, заменяем двойные кавычки
                    fixed_value = value.replace('""', '"')
                    try:
                        json.loads(fixed_value)
                        processed_row[key] = fixed_value
                    except json.JSONDecodeError:
                        processed_row[key] = value
            else:
                processed_row[key] = value
        
        processed_rows.append(processed_row)
    
    if not processed_rows:
        raise HTTPException(400, detail="Нет данных для импорта")
    
    # 5. Вставка в БД
    stmt = model.__table__.insert().values(processed_rows)
    await session.execute(stmt)
    await session.commit()
    
    return {"rows_imported": len(processed_rows)}