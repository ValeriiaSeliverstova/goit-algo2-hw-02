# Опис завдання
# 1. Використовуйте вхідні дані у вигляді списку завдань на друк, де кожне завдання містить: ID, об'єм моделі, пріоритет та час друку.
# 2. Реалізуйте основну функцію optimize_printing, яка буде:
# Враховувати пріоритети завдань.
# Групувати моделі для одночасного друку.
# Перевіряти обмеження об'єму та кількості.
# Розраховувати загальний час друку.
# Повертати оптимальний порядок друку.
# 3. Виведіть оптимальний порядок друку та загальний час виконання всіх завдань.


# 4. Пріоритети завдань:
# 1 (найвищий) — Курсові/дипломні роботи
# 2 — Лабораторні роботи
# 3 (найнижчий) — Особисті проєкти


# Програма групує моделі для одночасного друку, не перевищуючи обмеження (12 б).
# Завдання з вищим пріоритетом виконуються раніше (12 б).
# Час друку групи моделей розраховується як максимальний час серед моделей у групі (12 б).
# Програма обробляє всі тестові сценарії (12 б):
# завдання однакового пріоритету,
# завдання різних пріоритетів,
# перевищення обмежень принтера.
# Код використовує dataclass для структур даних (12 б).


from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def convert_jobs_to_object(print_jobs: List[Dict]) -> List[PrintJob]:
    return [
        PrintJob(
            id=str(j["id"]),
            volume=float(j["volume"]),
            priority=int(j["priority"]),
            print_time=int(j["print_time"]),
        )
        for j in print_jobs
    ]


def convert_constraints_to_object(constraints: Dict) -> PrinterConstraints:
    return PrinterConstraints(
        max_volume=float(constraints["max_volume"]),
        max_items=int(constraints["max_items"]),
    )


def batch_jobs_by_priority(jobs: List[PrintJob]) -> Dict[int, List[PrintJob]]:
    batches = {}
    for job in jobs:
        if job.priority not in batches:
            batches[job.priority] = []
        batches[job.priority].append(job)
    return batches


def group_jobs_for_printing(
    jobs: List[PrintJob], constraints: PrinterConstraints
) -> List[List[PrintJob]]:
    all_groups: List[List[PrintJob]] = []
    current_group: List[PrintJob] = []
    current_volume = 0.0

    for job in jobs:

        if job.volume > constraints.max_volume or constraints.max_items < 1:
            raise ValueError(
                f"Завдання {job.id} перевищує обмеження принтера і не може бути заплановане."
            )

        if (
            len(current_group) < constraints.max_items
            and current_volume + job.volume <= constraints.max_volume
        ):
            current_group.append(job)
            current_volume += job.volume
        else:
            if current_group:
                all_groups.append(current_group)
            current_group = [job]
            current_volume = job.volume

    if current_group:
        all_groups.append(current_group)

    return all_groups


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """

    jobs = convert_jobs_to_object(print_jobs)
    printer_constraints = convert_constraints_to_object(constraints)
    jobs_by_priority = batch_jobs_by_priority(jobs)

    all_groups: List[List[PrintJob]] = []

    for priority in sorted(jobs_by_priority.keys()):
        priority_jobs = jobs_by_priority[priority]
        priority_jobs.sort(key=lambda j: j.print_time, reverse=True)

        priority_groups = group_jobs_for_printing(priority_jobs, printer_constraints)

        all_groups.extend(priority_groups)

    print_order = [[job.id for job in group] for group in all_groups]
    total_time = (
        sum(max(job.print_time for job in group) for group in all_groups)
        if all_groups
        else 0
    )

    return {"print_order": print_order, "total_time": total_time}


# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150},
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {
            "id": "M3",
            "volume": 120,
            "priority": 3,
            "print_time": 150,
        },  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120},
    ]

    constraints = {"max_volume": 300, "max_items": 2}

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
