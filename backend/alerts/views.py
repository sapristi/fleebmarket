from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView

from .actions import score_advert
from .forms import AlertForm, TestRelevancyForm
from .models import Alert

# Create your views here.


@login_required
def index_list(request):
    alerts = Alert.objects.filter(user=request.user)
    return render(request, "alerts/list.html", {"alerts": alerts})


def add_user(request):
    if not request.POST:
        return None
    query_args = request.POST.copy()
    query_args["user"] = request.user
    return query_args


@login_required
def create(request):
    alerts = Alert.objects.filter(user=request.user)

    if request.method == "POST":
        form = AlertForm(add_user(request))
        if form.is_valid():
            form.save()
            return redirect("alerts:index")

    form = AlertForm()
    return render(request, "alerts/create.html", {"form": form, "alerts": alerts})


@login_required
def edit(request, pk, template_name="alerts/edit.html"):
    alerts = Alert.objects.filter(user=request.user)
    alert = get_object_or_404(Alert, pk=pk)
    form = AlertForm(add_user(request) or None, instance=alert)
    if form.is_valid():
        form.save()
        return redirect("alerts:index")

    print("ERRORS?", form.errors)
    return render(request, template_name, {"pk": pk, "form": form, "alerts": alerts})


@login_required
def delete(request, pk, template_name="alerts/confirm_delete.html"):
    alerts = Alert.objects.filter(user=request.user)
    alert = get_object_or_404(Alert, pk=pk)
    if request.method == "POST" and alert.user == request.user:
        alert.delete()
        return redirect("alerts:index")
    return render(request, template_name, {"pk": pk, "object": alert, "alerts": alerts})


def help(request, template_name="alerts/help.html"):
    form = TestRelevancyForm(request.POST or None)
    relevancy = None
    if request.method == "POST":
        if form.is_valid():
            terms = form.cleaned_data["terms"].split(" ")
            full_text = form.cleaned_data["full_text"]
            relevancy = score_advert(terms, "", full_text)
    return render(request, template_name, {"form": form, "relevancy": relevancy})


@login_required
def test_notifications(request, template_name="alerts/help.html"):
    request.user.send_message("This is a test message", "I works !")
    return redirect("alerts:help")
