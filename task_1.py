import csv

filename = "db\data.csv"
filename_out = "db\data_out.csv"

# Чтение csv файла
with open(filename) as r_file:
    file_reader = csv.reader(r_file, delimiter=";")
    # Отделяем шапку
    header = next(file_reader)
    # Создание списка из таблицы
    main_list = list(file_reader)

# Создание сортированного списка дат
date_list = []

for date in main_list:
    if date[3] not in date_list:
        date_list.append(date[3])

date_list.sort()

# Создание сортированного списка точек продаж
pos_list = []

for pos in main_list:
    if int(pos[1]) not in pos_list:
        pos_list.append(int(pos[1]))

pos_list.sort()

# Создание вложенного словаря {дата: {точка: сумма}...}
main_dict = {}

for date in date_list:
    if date not in main_dict:
        main_dict.update({date: {}})

for date in main_dict:
    for pos in pos_list:
        main_dict[date].update({pos: 0})

# Заполнение словаря суммами кредитов из таблицы
for line in main_list:
    date = main_dict[line[3]]
    amount = round(float(date[int(line[1])]), 2)
    date[int(line[1])] = round((amount + float(line[2])), 2)

# Создание словаря с общими суммами продажи за день
total_dict = {}

for date in main_dict:
    amount = 0
    for pos in main_dict[date]:
        amount += round(main_dict[date][pos], 2)
    total_dict.update({date: amount})

# Подготовка расчетного списка для создания csv файла
line_list = []

for date in main_dict:
    some_li = []
    some_li.append(date)
    for pos in main_dict[date]:
        some_li.append(round(main_dict[date][pos], 2))
        some_li.append(f"{round(((main_dict[date][pos] * 100) / total_dict[date]), 2)}%")
    line_list.append(some_li)

# Создание списка с дублированием точек для шапки таблицы
new_pos = []
for i in pos_list:
    for _ in range(2):
        new_pos.append(i)

# Выгрузка в csv файл
with open(filename_out, 'w') as w_file:
    file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
    file_writer.writerow(["DATE/POS", *new_pos])
    file_writer.writerows(line_list)
