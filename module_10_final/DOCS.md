---
title: Документация модели LightFM для рекомендательной системы
created: '2025-08-20T13:52:27.389Z'
modified: '2025-08-21T11:08:15.275Z'
---

# Документация модели LightFM для рекомендательной системы

## 1. Формат входных данных для обучения

### 1.1. Матрица взаимодействий (interactions)
- **Формат:** Разреженная матрица (CSR) взаимодействий пользователь-товар.
- **Размерность:** ~81,590 пользователей × ~90,942 товаров (после фильтрации).
- **Содержимое:** Взвешенные взаимодействия с весами событий:
  - `view`: 1.0
  - `addtocart`: 7.0
  - `transaction`: 35.0
- **Создание:** 
  - Извлечение пар `visitorid`-`itemid` из датасета событий.
  - Суммирование весов для каждой уникальной пары.
  - Плотность матрицы: ~0.0098% (высокая разреженность).

### 1.2. Матрица признаков товаров (item_features)
- **Формат:** Разреженная матрица токенов вида `feature_name=value`.
- **Признаки:**
  - Базовые: `categoryid`, `790` (цена), `available`, `888`, `283` (связанные товары).
  - Иерархические: `category_depth` (0–6), `parent_category`, `root_category`.
  - Производные: 
    - `price_numeric` (числовая цена из `790`).
    - `price_category` (низкая, средняя, высокая, премиум).
    - `related_items_count` (из `283`).
  - Дополнительно: `BIAS` для товаров без признаков.
- **Токенизация:** 182,706 уникальных токенов для 90,942 товаров.
- **Фильтрация:** Признаки ограничены товарами из отфильтрованного датасета событий.

### 1.3. Известные взаимодействия (known_csr)
- **Формат:** Разреженная матрица (CSR) для всех взаимодействий.
- **Назначение:** Исключение известных товаров из рекомендаций при оценке Precision@3.
- **Содержимое:** Пары пользователь-товар с ненулевыми весами.

---

## 2. Трансформации исходного датасета

### 2.1. Исходные данные
- **События (`events.csv`):** 2,756,101 записей (май–сентябрь 2015):
  - `timestamp`, `visitorid`, `event` (view, addtocart, transaction), `itemid`, `transactionid`.
- **Категории (`category_tree.csv`):** 1,669 записей (`categoryid`, `parentid`).
- **Свойства товаров (`item_properties_part1.csv`, `item_properties_part2.csv`):** 20,275,902 записей (`timestamp`, `itemid`, `property`, `value`).

### 2.2. Этапы предобработки
1. **Очистка:**
   - Удалено 3 записи с `visitorid=0` и 460 дубликатов.
   - Фильтрация: пользователи с <5 взаимодействий (с 1,407,580 до 81,590), товары с <5 взаимодействий (с 235,061 до 90,942).
   - Итог: 896,576 событий (32% от исходного).
2. **Конвертация типов:**
   - `categoryid` в `item_properties` преобразован из строк в числа для совместимости с `category_tree`.
   - Пропуски: числовые — 0, категориальные — `unknown`.
3. **Генерация признаков:**
   - Объединение `item_properties_part1.csv` и `item_properties_part2.csv` (4,121,722 записи после фильтрации).
   - Иерархические признаки: `category_depth`, `parent_category`, `root_category`.
   - Ценовые признаки: `price_numeric`, `price_category`.
   - Связанные товары: `related_items_count`.
4. **Матрицы взаимодействий:**
   - Агрегация пар `visitorid`-`itemid` с суммированием весов событий.
   - Создание CSR-матриц для train, validation, test.
5. **Токенизация признаков:**
   - Преобразование свойств товаров в токены `feature_name=value`.
   - Добавление `BIAS` для товаров без признаков.

---

## 3. Построение валидации

- **Метод:** Временное разбиение для предотвращения утечек.
- **Разбиение:**
  - **Train (72%):** 645,535 записей (май–август 2015, до 2015-08-01 05:44:19).
  - **Validation (8%):** 71,726 записей (первая половина августа 2015).
  - **Test (20%):** 179,315 записей (август–сентябрь 2015).
- **Точка отсечения:** 
  - Основная: 80-й процентиль (2015-08-14 12:01:13).
  - Train/validation: 2015-08-01 05:44:19.
- **Особенности:**
  - Хронологический порядок: train => validation => test.
  - Признаки товаров фильтруются по временной точке отсечения.
  - Precision@3 оценивается только по транзакциям, исключая известные товары.
- **Сохранение:** 
  - `train_final.pkl`, `val_events.pkl`, `test_events.pkl`.
  - Маппинги: `train_user_map.pkl`, `train_item_map.pkl`, `val_user_map.pkl`, `val_item_map.pkl`, `test_user_map.pkl`, `test_item_map.pkl`.

---

## 4. Проведённые эксперименты

### 4.1. Тип модели
- **Модель:** LightFM (гибрид коллаборативной и контентной фильтрации).
- **Библиотека:** `lightfm`.
- **Функция потерь:** WARP (оптимизация ранжирования).
- **Потоки:** 4 (обучение), 1 (оценка).

