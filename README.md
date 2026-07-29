# Data Science & ML Engineering Portfolio

Репозиторий содержит проекты, выполненные в рамках 2-летней программы «Профессия Data Scientist» (специализация: ML Engineer) от Skillfactory. Проекты охватывают полный цикл: от EDA и статистического анализа до построения ML-моделей, Causal Inference, обёртки в Docker API и настройки MLOps-мониторинга.

📍 **Локация:** Грузия (Remote)  
🎓 **Образование:** Skillfactory — Data Scientist / ML Engineer (2 года)  
✉️ **Контакты:** [Telegram](https://t.me/RivlexDS) · leecosmartfon@gmail.com

## Главные проекты

### [Предсказание цены недвижимости](module_7_final/) — итоговый проект 1-го года

Сервис для предсказания стоимости домов на основе исторических данных о предложениях (377K записей, 18 признаков).

- **Задача:** регрессия — прогнозирование цены недвижимости
- **Данные:** числовые, категориальные и бинарные признаки; очистка, обработка пропусков, извлечение признаков из вложенных JSON-полей (homeFacts, schools)
- **Модели:** создание и сравнение нескольких ML-моделей, выбор лучшей
- **Production:** Docker-контейнер с REST API (Flask), клиент для тестирования
- **Стек:** Python, Pandas, scikit-learn, Flask, Docker

---

### [Рекомендательная система для e-commerce](module_10_final/) — итоговый проект 2-го года

Персонализированная система рекомендаций товаров (Top-3) для e-commerce ритейлера на данных о 2.7M событий пользователей.

- **Задача:** рекомендация товаров с метрикой Precision@3
- **Данные:** 2.7M событий, 1.4M пользователей, 235K товаров, иерархия категорий (1669), свойства товаров (1104 признака)
- **Модели:** Baseline (0.61%), NMF (0.13% на тесте), LightFM (1.52% на валидации / 0.15% на тесте). Проведён анализ переобучения: падение LightFM в 10 раз, регуляризация 1e-4 улучшает тест до 0.3%
- **Production:** Docker-контейнер с REST API (Flask), эндпоинты `/health`, `/metrics`, `/recommend`, обработка холодного старта и некорректных запросов
- **Стек:** LightFM, Flask, Docker, SciPy, Pandas, NumPy
- **Оценка ментора:** 25/25

## Практические мини-проекты (2-й год)

| Проект | Ключевые темы | Результат |
|--------|--------------|-----------|
| [A/A/B-тестирование](module_9/ab_testing.ipynb) | Статистические тесты, SciPy, Statsmodels | Выявлен сбой сплит-системы (A/A-тест провален) |
| [Детектирование аномалий](module_9/anomaly_detection.ipynb) | Isolation Forest, DBSCAN, Z-score, IQR | 9 аномальных дней; комбинация методов наиболее устойчива |
| [Байесовские методы](module_9/bayesian_methods.ipynb) | PyMC3, линейная регрессия, MCMC | Регрессия с доверительными интервалами для каждого коэффициента |
| [Uplift-моделирование](module_9/uplift_modeling.ipynb) | CausalML, S/T-Learner, Qini-score | S-Learner — лучший qini-score (2169.5) без переобучения |
| [Мониторинг ML-моделей](module_9/wine_quality_monitoring.ipynb) | LightGBM, Prometheus, Grafana, MLOps | Пайплайн сбора метрик модели в реальном времени |

## Проекты 2-го года

| Модуль | Проект | Описание |
|--------|--------|----------|
| [module_8](module_8/) | Прогнозирование объёмов продаж | Временные ряды: Prophet, LightGBM, CatBoost |
| [module_9](module_9/) | Мини-проекты (5 шт.) | A/B-тесты, аномалии, байесовские методы, uplift, мониторинг |
| [module_10_final](module_10_final/) | Рекомендательная система | Дипломный проект: LightFM + Docker API |

## Проекты 1-го года

| Модуль | Проект | Описание |
|--------|--------|----------|
| [module_0](module_0/) + [Крестики-нолики](tick_tack_toe/) | Основы Python и игра | Бинарный поиск числа, OOP: игра «Крестики-нолики» |
| [module_2](module_2/) | Разведывательный анализ данных | EDA: влияние условий жизни на успеваемость |
| [module_3](module_3/) | Предсказание рейтинга TripAdvisor | ML: предсказание рейтинга ресторана |
| [module_4](module_4/) | Анализ авиарейсов | EDA: исследование данных о перелётах |
| [module_5](module_5/) | Кредитный скоринг | Классификация: предсказание дефолта клиента |
| [module_6](module_6/) | RFM-анализ клиентов | Сегментация клиентов по покупательской способности |
| [module_7_final](module_7_final/) | Предсказание цены недвижимости | Финальный проект 1-го года: регрессия + Docker API |

## Стек

**Язык и данные:** Python, Pandas, NumPy, SciPy, Pandas Profiling

**Machine Learning:** scikit-learn, LightGBM, XGBoost, CatBoost, LightFM

**Advanced ML & Stats:** PyMC3 (Bayesian), CausalML (Uplift), Statsmodels (A/B), Prophet (Time Series), Optuna (Hyperparameter Tuning)

**MLOps & Deployment:** Docker, Flask, Prometheus, Grafana

**Визуализация:** Matplotlib, Seaborn, Plotly
