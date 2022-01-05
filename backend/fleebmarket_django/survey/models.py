"""
questions
 - Q1 how often do you trade second hand keyboard parts (on reddit or discord e.g.) ?
 CHOICE never / once a year / once a month / many times a month
 - Q2 if yes, what service do you use the most ? (r/mechamarket ? some discord server ?)
 TEXT
 - Q3 what kind of parts do you trade the most ?
 MULTICHOICE full keyboards / keysets / keycaps / artisan keycaps / switches / other parts
 - Q4 would you be interested in using a service provided by a dedicated website ?
 CHOICE yes / maybe / no
 - Q5 what are the essential features provided by the service you actually use ?
 TEXTAREA
 - Q6 what kind of features do you miss in the service you actually use ?
 TEXTAREA
 - Q7 would you be ready to pay a small monthly fee (between 1 and 2€) for some advanced features ?
 CHOICE yes / maybe / no
 - Q8 if yes, what kind of feature ?
 TEXTAREA
 - Q9 how many keyboards do you own ?
 NUMER
 - Q10 do you like the name fleebmarket ?
 CHOICE I love it / it's ok / it sucks / i don't care
 - Q11 anything else to say ?
 TEXTAREA
 - Q12[CAPTCHA] what's the current year ?
 NUMBER

"""


from django.db import models
from utils import ChoiceEnum
from multiselectfield import MultiSelectField

class Parts(ChoiceEnum):
    full = "Full keyboards"
    keysets = "Keysets"
    keycaps = "Keycaps (including artisan)"
    switches = "Switches"
    other = "Other parts"

class Period(ChoiceEnum):
    never = "Never"
    yearly = "Once or twice a year"
    monthly = "Once or twice a month"
    many = "Many times a month"


class YesNo(ChoiceEnum):
    yes = "Yes"
    maybe = "Maybe"
    no = "No"
    other = "I don't know"


class CustomYesNo(ChoiceEnum):
    yesyes = "I love it"
    yes = "It's ok"
    no = "It sucks"
    other = "I don't care"


class FirstSurveyData(models.Model):

    trade_frequency = models.CharField(choices=Period.choices(), max_length=100)
    most_used_service = models.CharField(max_length=100, blank=True)
    most_traded_parts = MultiSelectField(choices=Parts.choices(), blank=True)
    service_interest = models.CharField(choices=YesNo.choices(), max_length=100)
    essential_features = models.CharField(max_length=10000, blank=True)
    missed_features = models.CharField(max_length=10000, blank=True)
    would_pay = models.CharField(choices=YesNo.choices(), max_length=100)
    paying_features = models.CharField(max_length=10000, blank=True)
    how_many_keebs = models.PositiveIntegerField()
    like_fleebmarket = models.CharField(max_length=100, choices=CustomYesNo.choices())
    anything_else = models.CharField(max_length=10000, blank=True)
    current_year = models.PositiveIntegerField()

    # not used in practice
    def get_absolute_url(self):
        pass

