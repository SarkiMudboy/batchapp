from django.urls import path
from .views import *

app_name = "raw_materials"

urlpatterns = [

	path("raw_materials/list", RawmaterialView.as_view(), name="raw-material-list"),
	path("raw_materials/list/create", RawmaterialCreateView.as_view(), name="raw-material-create"),
	path("raw_materials/list/update", RawmaterialUpdateView.as_view(), name="raw-material-update"),
	path("raw_materials/list/delete", RawmaterialDeleteView.as_view(), name="raw-material-delete"),

	path("raw_materials/list/batch/", RawMaterialBatchView.as_view(), name="raw-material-list"),
	path("raw_materials/list/batch/create", RawMaterialBatchCreate.as_view(), name="raw-material-create"),
	path("raw_materials/list//batch/update", RawMaterialBatchUpdate.as_view(), name="raw-material-update"),
	path("raw_materials/list/batch/delete", RawMaterialBatchDelete.as_view(), name="raw-material-delete"),
]