# project_1
_Проект выполнинли:_

**Семёнова Екатерина Романовна**
**(ИСУ** 467417)
Парсинг, подготовка данных, анализ данных, визуализация

**Захарова Дарья Олеговна**
**(ИСУ** 465950)
Анализ данных, визуализация, dashboard

Проект анализирует и сравнивает погодные условия (температуру, осадки) в Москве, Санкт-Петербурге и Самаре на основе данных OpenWeatherMap API за 5 дней. Включает:

Наглядные графики изменений температуры и осадков.

Основную статистику (средние значения, максимумы/минимумы).

Удобное сравнение погоды в разных городах.

В ходе проекта мы рассчитали ключевые метрики: средняя, минимальная и максимальная температура, сумма осадков; Провели аналитику и выявили, что наибольшая средняя температура зафиксирована в Самаре (15.5°C), наименьшая — в Санкт-Петербурге (10.4°C), Москва оказалась самым дождливым городом (17.3 мм осадков), тогда как в Петербурге выпало всего 3.4 мм.

## Установка и запуск

```bash
git clone git@github.com:SemenovaCatherine/project_1.git && cd project_1 && \
python -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
streamlit run dashboard/app.py
