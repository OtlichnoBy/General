# Рекомендательная система для e-commerce

Дипломный проект 2-го года обучения DS/ML в Skillfactory (трек ML-инженер). Максимум баллов — 25/25 от ментора.

## О проекте

Имитация реальной работы junior ML-инженера в команде, создающей рекомендательную систему для e-commerce ритейлера. Бизнес-задача — повысить допродажи на 20% через персонализированные рекомендации на главной странице магазина (3 слота).

**Целевая метрика:** Precision@3 (точность топ-3 рекомендаций)
**Baseline:** 0.61% (рекомендация популярных товаров)

## Данные

- **2 756 101** событий за период май–сентябрь 2015
- **1 407 580** уникальных посетителей
- **235 061** уникальных товаров
- **1 669** категорий с иерархической структурой
- **1 104** уникальных признака товаров

| Файл | Описание |
|------|----------|
| `events.csv` | События пользователей: timestamp, visitorid, event (view/addtocart/transaction), itemid, transactionid |
| `category_tree.csv` | Иерархия категорий: category_id, parent_id |
| `item_properties_part1.csv`, `item_properties_part2.csv` | Свойства товаров: timestamp, item_id, property (хешированные), value |

## Этапы работы

| Неделя | Этап |
|--------|------|
| 1 | Постановка задачи, выбор метрики, получение данных, первичный анализ |
| 2 | Feature engineering: факторы товаров, факторы пользователь-товар, временная валидация |
| 3 | Построение моделей (NMF, LightFM, XGBoost), подбор гиперпараметров |
| 4 | Обёртка модели в REST API сервис, Docker-контейнеризация, документация, презентация |

## Модели и результаты

| Модель | Precision@3 (val) | Precision@3 (test) | Примечание |
|--------|-------------------|---------------------|------------|
| Baseline (топ-3 товаров) | 0.61% | 0.61% | По числу транзакций до 01.07 |
| NMF | 0.41% | 0.13% | n_components=25 |
| LightFM | 1.52% | 0.15% | Гибридная модель с item features |

**Проблема переобучения:** LightFM показывает хороший результат на валидации, но падает на тесте — типичная проблема для рекомендательных систем при недостатке данных о взаимодействиях.

**XGBoost:** Модель подготовлена (признаки сгенерированы), но не доведена до рабочего состояния из-за ошибок в вычислении метрик.

## Структура репозитория

```
recommender_system_project.ipynb   # Основной ноутбук: EDA → Feature Engineering → Модели → Оценка
DOCS.md                             # Документация: данные, трансформации, API сервиса
presentation.pdf                    # Презентация результатов для бизнес-заказчика
requirements.txt                    # Зависимости Python
README.md                           # Описание проекта
```

## Production (Docker API)

Модель обёрнута в REST API сервис внутри Docker-контейнера:

### Запуск

```bash
docker load -i recommendation-service.tar
docker run --name recommendation-service -p 8000:8000 recommendation-service
```

### Эндпоинты

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/health` | Проверка состояния сервиса и модели |
| GET | `/metrics` | Параметры модели и данные обучения |
| POST | `/recommend` | Получение топ-k рекомендаций по `user_id` |

### Пример запроса

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{"user_id": 64, "k": 3}'
```

Полная документация API с примерами для Linux/macOS/Windows — в [DOCS.md](DOCS.md).

## Установка

```bash
pip install -r requirements.txt
```

## Использование

Открыть `recommender_system_project.ipynb` в Jupyter Notebook / JupyterLab.

## Стек

Python, Pandas, NumPy, SciPy, scikit-learn, LightFM, XGBoost, Matplotlib, Seaborn, Flask, Docker