### 4.2. Гиперпараметры
- **Сетка:**
  - Веса: `view=1.0`, `addtocart=7.0`, `transaction=35.0`.
  - Факторы (`no_components`): [300, 400].
  - Эпохи: [35, 50, 65].
  - Регуляризация (`item_alpha`, `user_alpha`): [1e-6, 1e-5].
  - Потери: WARP.
  - Фиксированные: `learning_rate=0.03`, `random_state=42`.
- **Комбинаций:** 12.

### 4.3. Подбор гиперпараметров
- **Метрика:** Precision@3 (по транзакциям, исключая известные товары).
- **Оценка:** На валидационной выборке (154 пользователя с покупками).
- **Лучший результат:** Precision@3 = **1.52%** (2.5× лучше baseline 0.61%).
- **Параметры:**
  - Факторы: 300.
  - Эпохи: 65.
  - Регуляризация: 1e-5.
  - Веса: `view=1.0`, `addtocart=7.0`, `transaction=35.0`.
- **Сохранение:** `lightfm_best_params.pkl`.

### 4.4. Финальное обучение
- **Данные:** Train + validation (`train_final` + `val_events`).
- **Параметры:** Как в лучшей конфигурации (см. выше).
- **Время:** ~360 секунд.
- **Сохранение:** `lightfm_best_final.pkl` (модель, признаки, маппинги, параметры).

### 4.5. Тестовая оценка
- **Данные:** `test_events.pkl` (179,315 записей).
- **Метрика:** Precision@3 на 225 пользователях с покупками.
- **Результат:** Precision@3 = **0.15%** (хуже baseline 0.61% в 4 раза).
- **Причины:**
  - Переобучение (1.52% на валидации => 0.15% на тесте).
  - Различия в распределении данных.
  - Ограниченный размер тестовой выборки (225 пользователей).

---

## 5. Устройство сервиса и запуск Docker-образа

### 5.1. Общее устройство сервиса

**Технологический стек:**
- **Flask 2.3.3** - веб-фреймворк для REST API
- **LightFM 1.17** - гибридная рекомендательная модель  
- **NumPy 1.26.4** - вычисления с массивами
- **SciPy 1.11.1** - разреженные матрицы

**Функциональность:**
REST API для предоставления персонализированных рекомендаций на основе обученной модели LightFM.

**Основные компоненты:**
```
service/                         # корневая папка
├── src/                         # исходный код
│   └── app.py                   # Flask-приложение
├── models/                      # обученные модели
│   └── lightfm_best_final.pkl   # файл модели (переменная MODEL_PATH)
├── requirements.txt             # зависимости Python
└── Dockerfile                   # сборка Docker-образа
```

**Docker-конфигурация:**
- **База:** `python:3.9`
- **Системные пакеты:** `gcc`, `g++` (для компиляции LightFM)
- **Рабочий порт:** 8000
- **Переменная среды:** `MODEL_PATH=models/lightfm_best_final.pkl`

### 5.2. Запуск Docker-контейнера

#### 1. Загрузка образа (общая команда для всех ОС)
```bash
docker load -i recommendation-service.tar
```

#### 2. Проверка, свободен ли порт 8000
*Linux / macOS*
```bash
netstat -an | grep ':8000'
```
*Windows CMD*
```cmd
netstat -an | findstr :8000
```
*Windows PowerShell*
```powershell
netstat -an | Select-String ':8000'
```

#### 3. Запуск контейнера (общая команда для всех ОС)
```bash
docker run --name recommendation-service -p 8000:8000 recommendation-service
```


**Параметры команды:**
| Параметр | Описание |
|----------|----------|
| `--name recommendation-service` | Имя контейнера для управления |
| `-p 8000:8000` | Проброс порта: хост:контейнер (порт 8000 хоста => порт 8000 внутри контейнера) |
| `recommendation-service` | Имя Docker-образа |

---

## 6. API сервиса

### 6.1. Общая информация

| Параметр | Значение |
|----------|----------|
| **Протокол** | HTTP/1.1 |
| **Формат данных** | JSON |
| **Базовый URL** | `http://localhost:8000` |
| **Кодировка** | UTF-8 |

### 6.2. Эндпоинты

#### 6.2.1. GET /health — проверка состояния сервиса

**Описание:** Проверка состояния сервиса и готовности модели

**Запрос:**

*Linux / macOS*
```bash
curl http://localhost:8000/health
```

*Windows CMD*
```cmd
curl http://localhost:8000/health
```

*Windows PowerShell*
```powershell
Invoke-RestMethod http://localhost:8000/health
```

**Ответы:**

| Состояние  | Пример JSON |
|------------|-------------|
| сервис и модель готовы | `{"status":"healthy","model_loaded":true}` |
| модель не загружена    | `{"status":"unhealthy","model_loaded":false}` |

**Успешный (HTTP 200):**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

**Ошибка загрузки модели (HTTP 503):**
```json
{
  "status": "unhealthy", 
  "model_loaded": false
}
```

