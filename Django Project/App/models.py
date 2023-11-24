from django.db import models
from django.utils import timezone
from datetime import timedelta



class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate =models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    def calculate_on_time_delivery_rate(self):
        completed_pos = self.purchaseorder_set.filter(status='completed')
        total_completed_pos = completed_pos.count()
        on_time_deliveries = completed_pos.filter(delivery_date__lte=timezone.now()).count()
        
        if total_completed_pos > 0:
            self.on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100
        else:
            self.on_time_delivery_rate = 0
        self.save()
    
    def calculate_quality_rating_avg(self):
        completed_pos_with_rating = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=False)
        avg_rating = completed_pos_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
        return avg_rating or 0
    
    def calculate_average_response_time(self):
        acknowledged_pos = self.purchaseorder_set.filter(acknowledgment_date__isnull=False)
        
        if acknowledged_pos.exists():
            response_times = [
                (po.acknowledgment_date - po.issue_date).total_seconds()
                for po in acknowledged_pos
                if po.acknowledgment_date and po.issue_date
            ]
            
            if response_times:
                return sum(response_times) / len(response_times)
        
        return 0
   
    def calculate_fulfillment_rate(self):
        total_pos = self.purchaseorder_set.count()
        completed_pos_without_issues = self.purchaseorder_set.filter(status='completed', quality_rating__isnull=True).count()
        if total_pos > 0:
            return (completed_pos_without_issues / total_pos)* 100 if completed_pos_without_issues <= total_pos else 100.0
        else:
            return 0


class PurchaseOrder(models.Model):
    STARUS_CHOICES =(
        ('pending','Pending'),
        ('conpleted','Completed'),
        ('canceled',' Canceled'),
    )
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(max_length=50 , unique=True)
    order_data = models.DateTimeField()
    delivery_data = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STARUS_CHOICES,default='pending' )
    quality_rating = models.FloatField(null=True, blank=True)
    issue_data = models.DateTimeField()
    acknowledgment_data = models.DateTimeField(null=True, blank=True)
   
    def __str__(self):
        return self.po_number
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        if self.status == 'completed' and self.delivery_data <= timezone.now():
           self.vendor.on_time_delivery_rate = self.vendor.calculate_on_time_delivery_rate()
           self.vendor.save()
        
        if self.quality_rating is not None:
            self.vendor.quality_rating_avg = self.vendor.calculate_quality_rating_avg()
            self.vendor.save()

        if self.acknowledgment_data is not None:
            self.vendor.average_response_time = self.vendor.calculate_average_response_time()
            self.vendor.save()
        
        if self.status == 'completed':
           self.vendor.fulfillment_rate = self.vendor.calculate_fulfillment_rate()
           self.vendor.save()
   

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillmet_rate = models.FloatField()

    def __str__(self):
       return f"{self.vendor.name} - {self.date.strftime('%Y-%m-%d')}"

