from django.shortcuts import render

from data_taking_objects.models import Run, Lumisection
from data_taking_certification.models import RunCertification, LumisectionCertification


# Create your views here.
def run_certification_view(request):

    error_message = None

    run_certifications = RunCertification.objects.all()
    n_certifications = run_certifications.count()

    if n_certifications > 0:
        print(f"{n_certifications} certifications are being loaded")
    else:
        error_message = "No run certifications in the database"

    context = {
        "error_message": error_message,
        "run_certifications": run_certifications,
    }

    return render(request, "data_taking_certification/run_certification.html", context)


def lumisection_certification_view(request):

    error_message = None

    lumisection_certifications = LumisectionCertification.objects.all()
    n_certifications = lumisection_certifications.count()

    if n_certifications > 0:
        print(f"{n_certifications} certifications are being loaded")
    else:
        error_message = "No lumisection certifications in the database"

    context = {
        "error_message": error_message,
        "lumisection_certifications": lumisection_certifications,
    }

    return render(
        request, "data_taking_certification/lumisection_certification.html", context
    )
