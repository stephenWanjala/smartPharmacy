from pharmacy.models import ExpiredMedicineLog


def expired_medicine_logs(request):
    expired_logs = ExpiredMedicineLog.objects.all()
    return {'expired_logs': expired_logs}
