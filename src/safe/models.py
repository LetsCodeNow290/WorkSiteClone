from django.db import models
from django.contrib.auth.models import User
from components.models import Drug
from django.db.models import Sum, Max


# Create your models here.

class Safe(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now=True)
    drug_name = models.ForeignKey('components.Drug', related_name='drug_remove', on_delete=models.PROTECT, default=0, limit_choices_to={'is_active_safe': True})
    amount_removed = models.IntegerField(blank=True, null=True)
    amount_added = models.IntegerField(blank=True, null=True)
    amount_in_safe = models.IntegerField(blank=True, null=True)
    incident_number = models.CharField(max_length=20, default='', blank=True)
    patient_name = models.CharField(max_length=20, default='', blank=True)
    medic_unit = models.ForeignKey('components.MedicUnit', related_name='medic_unit', on_delete=models.PROTECT, blank=True, null=True)
    free_text = models.TextField(default='', blank =True)
   
    class Meta:
        permissions = (
            ('can_view', "View This"),
            ('can_add', 'Add to the Safe')
            )
        

    def calc_total(self):
        add = 0
        sub = 0
        total = 0
        drugs = {}
        for drug in Drug.objects.all():
            try:
                add_drug = self.objects.filter(drug_name__name=drug).aggregate(Sum('amount_added'))
                if add_drug['amount_added__sum'] == None:
                    add_drug['amount_added__sum'] = 0
                add+=add_drug['amount_added__sum']
                sub_drug = self.objects.filter(drug_name__name=drug).aggregate(Sum('amount_removed'))        
                if sub_drug['amount_removed__sum'] == None:
                    sub_drug['amount_removed__sum'] = 0
                sub+=sub_drug['amount_removed__sum']
                total = add-sub
                drugs.update({drug:total})
                add=0
                sub=0
                total=0
            except:
                continue
        return drugs
            

    def get_check_date(self):
        check_date = {}
        for drug in Drug.objects.all():
            try:
                date = self.objects.filter(drug_name__name=drug).aggregate(Max('date_created'))
                check_date.update({drug:date['date_created__max']})
            except:
                continue
        return check_date