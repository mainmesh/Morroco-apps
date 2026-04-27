from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'loans', views.LoanViewSet, basename='loan')
router.register(r'repayments', views.RepaymentViewSet, basename='repayment')

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('apply/<int:amount>/', views.apply_loan, name='apply_loan'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.accounts, name='accounts'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users, name='admin_users'),
    path('admin/loans/', views.admin_loans, name='admin_loans'),
    path('admin/repayments/', views.admin_repayments, name='admin_repayments'),
    path('api/', include(router.urls)),
]