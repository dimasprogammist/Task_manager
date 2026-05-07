import csv
import datetime

def add_task():
    title = input('\nВведите название задачи: ')
    if not title.strip():
        print('Название не может быть пустым!')
        return

    print('Приоритет:\n    1 - Высокий \n    2 - Средний \n    3 - Низкий')
    priority_choice = input('Выберите приоритет: ')

    priorities = {'1': 'высокий', '2': 'средний', '3': 'низкий'}
    if priority_choice not in priorities:
        print('Такого приоритета нет!')
        return

    priority = priorities[priority_choice]

    count = db.execute_one(
        """INSERT INTO todo.tasks (title, priority) VALUES (%s, %s)""",
        (title, priority)
    )

    if count > 0:
        print(f"Задача '{title}' добавлена!")
    else:
        print("Ошибка при добавлении задачи")

def show_all_tasks():
    print('Список всех задач: ')
    tasks = db.select(
        """
        SELECT id, title, priority, is_done, created_at 
        FROM todo.tasks
        ORDER BY created_at DESC
        """
    )

    for task in tasks:
        id = task[0]
        title = task[1]
        priority = task[2]
        is_done = 'Сделана' if task[3] else 'Не сделана'
        created_at = task[4].strftime("%d.%m.%Y %H:%M") if task[4] else "—"

        print(f'{id}  |  {title}  |  {priority}  |  {is_done}  |  {created_at}')

def show_tasks_sort():
    print('Список задач отсортированных по приоритету: ')
    tasks = db.select(
        """
        SELECT id, title, priority, is_done, created_at 
        FROM todo.tasks
        WHERE priority = %s 
        ORDER BY created_at DESC
        """,
        ('высокий',)
    )

    for task in tasks:
        id = task[0]
        title = task[1]
        priority = task[2]
        is_done = 'Сделана' if task[3] else 'Не сделана'
        created_at = task[4].strftime("%d.%m.%Y %H:%M") if task[4] else "—"

        print(f'{id}  |  {title}  |  {priority}  |  {is_done}  |  {created_at}')

def mark_as_done():
    chose_id = int(input('Выберите номер задачи для отметки выполнения: '))
    count = db.execute_one("""UPDATE todo.tasks SET is_done = TRUE WHERE id = %s""", (chose_id,))

    if count > 0:
        print(f"Задача №'{chose_id}' отмечена как завершенная!")
    else:
        print("Ошибка при завершении задачи")

def delite_task():
    chose_id = int(input('Выберите номер задачи для удаления: '))
    count = db.execute_one("""DELETE FROM todo.tasks WHERE id = %s""", (chose_id,))

    if count > 0:
        print(f"Задача №'{chose_id}' удалена!")
    else:
        print("Ошибка при удалении задачи")

def export_csv():
    task = db.select("""SELECT * FROM todo.tasks""")

    file_name = f"Tasks_{datetime.now().strftime('%d_%m_%Y___%H_%M_%S')}.csv"
    with open(file_name, 'w', encoding='cp1251',newline='') as file:
        write = csv.writer(file, delimiter=',')
        write.writerow(['ID',
                        'Текст задачи',
                        'Приоритет',
                        'Статус',
                        'Дата создания',
                        ])
        for t in task:
            write.writerow([t[0],
                            t[1],
                            t[2],
                            'Сделана' if t[3] else 'Не сделана',
                            t[4].strftime("%d.%m.%Y %H:%M") if t[4] else "—",
                            ])
        print(f"Экспортировано {len(task)} задач в файл {file_name}")