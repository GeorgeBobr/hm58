from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import IssueForm
from webapp.models import Issue, Status, Type


class IssueListView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        issues = Issue.objects.order_by("-updated_at")
        context = {"issues": issues}
        return context


class IssueCreateView(View):
    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        types = Type.objects.all()
        context = {
            'statuses': statuses,
            'types': types
        }
        return render(request, "issue_create.html", context)

    def post(self, request, *args, **kwargs):
        summary = request.POST.get('summary')
        description = request.POST.get('description')
        status_id = request.POST.get('status')
        type_ids = request.POST.getlist('type')

        if summary and status_id and type_ids:
            status = get_object_or_404(Status, id=status_id)
            issue = Issue.objects.create(
                summary=summary,
                description=description,
                status=status
            )
            issue.types.set(Type.objects.filter(id__in=type_ids))
            return redirect('index')
        else:
            statuses = Status.objects.all()
            types = Type.objects.all()
            context = {
                'statuses': statuses,
                'types': types,
                'error': 'Заполните все обязательные поля'
            }
            return render(request, "issue_create.html", context)



class IssueUpdateView(View):
    def get(self, request, id, *args, **kwargs):
        issue = get_object_or_404(Issue, id=id)
        statuses = Status.objects.all()
        types = Type.objects.all()
        context = {
            'issue': issue,
            'statuses': statuses,
            'types': types
        }
        return render(request, "issue_edit.html", context)

    def post(self, request, id, *args, **kwargs):
        issue = get_object_or_404(Issue, id=id)
        summary = request.POST.get('summary')
        description = request.POST.get('description')
        status_id = request.POST.get('status')
        type_ids = request.POST.getlist('type')

        if summary and status_id and type_ids:
            status = Status.objects.get(id=status_id)
            issue.summary = summary
            issue.description = description
            issue.status = status
            issue.types.clear()  # Очищаем текущие типы задачи
            issue.types.add(*Type.objects.filter(id__in=type_ids))  # Добавляем новые типы
            issue.save()
            return redirect('index')
        else:
            statuses = Status.objects.all()
            types = Type.objects.all()
            context = {
                'issue': issue,
                'statuses': statuses,
                'types': types,
                'error': 'Заполните все обязательные поля'
            }
            return render(request, "issue_edit.html", context)



def IssueDeleteView(request, id):
    issue = get_object_or_404(Issue, id=id)
    if request.method == "GET":
        return render(request, "issue_delete.html", {"issue": issue})
    else:
        issue.delete()
        return redirect("index")


class IssueDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["issue"] = get_object_or_404(Issue, id=kwargs['id'])
        return context

    def get_template_names(self):
        return "issue_detail.html"