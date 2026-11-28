from django.shortcuts import get_object_or_404, render

from website.models import Teacher


def teacher_detail(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk, is_active=True)
    return render(request, "website/teachers/detail.html", {
        "teacher": teacher,
    })
