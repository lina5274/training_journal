import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
import json
from datetime import datetime
from tkinter import DateEntry
import csv

# Файл для сохранения данных
data_file = 'training_log.json'

def load_data():
    """Загрузка данных о тренировках из файла."""
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """Сохранение данных о тренировках в файл."""
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)


def export_to_csv():
    """Экспорт данных в CSV файл."""
    data = load_data()
    with open('training_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Дата', 'Упражнение', 'Вес', 'Повторения']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in data:
            writer.writerow({'Дата': entry['date'],
                             'Упражнение': entry['exercise'],
                             'Вес': entry['weight'],
                             'Повторения': entry['repetitions']})

    messagebox.showinfo("Успех", "Данные успешно экспортированы в CSV файл.")

class TrainingLogApp:
    def __init__(self, root):
        self.root = root
        root.title("Дневник тренировок")
        self.create_widgets()

    def create_widgets(self):
        # Виджеты для ввода данных
        self.exercise_label = ttk.Label(self.root, text="Упражнение:")
        self.exercise_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.exercise_entry = ttk.Entry(self.root)
        self.exercise_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        self.weight_label = ttk.Label(self.root, text="Вес:")
        self.weight_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.weight_entry = ttk.Entry(self.root)
        self.weight_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

        self.repetitions_label = ttk.Label(self.root, text="Повторения:")
        self.repetitions_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)

        self.repetitions_entry = ttk.Entry(self.root)
        self.repetitions_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

        self.add_button = ttk.Button(self.root, text="Добавить запись", command=self.add_entry)
        self.add_button.grid(column=0, row=3, columnspan=2, pady=10)

        self.view_button = ttk.Button(self.root, text="Просмотреть записи", command=self.view_records)
        self.view_button.grid(column=0, row=4, columnspan=2, pady=10)

        self.start_date_label = ttk.Label(self.root, text="Начальная дата:")
        self.start_date_label.grid(column=0, row=4, sticky=tk.W, padx=5, pady=5)

        self.end_date_label = ttk.Label(self.root, text="Конечная дата:")
        self.end_date_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)

        self.start_date_entry = DateEntry(self.root)
        self.start_date_entry.grid(column=1, row=4, sticky=tk.EW, padx=5, pady=5)

        self.end_date_entry = DateEntry(self.root)
        self.end_date_entry.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)

        self.exercise_combobox = ttk.Combobox(self.root, values=["Приседание", "Жим лежа", "Подтягивание"],
                                              state='readonly')
        self.exercise_combobox.current(0)
        self.exercise_combobox.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

        self.export_button = ttk.Button(self.root, text="Экспорт в CSV", command=self.export_to_csv)
        self.export_button.grid(column=0, row=6, columnspan=2, pady=10)

    def add_entry(self):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exercise = self.exercise_entry.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        entry = {
            'date': date,
            'exercise': exercise,
            'weight': weight,
            'repetitions': repetitions
        }

        data = load_data()
        data.append(entry)
        save_data(data)

        # Очистка полей ввода после добавления
        self.exercise_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)
        messagebox.showinfo("Успешно", "Запись успешно добавлена!")

    def view_records(self, start_date=None, end_date=None, xercise_filter=None):
        data = load_data()
        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")

        tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")

        filtered_entries = [entry for entry in data if
                            not start_date or datetime.strptime(entry['date'][:10], '%Y-%m-%d') >= datetime.strptime(
                                start_date, '%Y-%m-%d')
                            if not end_date or datetime.strptime(entry['date'][:10], '%Y-%m-%d') <= datetime.strptime(
                end_date, '%Y-%m-%d')]

        if exercise_filter:
            filtered_entries = [entry for entry in filtered_entries if entry['exercise'] == exercise_filter]

        for entry in data:
            tree.insert('', tk.END, values=(entry['date'], entry['exercise'], entry['weight'], entry['repetitions']))

        tree.pack(expand=True, fill=tk.BOTH)

def main():
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
