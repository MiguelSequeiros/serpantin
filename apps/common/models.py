#
#
#

from string import find

from django.db import models
from django.core import validators
from django.core.validators import isValidEmail
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.contrib.auth.models import User


class Country(models.Model):
    #addr_code = models.CharField(_('Street Code'), maxlength=6)
    name = models.CharField(_('Country Name'), maxlength=100)
    
    createuser = models.ForeignKey(User, related_name='created_countries', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_countries', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)


    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ('name',)


    class Admin:
        fields = (
            (None, {'fields': ('name',)}),
        )     
        list_display = ('name',)

        
    def __unicode__(self):
        return self.name


class Region(models.Model):
    country = models.ForeignKey(Country, blank=True, null=True, verbose_name=_('Country'))
    #FIXME: shortname is too short
    #shortname = models.CharField(_('Region Code'), maxlength=6, unique=True, blank=True)
    name = models.CharField(_('Region Name'), maxlength=100, unique=True)
    
    createuser = models.ForeignKey(User, related_name='created_regions', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_regionss', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)


    class Meta:
        verbose_name = _('Region')
        verbose_name_plural = _('Regions')


    class Admin:
        fields = (
            (None, {'fields': ('name',)}),
        )      
        list_display = ('name',)

        
    def __unicode__(self):
        return self.name


class District(models.Model):
    name = models.CharField(_('District Name'), maxlength=60, blank=True)
    region = models.ForeignKey(Region, verbose_name=_('Region Name'), blank=True, null=True)

    createuser = models.ForeignKey(User, related_name='created_districts', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_districts', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)


    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')
        unique_together = (('name', 'region'), )

    class Admin:
        list_display = ('name',)
        search_fields = ['name',]


    def __unicode__(self):
        return u"%s" % (self.name,)


class TownType(models.Model):
    shortname = models.CharField(maxlength=5, blank=True, null=True)
    name = models.CharField(maxlength=60, blank=True, null=True)

    createuser = models.ForeignKey(User, related_name='created_towntypes', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_towntypes', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)


    class Meta:
        verbose_name = _('TownType')
        verbose_name_plural = _('TownTypes')


    class Admin:
        pass


    def __unicode__(self):
        return u"%s" % self.shortname


class Town(models.Model):
    #code = models.CharField(_('Town Code'), maxlength=6)
    country = models.ForeignKey(Country, blank=True, null=True, verbose_name=_('Country'))
    region = models.ForeignKey(Region, blank=True, null=True, verbose_name=_('Region'))
    district = models.ForeignKey(District, blank=True, null=True, verbose_name=_('District'))
    type = models.ForeignKey(TownType, verbose_name=_('Type'), blank=True, null=True)
    name = models.CharField(_('Town Name'), maxlength=35)
    is_region_centre = models.BooleanField(_('IRC?')) #Is Region Centre?
    is_district_centre = models.BooleanField(_('IDC?')) #Is District Centre?

    createuser = models.ForeignKey(User, related_name='created_towns', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_towns', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)
    

    def __unicode__(self):
      return self.name


    class Meta:
        verbose_name = _('Town')
        verbose_name_plural = _('Towns')
        ordering = ('name',)


    class Admin:
      	list_display = ('type','name','region','district','is_region_centre','is_district_centre')
        #js = ('js/tiny_mce/tiny_mce.js','js/tiny_mce/textareas.js'),
      	list_filter = ['createdate']
        search_fields = ['name',]



class StreetType(models.Model):
    shortname = models.CharField(maxlength=5, blank=True, null=True)
    name = models.CharField(maxlength=60, blank=True, null=True)

    createuser = models.ForeignKey(User, related_name='created_streettypes', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_streettypes', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)


    class Meta:
        verbose_name = _('StreetType')
        verbose_name_plural = _('StreetTypes')


    class Admin:
        pass


    def __unicode__(self):
        return u"%s" % self.shortname



class Street(models.Model):
    #addr_code = models.CharField(_('Street Code'), maxlength=6)
    name = models.CharField(_('Street Name'), maxlength=100)
    #type = models.ForeignKey(StreetType, null=True)
	
    createuser = models.ForeignKey(User, related_name='created_streets', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_streets', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)


    class Meta:
        verbose_name = _('Street')
        verbose_name_plural = _('Streets')
        ordering = ('name',)


    class Admin:
      	list_display = ('name',)

        
    def __unicode__(self):
        return u"%s" %  self.name



PHONE_CHOICES = (
        ('P', _('City Number')),
        ('F', _('Fax Number')),
        ('M', _('Mobile Number')),
        )


class Phone(models.Model):
    type = models.CharField(_('Phone Type'), maxlength=1, choices=PHONE_CHOICES)
    number = models.CharField(_('Phone Number'), unique=True, maxlength=30)
    
    createuser = models.ForeignKey(User, related_name='created_phones', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_phones', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)
   

    class Meta:
        verbose_name = _('Phone')
        verbose_name_plural = _('Phones')


    class Admin:
        list_display = ('type','number','createuser')
        search_fields = ['number',]



    def __unicode__(self):
        return u"%s %s" % (self.type, self.number)


class PhoneList(models.Model):
    number = models.ForeignKey(Phone, verbose_name=_('Phone Number'))
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content'))
    object_id = models.IntegerField()

    createuser = models.ForeignKey(User, related_name='created_phonelist', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_phonelist', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)

    content_object = generic.GenericForeignKey()


    class Meta:
        verbose_name = _('Phone List')
        verbose_name_plural = _('Phone Lists')


    class Admin:
        list_display = ('number','content_type','object_id','createuser')


    def __unicode__(self):
        return u"%s" % (self.number)



class Addresstype(models.Model):
    shortname = models.CharField(_('Addresstype Short Name'), maxlength=20, unique=True)
    name = models.CharField(_('Addresstype Name'), maxlength=40)

    createuser = models.ForeignKey(User, related_name='created_addresstype', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_addresstype', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)


    class Meta:
        verbose_name = _('Address Type')
        verbose_name_plural = _('Address Types')


    class Admin:
        list_display = ('shortname','name','createuser')


    def __unicode__(self):
        return u"%s" % (self.shortname)



class Location(models.Model):
    zipcode = models.CharField(_('Zipcode'), maxlength=10, blank=True)
    town = models.ForeignKey(Town, blank=True, null=True, verbose_name=_('Town'))
    town_aux = models.ForeignKey(Town, related_name='town_aux', blank=True, null=True, verbose_name=_('Town (Aux.)'))
    street = models.ForeignKey(Street, blank=True, null=True, verbose_name=_('Street'))
    building = models.CharField(_('Building'), maxlength=35, blank=True)
    #extention = models.TextField(_('Extention'), cols=28, rows=5, blank=True)
    extention = models.TextField(_('Extention'), blank=True)

    createuser = models.ForeignKey(User, related_name='created_locations', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_locations', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)


    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')


    class Admin:
        list_display = ('zipcode','town','street','building','extention')


    def __unicode__(self):
        loc_str = u""
        if self.zipcode:
            loc_str = loc_str + u"%s" % self.zipcode
        if self.town:
#            for elem in (self.zipcode, self.town.country, self.town.region, self.town.district, self.town, self.street, self.building):
#                if elem:
#                    if loc_str:
#                        loc_str = loc_str + ", " + str(elem) 
#                    else:
#                        loc_str = str(elem)
			if not self.town.is_region_centre and self.town.district:
				loc_str = loc_str + u", %s" % self.town.region
				if not self.town.is_district_centre and self.town.district:
					loc_str = loc_str + u", %s" % (self.town.district,)
			loc_str = u"%s, %s%s" % (loc_str, self.town.type, self.town)
			for elem in (self.street, self.building):
				if elem:
					loc_str = loc_str + u", %s" % elem
                
        return loc_str



class Address(models.Model):
    location = models.ForeignKey(Location, verbose_name=_('Location'), blank=True, null=True)
    place = models.CharField(maxlength=15, blank=True)

    createuser = models.ForeignKey(User, related_name='created_addresses', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_addresses', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)


    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')


    class Admin:
        list_display = ('location', 'place')


    def __unicode__(self):
        if self.place:
            return u"%s, %s" % (self.location, self.place)
        else:
            return u"%s" % self.location



class Client(models.Model):
    #org = models.ForeignKey(Org, verbose_name=_('Org'))	
    #org_id = models.IntegerField()
    content_type = models.ForeignKey(ContentType, verbose_name=_('Content'))
    object_id = models.PositiveIntegerField()
    is_facture_required = models.BooleanField(_('Is Facture Required?'), blank=True, null=True)

    createuser = models.ForeignKey(User, related_name='created_clients', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_clients', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)

    content_object = generic.GenericForeignKey()

    def _name(self):
	return u"%s" % self.content_object.name
    name = property(_name)

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')


    class Admin:
        list_display = ('id','name')
        search_fields = ('id',)


    def __unicode__(self):
        return u"%s" % self.content_object 


    def _get_primary_contract(self):
        try:
            contract = self.contract_set.all()[0]
        except:
            contract = None

        return contract
    primary_contract = property(_get_primary_contract)


    def _get_accountants(self):
        try:
            empl_list = self.content_object.employee_set
            accountants = empl_list.select_related().filter(position__sort__exact=880)
            if not accountants:
                accountants = empl_list.select_related().filter(position__sort__exact=800)
            if accountants:
                accountants = accountants[0]
            else:
                accountants = None
        except:
            print "RA3VAT except in _get_accountants..."
            empl_list = {}
            accountants = None 
        return accountants
    accountants = property(_get_accountants)


    def _lookup(searchString='', filter_by=None):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute('''select common_org.name as name, common_client.id from common_client, common_org 
                where content_type_id=16 and object_id =common_org.id and common_org.name LIKE '%%%%%(search)s%%%%'  
                ''' % {'search':searchString})
        res1 = cursor.fetchall()
        ret1 = [[elem[0].decode('utf8'), elem[1]] for elem in res1]
        cursor.execute('''select (common_person.lastname ||' '|| common_person.firstname ||' '|| common_person.middlename) as name, 
                common_client.id from common_client, common_person 
                where content_type_id=10 and object_id =common_person.id and common_person.lastname LIKE '%%%%%(search2)s%%%%' 
                    ''' % {'search2':searchString})
        res2 = cursor.fetchall()
        ret2 = [[elem[0].decode('utf8'), elem[1]] for elem in res2]
        return ret1+ret2    			       
    lookup = staticmethod(_lookup)	


    def setContentData(self, obj):
	if obj:
	    #from django.contrib.contenttypes.models import ContentType
	    ct = ContentType.objects.filter(model__exact=obj._meta.module_name)
	    self.content_type = ct[0]
	    self.object_id = obj.id



    def _getStaffList(client, as_choices=True):
        obj_list = []
        if client:
            temp_list = client.content_object.employee_set.all()
            if temp_list:
                if as_choices:
                    obj_list = [(elem.person.fullname, elem.id) for elem in temp_list]
                else:
                    obj_list = temp_list
        return obj_list
    getStaffList = staticmethod(_getStaffList)


    def getInvoicesToBePaid(self):
	obj_list = self.invoice_set.all().extra(where=['paym_complete is not True and wontbepaid is not True'])
	return obj_list


class Person(models.Model):
    firstname = models.CharField(_('First Name'), maxlength=35, core=True)
    middlename = models.CharField(_('Middle Name'), maxlength=35, blank=True)
    lastname = models.CharField(_('Last Name'), maxlength=35)
    town = models.ForeignKey(Town, blank=True, null=True, verbose_name=_('Town'))
    #town = LookupField(Town, blank=True, null=True, verbose_name=_('Town'))
    #FIXME: define PhonesField
    #phones = PhonesField(Phone, blank=True)

    #email = models.EmailField(_('Email'), blank=True, validator_list=[isValidEmail], length=30)
    email = models.EmailField(_('Email'), blank=True, validator_list=[isValidEmail])
    web = models.CharField(_('Web Site'), maxlength=40, blank=True, null=True)
    im = models.CharField(_('Instant Messenger'), maxlength=40, blank=True, null=True)
    #info = models.TextField(_('Info'), blank=True, cols=28, rows=5)
    info = models.TextField(_('Info'), blank=True)
    #user = models.OneToOneField(User, verbose_name=_('User'))
    
    createuser = models.ForeignKey(User, related_name='created_people', blank=True, null=True)
    createdate = models.DateTimeField(blank=True, auto_now_add=True)
    modifyuser = models.ForeignKey(User, related_name='modified_people', blank=True, null=True)
    modifydate = models.DateTimeField(blank=True, auto_now=True)

    #context_list = ('PhoneList',)
    clients = generic.GenericRelation(Client) #, verbose_name=_('Client'), blank=True, null=True)


    def _get_fullname(self):
        return u"%s %s %s" % (self.lastname, self.firstname, self.middlename)

    fullname = property(_get_fullname)

    name = property(_get_fullname)


    def _get_phone_list(self):
		ct = ContentType.objects.get_for_model(self)
		phones = PhoneList.objects.filter(content_type__id__exact=ct.id, object_id__exact=self.id)
		return phones
    phone_list = property(_get_phone_list)
		

    def _get_employment_list(self):
		employment = Employee.objects.filter(person__id__exact=self.id)
		return employment
    employment_list = property(_get_employment_list)


    def _get_initials(self):
        last = u""
        first = u""
        middle = u""
        if self.lastname:
            last = u"%s" % self.lastname
        if self.firstname:
            first = u"%s." % self.firstname[:2]
            #first = self.firstname[0]
        if self.firstname:
            middle = u"%s." % self.middlename[:2]
            #middle = self.middlename[0]
        return u"%s %s%s" % (last, first, middle)
    initials = property(_get_initials)


    def get_phones(self):
        phone_list = u""
        for phone in self.phones.all():
            phone_list = phone_list + u" %s" % phone
        return phone_list
 
 
    class Meta:
        list_display_related = ('PersonAddress','PhoneList',)	
        verbose_name = _('Person')
        verbose_name_plural = _('People')
	lookup_options = {'field':'lastname', 'outfield':'fullname'}


    class Admin:
        js = ('/site_media/js/tags.js',)
        fields = (
            (None, {'fields': ('lastname','firstname','middlename','town','info', 'web','email','im')}),
            ('Date information',{'classes':'collapse','fields':('createuser','modifyuser','createdate','modifydate')}),	
        )     
        list_display = ('fullname','town','modifyuser')
        search_fields = ('lastname','firstname','middlename','info')


    def colored_name(self):
        return '<span style="color: red;">%s</span>' % (self.lastname) 
    colored_name.allow_tags = True


    def __unicode__(self):
        last = u""
        first = u""
        middle = u""
        if self.lastname:
            last = u"%s" % self.lastname
        if self.firstname:
            first = u"%s" % self.firstname
        if self.firstname:
            middle = u"%s" % self.middlename
        return u"%s %s %s" % (last, first, middle)

    
    
