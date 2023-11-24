 1. models.py
Defines the models: Vendor, PurchaseOrder, and HistoricalPerformance.
Includes methods for calculating metrics and handling data operations.

2. admin.py
Registers models in the Django admin interface (Vendor, PurchaseOrder, and HistoricalPerformance).
Defines custom admin classes for better representation in the admin interface.

3. views.py
Contains viewsets and APIView classes for handling CRUD operations and retrieving performance metrics for vendors.
Includes signal receivers for updating vendor metrics based on purchase order events.

4. urls.py
Configures URL patterns using Django's path() and include() functions.
Defines routes for API endpoints related to vendors, purchase orders, vendor performance, and acknowledging purchase orders.

Additional Notes:
 * Ensure that the provided logic for metric calculation and   handling of events related to purchase orders and vendors works as expected.
* Document the API endpoints thoroughly in the README file, including details on how to use them and what each endpoint does.
* Consider adding further validation and error handling to the code for robustness.
* Review the signal receivers to ensure they're triggered appropriately upon events and updates.
