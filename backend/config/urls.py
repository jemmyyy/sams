"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from apps.common.views import HealthCheckView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/health/", HealthCheckView.as_view(), name="health_check"),
    path("api/v1/accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("api/v1/sessions/", include("apps.sessions.urls", namespace="sessions")),
    path("api/v1/coaches/", include("apps.coaches.urls", namespace="coaches")),
    path("api/v1/players/", include("apps.players.urls", namespace="players")),
    path("api/v1/groups/", include("apps.groups.urls", namespace="groups")),
    path("api/v1/attendance/", include("apps.attendance.urls", namespace="attendance")),
    path("api/v1/communication/", include("apps.communication.urls", namespace="communication")),
    path("api/v1/cancellations/", include("apps.cancellations.urls", namespace="cancellations")),
    path("api/v1/ratings/", include("apps.ratings.urls", namespace="ratings")),
    path("api/v1/reports/", include("apps.reports.urls", namespace="reports")),
    path("api/v1/payments/", include("apps.payments.urls", namespace="payments")),
    path("api/v1/notifications/", include("apps.notifications.urls")),
    path("api/v1/analytics/", include("apps.analytics.urls")),
]
