from django.shortcuts import reverse, redirect
from django.conf import settings

def under_maintenance():
    maintenance_file = settings.DATA_DIR / "maintenance"
    print("MAINTENANCE", maintenance_file, maintenance_file.exists())
    return maintenance_file.exists()

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.META.get('PATH_INFO', "")

        if under_maintenance() and path != reverse("maintenance"):
            return redirect(reverse("maintenance"))

        if not under_maintenance() and path == reverse("maintenance"):
            return redirect(reverse("index"))

        return self.get_response(request)