#### 6.2.2 GET /metrics — параметры модели

**Описание:** Информация о модели и её параметрах

**Запрос:**

*Linux / macOS*
```bash
curl http://localhost:8000/metrics
```

*Windows CMD*
```cmd
curl http://localhost:8000/metrics
```

*Windows PowerShell*
```powershell
Invoke-RestMethod http://localhost:8000/metrics
```

**Возможные ответы**

| HTTP | Когда происходит          | Пример тела |
|------|---------------------------|-------------|
| 200  | Модель загружена          | см. ниже  |
| 503  | Модель не загружена       | `{"error": "Model not loaded"}` |

**Ответ (HTTP 200):**
```json
{
  "model_type": "LightFM",
  "users_count": 62062,
  "items_count": 59841,
  "model_params": {
    "weights": {
      "view": 1.0,
      "addtocart": 7.0, 
      "transaction": 35.0
    },
    "factors": 300,
    "epochs": 65,
    "alpha": 1e-05,
    "loss": "warp"
  }
}
```

#### 6.2.3 POST /recommend — получение рекомендаций

**Описание:** Генерация персонализированных рекомендаций

**Параметры запроса:**

| Параметр | Тип | Обязательный | Описание | Ограничения |
|----------|-----|-------------|----------|-------------|
| `user_id` | int | Да | Идентификатор пользователя | Должен существовать в модели |
| `k` | int | Нет | Количество рекомендаций | 1 <= k <= 100, по умолчанию 3 |

**Примеры запросов:**

*Linux / macOS*  
```bash
curl -X POST http://localhost:8000/recommend -H "Content-Type: application/json" -d '{"user_id": 64, "k": 3}'
```

*Windows CMD*  
```cmd
curl -X POST http://localhost:8000/recommend -H "Content-Type: application/json" -d "{\"user_id\": 64, \"k\": 3}"
```

*Windows PowerShell*  
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/recommend" -Method Post -ContentType "application/json" -Body '{"user_id": 64, "k": 3}'
```

**Возможные ответы**

| HTTP | Когда происходит                                | Пример тела |
|------|------------------------------------------------|-------------|
| 200  | Успех                                          | см. ниже  |
| 400  | Ошибки клиента (нет user_id, k ≤ 0, k > 100, user_id не число) | `{"error":"k must be positive number"}` *(пример)* |
| 404  | Пользователь не найден                         | `{"error":"User 64 not found"}` |
| 503  | Сервис не готов (модель не загружена)          | `{"error":"Service unavailable"}` |

**Успешный ответ (HTTP 200):**
```json
{
  "user_id": 64,
  "recommendations": [
    {
      "item_id": 67890,
      "score": 0.1234,
      "rank": 1
    },
    {
      "item_id": 45678,
      "score": 0.0987,
      "rank": 2
    },
    {
      "item_id": 23456,
      "score": 0.0678,
      "rank": 3
    }
  ],
  "timestamp": 1698765432.123
}
```

### 6.3. Коды ошибок

| HTTP Код | Причина                         | Пример ответа                                    |
|----------|---------------------------------|--------------------------------------------------|
| **400**  | Некорректный запрос            | `{"error": "Please specify user_id"}`            |
| **400**  | Неверный тип данных            | `{"error": "user_id must be a number"}`          |
| **400**  | k <= 0                         | `{"error": "k must be positive number"}`         |
| **400**  | k > 100                        | `{"error": "k cannot be greater than 100"}`      |
| **404**  | Пользователь не найден         | `{"error": "User 12345 not found"}`              |
| **503**  | Сервис или модель недоступны   | `{"error": "Service unavailable"}`               |
| **500**  | Внутренняя ошибка сервера      | `{"error": "Internal server error"}`             |

### 6.4. Примеры использования

#### Проверка работоспособности (общая команда для всех ОС)
```bash
curl http://localhost:8000/health
```

#### Получение информации о модели (общая команда для всех ОС)
```bash
curl http://localhost:8000/metrics
```

#### Базовые рекомендации (топ-3)

*Linux / macOS*  
```bash
curl -X POST http://localhost:8000/recommend -H "Content-Type: application/json" -d '{"user_id": 64}'
```

*Windows CMD*  
```cmd
curl -X POST http://localhost:8000/recommend -H "Content-Type: application/json" -d "{\"user_id\": 64}"
```

*Windows PowerShell*  
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/recommend" -Method Post -ContentType "application/json" -Body '{"user_id": 64}'
```

#### Расширенные рекомендации (топ-10)

*Linux / macOS*  
```bash
curl -X POST http://localhost:8000/recommend -H "Content-Type: application/json" -d '{"user_id": 64, "k": 10}'
```

*Windows CMD*  
```cmd
curl -X POST http://localhost:8000/recommend -H "Content-Type: application/json" -d "{\"user_id\": 64, \"k\": 10}"
```

*Windows PowerShell*  
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/recommend" -Method Post -ContentType "application/json" -Body '{"user_id": 64, "k": 10}'
```

