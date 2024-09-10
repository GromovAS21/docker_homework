from django.core.management import BaseCommand

from materials.models import Course, Lesson


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Заполнение базы курсами и уроками
        """

        course_list = [
            {
                "title": "Курс программирования",
                "description": "Программа в светлое будущее",
            },
            {"title": "Курс Чтения", "description": "Учимся читать по слогам"},
        ]
        lesson_list = [
            {"course_id": 1, "title": "python3", "description": "Питон"},
            {"course_id": 1, "title": "JavaScript", "description": "Скрипты"},
            {"course_id": 2, "title": "Букварь", "description": "Буквы"},
            {
                "course_id": 2,
                "title": "Литература",
                "description": "школьная программа",
            },
        ]

        course_for_create = []
        for course in course_list:
            course_for_create.append(Course(**course))

        Course.objects.bulk_create(course_for_create)

        lesson_for_create = []
        for lesson in lesson_list:
            lesson_for_create.append(Lesson(**lesson))

        Lesson.objects.bulk_create(lesson_for_create)
