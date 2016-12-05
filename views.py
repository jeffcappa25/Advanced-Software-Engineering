from django.shortcuts import render
from allauth.account.decorators import verified_email_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Bill, Login
from .forms import BillForm, LoginForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum
#importing libraries and begin registration
#
@login_required
def home(request):
    print Login.objects.filter(user=request.user)
    if len(Login.objects.filter(user=request.user)) == 0:
        user = User.objects.get(pk=request.user.id)
        form = LoginForm(request.POST or None)
        data = {
                "user": user,
                "form": form
                }
        return render(request, "choose_tipe.html", data)
    print "Here!"
    user_m = get_object_or_404(Login, user=request.user)
    if user_m.tipe == 'Parent':
        if len(user_m.relation) > 0:
            return HttpResponseRedirect("/dashboard/")
        else:
            print "Here choose_child"
            return render(request, "choose_child.html", {})
    else:
        return HttpResponseRedirect("/dashboard/")


@login_required
def choose_tipe(request):
    print request.POST
    form = LoginForm(request.POST or None)
    if form.is_valid():
        tipe_add = form.save(commit=False)
        tipe_add.user = User.objects.get(pk=request.user.id)
        print tipe_add.user
        tipe_add.save()
        return HttpResponseRedirect("/dashboard/")
    return HttpResponseRedirect("/")


@login_required
def choose_child(request):
    main_user = Login.objects.get(user=request.user)
    post_dict = request.POST
    chi_id = post_dict['s_id']
    chi_user = Login.objects.get(user=chi_id)
    main_user.relation = chi_user.user.username
    main_user.save()
    return HttpResponseRedirect("/dashboard/")


@login_required
def dashboard(request):
    user_m = get_object_or_404(Login, user=request.user)
    show_id = "Student"
    if user_m.tipe == 'Parent':
        if len(user_m.relation) > 0:
            print user_m.relation
            user_m = get_object_or_404(Login, user=User.objects.get(username=user_m.relation))
            show_id = 'Parent'
        else:
            return HttpResponseRedirect("/")
    form = BillForm(request.POST or None)
    if form.is_valid():
        bill_add = form.save(commit=False)
        bill_add.creator = User.objects.get(username=user_m)
        bill_add.save()
    rows = Bill.objects.filter(creator=user_m.user)
    total_bill_sum = rows.aggregate(Sum('bill_sum')).values()[0]
    data = {
        "form": form,
        "rows": rows,
        "total": total_bill_sum,
        "user_m": user_m,
        "show_id": show_id
    }
    return render(request, "dashboard.html", data)
