from django.conf.urls import url, include
from .views import IndexView, LoginView, BaseAdminView, LogoutView, ImportFileView, ViewFileView, GraphFileView
from .views import ExcelListView, ExcelFileDetailView, ExcelFileDeleteView, ExcelFileToJsonView

app_name = "viewer"

urlpatterns = [
    url(r'^api/', include('Grafistica.apps.viewer.api.urls'), name="api"),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^base/$', BaseAdminView.as_view(), name='base'),
    url(r'^import-file/$', ImportFileView.as_view(), name='import-file'),
    url(r'^excel-file-list/$', ExcelListView.as_view(), name='file-list'),
    url(r'^excel-file-detail/(?P<data_id>[0-9]+)/$', ExcelFileDetailView.as_view(), name='file-detail'),
    url(r'^excel-file-delete/(?P<data_id>[0-9]+)/$', ExcelFileDeleteView.as_view(), name='file-delete'),
    url(r'^excel-file-json-download/(?P<data_id>[0-9]+)/$', ExcelFileToJsonView.as_view(), name='file-json-download'),
    url(r'^view-file/(?P<data_id>[0-9]+)/$', ViewFileView.as_view(), name='view-file'),
    url(r'^graph-file/(?P<data_id>[0-9]+)/step/(?P<step>[0-9]+)/$', GraphFileView.as_view(), name='graph-file'),
    url(r'^logout/$', LogoutView.as_view(), name='logout')
]
