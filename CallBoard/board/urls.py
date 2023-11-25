from django.urls import path

from .views import AnnouncementList, AnnouncementDetail, AnnouncementCreate, AnnouncementUpdate, AnnouncementDelete, \
    CategoryList, successful_page_view, announcements_in_category_list

urlpatterns = [
    path('', AnnouncementList.as_view(), name='announcements'),
    path('<int:pk>', AnnouncementDetail.as_view(), name='announcement_detail'),
    path('create/', AnnouncementCreate.as_view(), name='announcement_create'),
    path('<int:pk>/update', AnnouncementUpdate.as_view(), name='announcement_update'),
    path('<int:pk>/delete', AnnouncementDelete.as_view(), name='announcement_delete'),
    path('category_list/', CategoryList.as_view(), name='category_list'),
    path('category/<int:id_ctg>', announcements_in_category_list, name='announcements_in_category_list'),
    path('successful/', successful_page_view, name='successful'),
]
