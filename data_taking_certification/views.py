from django.shortcuts import render

from data_taking_objects.models import Run, Lumisection
from data_taking_certification.models import RunCertification, LumisectionCertification

# from histograms.models import RunHistogram

import pandas as pd


# Create your views here.
def run_certification_view(request):

    error_message = None
    df = None

    # TODO The following lines should be done on the DB side
    certification_df = pd.DataFrame(RunCertification.objects.all().values())
    runs_df = pd.DataFrame(Run.objects.all().values())

    if certification_df.shape[0] > 0:
        df = runs_df.merge(certification_df, left_on="id", right_on="run_id")[
            [
                "run_number",
                "rr_frac_pixel_good",
                "rr_frac_strip_good",
                "rr_frac_tracking_good",
                "rr_frac_ecal_good",
            ]
        ]
        print(df.head())
    else:
        error_message = "No certificationss in the database"

    context = {
        "error_message": error_message,
        "runs": df,
    }

    return render(request, "data_taking_certification/run_certification.html", context)

def lumisection_certification_view(request):

    error_message = None
    df = None

    lumisection_certifications = LumisectionCertification.objects.all()
    n_certifications = len(lumisection_certifications)

    if n_certifications > 0:
        print(f"{n_certifications} certifications are being loaded")
    else:
        error_message = "No lumisectionn certifications in the database"

    context = {
        "error_message": error_message,
        "lumisection_certifications": lumisection_certifications,
    }

    return render(request, "data_taking_certification/lumisection_certification.html", context)
