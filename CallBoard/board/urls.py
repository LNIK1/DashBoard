from django.urls import path

from .views import AnnouncementList, AnnouncementDetail, AnnouncementCreate, AnnouncementUpdate, AnnouncementDelete, \
    CategoryList, RespondList, RespondCreate, RespondDetail, \
    announcements_in_category_list, announcements_own_list, \
    successful_announcement_view, successful_respond_view, accept_respond, denied_respond


urlpatterns = [
    path('', AnnouncementList.as_view(), name='announcements'),
    path('own/', announcements_own_list, name='announcements_own'),
    path('<int:pk>', AnnouncementDetail.as_view(), name='announcement_detail'),
    path('create/', AnnouncementCreate.as_view(), name='announcement_create'),
    path('<int:pk>/update', AnnouncementUpdate.as_view(), name='announcement_update'),
    path('<int:pk>/delete', AnnouncementDelete.as_view(), name='announcement_delete'),
    path('category_list/', CategoryList.as_view(), name='category_list'),
    path('category/<int:id_ctg>', announcements_in_category_list, name='announcements_in_category_list'),
    path('responds_list/', RespondList.as_view(), name='responds_list'),
    path('<int:pk>/responds/create/', RespondCreate.as_view(), name='respond_create'),
    path('responds/<int:pk>/', RespondDetail.as_view(), name='respond_detail'),
    path('responds/accept/<int:pk>/', accept_respond, name='respond_accept'),
    path('responds/denied/<int:pk>/', denied_respond, name='respond_denied'),
    path('successful/announcement', successful_announcement_view, name='successful_announcement'),
    path('successful/respond', successful_respond_view, name='successful_respond'),
]
