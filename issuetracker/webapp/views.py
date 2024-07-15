from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from webapp.forms import IssueForm
from webapp.models import Issue


class IssueListView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        issues = Issue.objects.order_by("-updated_at")
        context = {"issues": issues}
        return context


class IssueCreateView(View):
    def get(self, request, *args, **kwargs):
        form = IssueForm()
        print(form)
        return render(request, "issue_create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = IssueForm(data=request.POST)
        if form.is_valid():
            types = form.cleaned_data.get("type")

            issue = Issue.objects.create(
                summary=form.cleaned_data.get("summary"),
                description=form.cleaned_data.get("description"),
                status=form.cleaned_data.get("status")
            )
            if types:
                issue.type.set(types)

            return redirect("index")
        else:
            print(form.errors)
            return render(request, "issue_create.html", {"form": form})


def IssueUpdateView(request, id):
    issue = get_object_or_404(Issue, id=id)
    if request.method == "GET":
        form = IssueForm(initial={
            "summary": issue.summary,
            "description": issue.description,
            "types": issue.types.all(),
            "status": issue.status
        })
        return render(request, "issue_edit.html", {"form": form})
    else:
        form = IssueForm(data=request.POST)
        if form.is_valid():
            types = form.cleaned_data.get("types")
            status = form.cleaned_data.get("status")
            issue.summary = form.cleaned_data.get("summary")
            issue.description = form.cleaned_data.get("description")
            issue.types.set(types)
            issue.status = status
            issue.save()
            return redirect("index")
        else:
            return render(request, "issue_edit.html", {"form": form})



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