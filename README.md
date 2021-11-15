# AllPawsInn
Dashboard source code for allpawsinns.com. Developed in Python with Pyqt5. MSSQL integrated.
0.    Dashboard – Show menu details
      

A.    Register new customer
-    Click “New Client” section from the left menu.
-    Enter the details like shown below.
      
-    Afterward, you need to add the pet information. 
-    Enter the details shown below
 
-    Afterward, you need to add the vet information.
-    Enter the details like shown below.

 
-     Then, simply click “Submit” button. 
-    Customer, new pet, and associated vet information is saved to database succesfully.
-    
B.    Customer – New pet
-    Click “Additional Animal” section from the left menu.
-    Then, search for either client or pet name.

 
-    Pick from the result list.
-    Enter the pet details below.

   

C.    Customer – Reservation
Note:    Follow the steps in section B first for the reservations with a new pet.
-    Enter the “Reservations” section from the left menu.
-    Then, search for the already added customer, or pet name.
 
-    After selecting the customer, simply pick the dates by clicking on them.
 
-    Then, you will see the dates as shown below. 
-    Select dates and click “Remove Dates” button in the middle, if needed.
-    If okay, click “Submit”. Now, you can view the reservation from the “Daily Schedule” and “Weekly Schedule” sections.
 
D.    Customer – Check in
Note: If customer is not registered, follow the steps in section A.
Note: If pet is not registered, follow the steps in section B.
-    Enter the “Daily Schedule” section from the left menu.
-    Find the customer’s name from the list then select it.
-    Click “Check-in” button. 
 
-    Note that program only allows you to check in in same day as the reservation.
-    So, if you cannot see the reservation, you probably looking to a different date.
-    Also, if you cannot check-in a customer and get an “Invalid Operation” error, check the date you are trying to check-in.
 
-    After checking in, you will see the customer in the middle list.
-    If customer wants to check out, follow the steps in E or F.

E.    Customer – Check out with payment
-    If you click “Check-out with payment”, you will have to follow these steps
-    Firstly, state any extra services or costs. See below.
-    Afterward, enter the payment information. See below.
-    Note that customers do not have to pay the whole amount.
      
F.    Customer – Check out without payment
-    If you click “Check-out with payment”, you will have to follow these steps
-    Enter the service details for further billing.
 
G.    Customer – Make payment
-    Enter the “Payment” section from the left menu.
-    Then, search for either client or pet name.
-    Select it. Now, you can see the client details below.
 
-    For simple payments, you can enter the amount to “Amount Received” section at very bottom.
-    Afterward, just click “Pay Remaining Balance”. This will reduce the balance.
-    We need a label saying services, same as “Payment” label. Poor UI/UX
-    Change payment to “take payment”
-    Look for previous receipts or bills. Itemized payment receipts. List of every services or costs, etc.
-    For detailed payments, use the section on the right.
-    After selecting the client, you can enter the payment information.
-    State any extras, discounts, and other required information.
-    See below.
 
-    When all finished, click the button below “Add to List”
-    Misaddition – no delete func. Add it.
-    Total amount needs to be truncated to space 2 decimal.
-    Look for the math in the python code.
-    Now, you will be able to see the payment below.
 
-    Afterward, you can enter the amount that you received from the customer. 
 
-    If you do not write anything to this box, program will terminate itself.
-    This is a bug needs to be fixed. For empty inputs, it should be assumed customer paid for the whole service fee which is stated in the list above.
H.    Edit customer
-    Firstly, search for the customer. Then select it.
 
-    Now, you need to be able to display any details associated with that customer.
-    See below.
 
-    Simply edit anything at the right section.
-    See below.
   
İ.    Display weekly schedule
-    Enter the “Weekly Schedule” section from the left menu.
-    This page includes no function for example, check-in, or delete, etc.  Can be added.
 
-    Make “Show Today” button work.
