"""fleebmarket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin, sitemaps
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, reverse
from django.views.generic.base import TemplateView  # import TemplateView
from simpleblog.models import Post

from . import views


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return ["about"]

    def location(self, item):
        return reverse(item)


class BlogSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return Post.objects.all()

    def lastmod(self, item: Post):
        return item.modified or item.post_date


fleebmarket_sitemaps = {"static": StaticViewSitemap(), "blog": BlogSitemap()}

urlpatterns = [
    path("", views.redirect_search),
    path("search_ads/", views.redirect_search),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/profile/", include("accounts.urls")),
    path("about", views.about, name="about"),
    path("contact", views.contact, name="contact"),
    path("survey/", include("survey.urls")),
    path("search/", include("search_app.urls")),
    path("search_item/", include("search_app.urls")),
    path("blog/", include("simpleblog.urls")),
    path("alerts/", include("alerts.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": fleebmarket_sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.autodiscover()
admin.site.enable_nav_sidebar = False
