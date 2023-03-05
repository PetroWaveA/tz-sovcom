import csv
import plotly.graph_objects as go
from datetime import datetime

filename_out = "db\data_out.csv"

# Открываем файл и формируем глобальный список
with open(filename_out) as r_file:
    file_reader = csv.reader(r_file, delimiter=";")
    header = next(file_reader)
    main_list = list(file_reader)

# Формируем список дат
date_list = []
for line in main_list:
    date = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')
    date_list.append(date)

# Формируем список точек продаж
pos_list = []
for i in range(len(header)):
    if i == 0:
        pass
    else:
        pos_list.append(int(header[i]))

# Создаем график суммы выдач
fig = go.Figure()

for i in range(len(pos_list)):
    amount_list = []

    if i % 2 != 0:
        for line in main_list:
            amount_list.append(float(line[i]))

    fig.add_trace(
        go.Scatter(
            x=date_list,
            y=amount_list,
            name=f"{pos_list[i]}"
        ))

fig.update_layout(yaxis_title="Сумма кредита",
                  xaxis_title="Дата",
                  title="Сумма выдач",
                  legend_title="Точка продажи",
                  title_font_size=24)

# Создаем график суммы выдач по процентам
fig_p = go.Figure()

for i in range(len(pos_list)):
    amount_list = []
    if i % 2 == 0:
        for line in main_list:
            if i == 0:
                n = line[i+2]
                amount_list.append(float(n[:-1]))
            else:
                n = line[i]
                amount_list.append(float(n[:-1]))

    fig_p.add_trace(
        go.Scatter(
            x=date_list,
            y=amount_list,
            name=f"{pos_list[i]}"
        ))

fig_p.update_layout(yaxis_title="Сумма кредита %",
                    xaxis_title="Дата",
                    title="Сумма выдач %",
                    legend_title="Точка продажи",
                    title_font_size=24)

# Открываем оба графика
fig.show()
fig_p.show()
