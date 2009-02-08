#
# $Id$
#

from django import forms
from serpantin.apps.common.models import *

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District

class TownTypeForm(forms.ModelForm):
    class Meta:
        model = TownType

class TownForm(forms.ModelForm):
    class Meta:
        model = Town

class StreetTypeForm(forms.ModelForm):
    class Meta:
        model = StreetType

class StreetForm(forms.ModelForm):
    class Meta:
        model = Street

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone

class PhoneListForm(forms.ModelForm):
    class Meta:
        model = PhoneList

class AddresstypeForm(forms.ModelForm):
    class Meta:
        model = Addresstype

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person

class OrgtypeForm(forms.ModelForm):
    class Meta:
        model = Orgtype

class OrgForm(forms.ModelForm):
    class Meta:
        model = Org




 





