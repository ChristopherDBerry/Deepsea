from django.shortcuts import render
from dsdata.models import SensorData


def main(request):
    if request.method == 'POST' and request.POST.get('reset'):
        SensorData.objects.all().delete()
    return render(request, 'dsadmin/admin.html')