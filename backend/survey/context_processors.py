from datetime import datetime

survey_start = datetime(2021, 1, 1)
survey_end = datetime(2021, 2, 1)


def survey_active(request):
    now = datetime.now()
    active = now >= survey_start and now <= survey_end
    return {"survey_active": active}
