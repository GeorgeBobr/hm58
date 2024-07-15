from django.urls import path
from .views import IssueListView, IssueDetailView, IssueCreateView, IssueUpdateView, IssueDeleteView


urlpatterns = [
    path('', IssueListView.as_view(), name='index'),
    path('Issue/<int:id>/', IssueDetailView.as_view(), name='issue_detail'),
    path('Issue/create/', IssueCreateView.as_view(), name='issue_create'),
    path('Issue/update/<int:id>/', IssueUpdateView, name='issue_update'),
    path('Issue/delete/<int:id>/', IssueDeleteView, name='issue_delete')
]