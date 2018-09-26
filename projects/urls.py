from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r"all", views.AllProjects.as_view(), name="all_projects"
    ),
    url(
        r"(?P<pk>\d+)/detail/$",
        views.ProjectDetailView.as_view(),
        name="detail"),
    url(
        r"(?P<pk>\d+)/positions/(?P<position_pk>\d+)/apply$",
        views.CreateApplicationView.as_view(),
        name="apply"),
    url(
        r"new/$",
        views.CreateProjectPositionView.as_view(),
        name="create_project"),
    url(
        r"(?P<pk>\d+)/edit$",
        views.TestEditView.as_view(),
        name="edit_project"),
    url(
        r"applications/$", views.AllApplications.as_view(), name="applications"
    ),
    url(
        r"applications/(?P<pk>\d+)$", views.ApplicationsDetailView.as_view(),
        name="application_detail"
    ),
    url(
        r"applications/(?P<pk>\d+)/(?P<decision>\w+)$",
        views.AcceptRejectApplicationView.as_view(),
        name="application_decision"),
    url(r'delete/(?P<pk>\d+)$', views.DeleteProjectView.as_view(),
        name='delete'),
]
