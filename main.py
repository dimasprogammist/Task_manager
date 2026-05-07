from database import Database
import menu_options as options

db = Database()
db.init_database()

def menu():
    while True:
        print('===============Меню===============')
        print('1. Добавить задачу')
        print('2. Показать все задачи')
        print('3. Показать задачи по приоритету')
        print('4. Отметить как выполненную')
        print('5. Удалить задачу')
        print('6. Экспорт в CSV')
        print('7. Выход')

        option = int(input('\nВведите номер функции: '))

        if option == 1:
            options.add_task()
        elif option == 2:
            options.show_all_tasks()
        elif option == 3:
            options.show_tasks_sort()
        elif option == 4:
            options.mark_as_done()
        elif option == 5:
            options.delite_task()
        elif option == 6:
            options.export_csv()
        elif option == 7:
            print('До свидания')
            break
        else:
            print('Выбрана неизвестная функция')

if __name__ == '__main__':
    menu()