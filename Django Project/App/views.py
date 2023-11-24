from rest_framework import viewsets
from rest_framework.response import Response
from .models import Vendor , PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializers
from rest_framework.views import APIView


class VendorViewSet(viewsets.ViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    def list(self, request):
        vendors = self.queryset
        serializer = self.serializer_class(vendors, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def retrieve(self, request, pk=None):
        vendor = Vendor.objects.get(pk=pk)
        serializer = self.serializer_class(vendor)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        vendor = Vendor.objects.get(pk=pk)
        serializer = self.serializer_class(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)  # Changed status to 200 for successful update
        return Response(serializer.errors, status=400)
    
    def partial_update(self, request, pk=None):
        vendor = Vendor.objects.get(pk=pk)
        serializer = self.serializer_class(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)  # Changed status to 200 for successful partial update
        return Response(serializer.errors, status=400)
    
    def destroy(self, request, pk=None):
        vendor = Vendor.objects.get(pk=pk)
        vendor.delete()
        return Response(status=204)



    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor does not exist'}, status=404)
        
        response_time_seconds = vendor.average_response_time.total_seconds()

        performance_metrics = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating': vendor.quality_rating_avg,
            'response_time': response_time_seconds,
            'fulfillment_rate': vendor.fulfillment_rate,
        }    
        return Response(performance_metrics)
   

class VendorPerformanceView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor does not exist'}, status=404)
        
        average_response_time = vendor.average_response_time

        performance_metrics = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating': vendor.quality_rating_avg,
            'response_time': str(average_response_time),  
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(performance_metrics)


class AcknowledgePurchaseOrder(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order does not exist'}, status=404)
        
        purchase_order.acknowledge()  # Call the acknowledge method in the PurchaseOrder model
        return Response({'message': 'Purchase Order acknowledged successfully'})


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    purchaseorder = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializers


from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics_on_po_save(sender,instance, **kwargs):
    if instance.status == 'completed':
        instance.vendor.update_metrics()

@receiver(pre_delete, sender=PurchaseOrder)
def update_vendor_metrics_on_po_delete(sender, instance, **kwargs):
    if instance.status == 'completed':
        instance.vendor.update_metrics


