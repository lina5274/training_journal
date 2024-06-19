import tkinter as tk
from tkinter import ttk, Toplevel, messagebox
import json
from datetime import datetime
from tkcalendar import Calendar
import csv
import matplotlib.pyplot as plt

data_file = 'training_log.json'


class TrainingLogApp:
    def __init__(self, root):
        self.root = root
        root.title("Дневник тренировок")
        self.existing_entry_id = None
        self.create_widgets()
        #self.load_treeview_data()

    def plot_exercise_statistics(self, exercises_stats):
        fig, ax = plt.subplots()
        ax.set_title('Изменение веса и повторений по упражнениям')

        exercises = list(exercises_stats.keys())
        total_reps = [stats['Общее количество повторений'] for stats in exercises_stats.values()]
        total_weight = [stats['Общий вес'] for stats in exercises_stats.values()]

        ax.plot(exercises, total_reps, label='Повторения')
        ax.plot(exercises, total_weight, label='Вес')

        ax.legend()
        plt.xlabel('Упражнения')
        plt.ylabel('Количество')
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.show()

    def load_data(self):
        try:
            with open(data_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self, data):
        with open(data_file, 'w') as file:
            json.dump(data, file, indent=4)

    def export_to_csv(self):
        data = self.load_data()
        with open('training_log.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Дата', 'Упражнение', 'Вес', 'Повторения']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for entry in data:
                writer.writerow({'Дата': entry['Дата'],
                                 'Упражнение': entry['Упражнение'],
                                 'Вес': entry['Вес'],
                                 'Повторения': entry['Повторения']})

        messagebox.showinfo("Успех", "Данные успешно экспортированы в CSV файл.")

    def import_from_csv(self):
        try:
            with open('training_log.csv', 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                existing_data = self.load_data()
                for row in reader:
                    new_entry = {
                        'Дата': row['Дата'],
                        'Упражнение': row['Упражнение'],
                        'Вес': row['Вес'],
                        'Повторения': row['Повторения'],
                        'id': len(existing_data) + 1  # Обеспечение уникальности ID
                    }
                    existing_data.append(new_entry)
                self.save_data(existing_data)
                messagebox.showinfo("Успех", "Данные успешно импортированы из CSV файла.")
                self.load_treeview_data()
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "CSV файл не найден.")

    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        self.tree.heading('Дата', text="Дата")
        self.tree.heading('Упражнение', text="Упражнение")
        self.tree.heading('Вес', text="Вес")
        self.tree.heading('Повторения', text="Повторения")
        self.tree.grid(row=10, column=0, columnspan=2, sticky=tk.NSEW)

        self.exercise_label = ttk.Label(self.root, text="Упражне  ие:")
        self.exercise_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.exercise_combobox = ttk.Combobox(self.root, values=["Приседание", "Жим лежа", "Подтягивание"])
        self.exercise_combobox.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

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
        self.start_date_label.grid(column=0, row=5, sticky=tk.W, padx=5, pady=5)

        self.end_date_label = ttk.Label(self.root, text="Конечная дата:")
        self.end_date_label.grid(column=0, row=6, sticky=tk.W, padx=5, pady=5)

        self.start_date_entry = Calendar(self.root, selectmode='day', date_pattern='yyyy-mm-dd')
        self.start_date_entry.grid(column=1, row=5, sticky=tk.EW, padx=5, pady=5)

        self.end_date_entry = Calendar(self.root, selectmode='day', date_pattern='yyyy-mm-dd')
        self.end_date_entry.grid(column=1, row=6, sticky=tk.EW, padx=5, pady=5)

        self.export_button = ttk.Button(self.root, text="Экспорт в CSV", command=self.export_to_csv)
        self.export_button.grid(column=0, row=7, columnspan=2, pady=10)

        self.import_button = ttk.Button(self.root, text="Импорт из CSV", command=self.import_from_csv)
        self.import_button.grid(column=0, row=8, columnspan=2, pady=10)

        self.delete_button = ttk.Button(self.root, text="Удалить запись", command=self.delete_entry)
        self.delete_button.grid(column=0, row=9, columnspan=2, pady=10)

        self.plot_button = ttk.Button(self.root, text="Статистика", command=self.display_statistics)
        self.plot_button.grid(column=0, row=11, columnspan=2, pady=10)

        self.tree.bind('<Double-1>', self.select_item)

    def load_treeview_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        data = self.load_data()
        for entry in data:
            self.tree.insert('', tk.END, values=(entry['Дата'], entry['Упражнение'], entry['Вес'], entry['Повторения']))

    def select_item(self, event):
        selected_item = self.tree.selection()[0]
        selected_data = self.tree.item(selected_item)['values']
        self.populate_fields(selected_data)

    def populate_fields(self, data):
        self.exercise_combobox.set(data[1])

        self.weight_entry.delete(0, tk.END)
        self.weight_entry.insert(tk.END, data[2])

        self.repetitions_entry.delete(0, tk.END)
        self.repetitions_entry.insert(tk.END, data[3])

    def add_entry(self):
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exercise = self.exercise_combobox.get()
        weight = self.weight_entry.get()
        repetitions = self.repetitions_entry.get()

        if not (exercise and weight and repetitions):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
            return

        entry = {
            'Дата': date,
            'Упражнение': exercise,
            'Вес': weight,
            'Повторения': repetitions,
            'id': len(self.load_data()) + 1  # Обеспечение уникальности ID
        }

        data = self.load_data()
        if self.existing_entry_id is not None:
            index = next((i for i, d in enumerate(data) if d['id'] == self.existing_entry_id), None)
            if index is not None:
                data[index] = entry
            else:
                messagebox.showerror("Ошибка", "Запись не найдена.")
                return
        else:
            data.append(entry)

        self.save_data(data)
        self.load_treeview_data()
        self.existing_entry_id = entry['id']

        self.exercise_combobox.set('')
        self.weight_entry.delete(0, tk.END)
        self.repetitions_entry.delete(0, tk.END)
        messagebox.showinfo("Успешно", "Запись успешно добавлена!")

    def delete_entry(self):
        selected_item = self.tree.selection()[0]
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите запись для удаления.")
            return
        selected_data = self.tree.item(selected_item)['values']
        data = self.load_data()
        data = [entry for entry in data if entry['Дата'] != selected_data[0] or entry['Упражнение'] != selected_data[1]]
        self.save_data(data)
        self.tree.delete(selected_item)
        messagebox.showinfo("Успех", "Запись успешно удалена!")
        self.load_treeview_data()

    def view_records(self):
        data = self.load_data()
        records_window = Toplevel(self.root)
        records_window.title("Записи тренировок")

        tree = ttk.Treeview(records_window, columns=("Дата", "Упражнение", "Вес", "Повторения"), show="headings")
        tree.heading('Дата', text="Дата")
        tree.heading('Упражнение', text="Упражнение")
        tree.heading('Вес', text="Вес")
        tree.heading('Повторения', text="Повторения")
        tree.grid(row=0, column=0, sticky=tk.NSEW)

        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()

        filtered_data = []

        for entry in data:
            entry_date = datetime.strptime(entry['Дата'], '%Y-%m-%d %H:%M:%S').date()
            if start_date and entry_date < start_date:
                continue
            if end_date and entry_date > end_date:
                continue

            filtered_data.append(entry)
            tree.insert('', tk.END, values=(entry['Дата'], entry['Упражнение'], entry['Вес'], entry['Повторения']))

        records_window.grid_rowconfigure(0, weight=1)
        records_window.grid_columnconfigure(0, weight=1)

        if filtered_data:
            exercises_stats = {}
            for entry in filtered_data:
                exercise = entry['Упражнение']
                weight = int(entry['Вес'])
                repetitions = int(entry['Повторения'])

                if exercise not in exercises_stats:
                    exercises_stats[exercise] = {'Общее количество повторений': 0, 'Общий вес': 0}

                exercises_stats[exercise]['Общее количество повторений'] += repetitions
                exercises_stats[exercise]['Общий вес'] += weight

            statistics_message = "Статистика упражнений:\n"
            for exercise, stats in exercises_stats.items():
                statistics_message += f"{exercise}: Повторений - {stats['Общее количество повторений']}, Вес - {stats['Общий вес']}\n"
            messagebox.showinfo("Статистика упражнений", statistics_message)

    def display_statistics(self):
        start_date = self.start_date_entry.get_date()
        end_date = self.end_date_entry.get_date()
        self.view_records()

def main():
    root = tk.Tk()
    app = TrainingLogApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
