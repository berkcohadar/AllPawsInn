TotalCharges=0
current_client=-1
from asyncio.windows_events import NULL
from http import client
from Reports_functions import *
from datetime import datetime
from PyQt5.QtGui import QColor

class PaymentFunctions(MainWindow):

    def clearPayments(self):
        self.ui.pay_search_list.clear()

    def updatePaymentDisplay(self):  
        self.ui.pay_search_list.clear()
        object = Database_Class()
        for obj in self.paws:  
            animalID = str(obj[3]) 
            clientID = str(obj[4]) 
            animalName = obj[2] 
            ownerName = obj[0] + " " + obj[1]
            clientInfo = object.GetClientInfo(int(clientID))
            for client in clientInfo:
                clientBalance = client['AccountBalance']
            self.ui.pay_search_list.addTopLevelItem( QtWidgets.QTreeWidgetItem([ownerName , animalName, str(clientBalance) ,animalID,clientID] ) )

    def updatePaymentList(self):
        self.ui.pay_search_list.setHeaderHidden(False)
        self.ui.pay_list_widget.setHeaderHidden(False)

        text = self.ui.pay_search_bar.text()
            
        if len(text) < 3:
            PaymentFunctions.clearPayments(self)
            self.paws= []
        else:
            object = Database_Class()

            result = object.SearchForPayment()
           
            for paw in result:
                
                if text.lower() in paw[0].lower() or text.lower() in paw[1].lower() or text.lower() in paw[2].lower():
            
                    if paw not in self.paws:
                        self.paws.append(paw)           
                else:
                    if paw in self.paws:
                        print(paw)
                        self.paws.remove(paw)
            PaymentFunctions.updatePaymentDisplay(self)  

    def DisplayDetail(self): # THIS FUNCTION IS CALLED WHEN A CUSTOMER IS CHOSEN FROM THE SEARCH LIST IN THE PAYMENT PAGE
        global current_client   
        
        animalId= self.ui.pay_search_list.currentItem().text(3)
        clientId = self.ui.pay_search_list.currentItem().text(4)

        if(current_client != -1 and current_client != clientId): # IF A CLIENT IS CHOSEN BEFORE, AND THIS CLIENT IS NOT THE SAME AS THE NEWLY CHOSEN CLIENT, AND THE SERVICES LIST IS NOT EMPTY.
            self.ui.pay_list_widget.clear()
        
        current_client = clientId # selected client's id is saved to the global instance.

        object = Database_Class()
        animalInfo = object.GetAnimalInfo(int(animalId))
        clientInfo = object.GetClientInfo(int(clientId))
        animalDateIn = ""
        animalDateOut = ""
        animalDaysIn = ""
        serviceDetails = ""

        try:
            serviceDetails = object.getLastServicesDetails(animalId)[0]
            animalDateIn = serviceDetails['resStartDate'].strftime("%Y-%m-%d")
            animalDateOut = serviceDetails['resEndDate'].strftime("%Y-%m-%d")
            animalDaysIn = str(serviceDetails['daysIn'])
        except:
            pass
        
        print(animalDateIn,animalDateOut,animalDaysIn)

        for item in animalInfo:
            animalName = item['AnimalName']
            animalSize = item['Size']
            animalBreed = item['Breed']

            
        self.ui.pay_animal_name.setText(animalName)
        self.ui.pay_animal_size.setText(animalSize)
        self.ui.pay_animal_breed.setText(animalBreed)
        self.ui.pay_animal_date_in.setText(animalDateIn)
        self.ui.pay_animal_date_out.setText(animalDateOut)
        self.ui.pay_animal_day.setText(animalDaysIn)

        for client in clientInfo:
            clientName = client['FirstName'] + " " + client['LastName']
            clientTown =  client['Town'] +", " if client['Town'] else ""
            clientPostCode = client['PostcodeZIP'] if client['PostcodeZIP'] else ""
            clientAddress = client['Address1']  + "\n" + clientTown + clientPostCode
            clientCell = client['CellMobile']
            clientNotes = client['Email']
            if client['AccountBalance'] :
                clientBalance = client['AccountBalance']
            else:
                clientBalance = 0
                object.SetClientAccountBalance(int(clientId),float(0))

        self.ui.pay_client_name.setText(clientName)
        self.ui.pay_client_address.setText(clientAddress)
        self.ui.pay_client_cellphone.setText(clientCell)
        self.ui.pay_client_notes.setText(clientNotes)
        self.ui.pay_client_balance.setText("{:.2f}".format(clientBalance))

        servicesinfo= object.GetDayCareRateAndTax(4)

        for  service in servicesinfo:
            daycarerate = service[0]
            tax = service[1]

        self.ui.pay_daycare_rate.setText("{:.2f}".format(daycarerate))
        self.ui.pay_nys_tax.setText("{:.2f}".format(tax))
        PaymentFunctions.calculateService(self)
       
    def calculateService(self):
        object = Database_Class()
        othergoods = self.ui.pay_services_other_goods.text()
        if (othergoods == ''):
            othergoods = '0'

        amount_received = self.ui.pay_services_amt_recieved.text()
        if (amount_received == ''):
            amount_received = '0'    

        foodFeeArray = object.GetServicesFees('food')
        for item in foodFeeArray:
            foodFee = item[0]
     
        hairFeeArray = object.GetServicesFees('hair')
        for item2 in hairFeeArray:
            hairFee = item2[0]

        nailFeeArray = object.GetServicesFees('nails')
        for item3 in nailFeeArray:
            nailFee = item3[0]

        servicesinfo= object.GetDayCareRateAndTax(4)
        discount = self.ui.pay_services_discount.text()
        if discount == '':
            discount= '0'
        
        daycarerate = 0
        for  service in servicesinfo:
            if self.ui.pay_daycare_checkbox.isChecked():
                daycarerate = service[0]
            tax = service[1]

        servicesSubTotal = 0
        if self.ui.pay_services_food.isChecked():
            servicesSubTotal += foodFee
        
        if self.ui.pay_services_hair.isChecked():
            servicesSubTotal += hairFee

        if self.ui.pay_services_nails.isChecked():
            servicesSubTotal += nailFee

        floatTotal = float(servicesSubTotal)
        floatTotal+= float(daycarerate) + float(othergoods) - float(discount) 


        totalCharges =   format((floatTotal * tax/100 + floatTotal),'.2f' )

        pay_remaining = float(totalCharges) - float(amount_received)
        self.ui.pay_remaining.setText("{:.2f}".format(pay_remaining))

        x = Decimal(totalCharges)
        output = round(x,2)

        round(Decimal(),2)   
        self.ui.pay_subtotal.setText("{:.2f}".format(output))

    def AddServiceDetail(self):
        global TotalCharges
        object = Database_Class()

        # Set variables as 0.
        foodFee = 0.0
        hairFee = 0.0
        nailFee = 0.0
        careFee = 0.0
        subTotal = 0.0

        # Set othergoods and discount
        othergoods = self.ui.pay_services_other_goods.text()
        discount = self.ui.pay_services_discount.text()

        # Set othergoods by checking UI input
        if (othergoods == ''):
            othergoods = 0.0
        else:
            othergoods = float(othergoods)

        # Set discount by checking UI input
        if (discount == ''):
            discount = 0.0
        else:
            discount = float(discount)
        

        # Get dayCare fee from database
        dayCare = object.GetDayCareRateAndTax(4)
        for item in dayCare:
            if self.ui.pay_daycare_checkbox.isChecked():
                careFee = float(item[0])
            tax = float(item[1])/100

        # Get food fee from database
        if self.ui.pay_services_food.isChecked():
            food = object.GetServicesFees('food')
            for i in food:
                foodFee = float(i[0])
            subTotal += foodFee

        # Get hair fee from database
        if self.ui.pay_services_hair.isChecked():
            hair = object.GetServicesFees('hair')
            for i in hair:
                hairFee = float(i[0])
            subTotal += hairFee
        
        # Get nail fee from database
        if self.ui.pay_services_nails.isChecked():
            nail = object.GetServicesFees('nails')
            for i in nail:
                nailFee = float(i[0])
            subTotal += nailFee
        
        # Calculate subTotal with tax
        subTotal += (careFee + othergoods - discount)
        taxTotal = subTotal * tax 
        subTotal += taxTotal

        received = 0.0
        if (self.ui.pay_services_amt_recieved.text() != ''):
            received = float(self.ui.pay_services_amt_recieved.text())
            
        animalId= int(self.ui.pay_search_list.currentItem().text(3))
        clientId = int(self.ui.pay_search_list.currentItem().text(4))
        dateIn = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dateOut = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resStartDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        resEndDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
        serviceID = object.addServicesDetails(careFee, nailFee, foodFee, hairFee, othergoods, subTotal, discount, clientId, animalId, taxTotal, dateIn, dateOut, resStartDate, resEndDate, 1, 1, 1, 1)
        PaymentFunctions.payForClient(self,serviceID=serviceID,paymentAmount=received)
        return subTotal

    def createService(self):
        if(self.ui.pay_search_list.currentItem()):
            PaymentFunctions.AddServiceDetail(self)
        else:
            MainWindow.show_popup(self,"Missing Client!","Please search and choose a client")
                
    def findAllReservations(self):
        self.ui.pay_list_widget.clear()
        animalName = self.ui.pay_search_list.currentItem().text(1)
        animalId = int(self.ui.pay_search_list.currentItem().text(3))
        clientId = int(self.ui.pay_search_list.currentItem().text(4))

        object = Database_Class()

        result = object.findAllReservations(animalID=animalId,clientID=clientId)
        index = -1
        for item in result:
            if item['checkedIn'] == 1:
                status = "Checked In"
            else:
                status = "Reserved"
            
            if item['checkedOut'] == 1:
                status = "Checked Out"

            if item['completed'] == 1:
                status = "Completed"

            self.ui.pay_list_widget.addTopLevelItem(QtWidgets.QTreeWidgetItem([  item["resStartDate"].strftime("%m/%d/%Y"), item["resEndDate"].strftime("%m/%d/%Y"), animalName ,"{:.2f}".format(float(item["subTotal"])), status, str(clientId), str(animalId), str(item["serviceID"])] ))
            index += 1
            today = datetime.now().date()
            if (today>=item["resStartDate"].date() and today<=item["resEndDate"].date() and item['completed'] != 1):

                self.ui.pay_list_widget.topLevelItem(index).setBackground(0, QColor(25, 135, 84, 255) )
                self.ui.pay_list_widget.topLevelItem(index).setBackground(1, QColor(25, 135, 84, 255) )
                self.ui.pay_list_widget.topLevelItem(index).setBackground(2, QColor(25, 135, 84, 255) )
                self.ui.pay_list_widget.topLevelItem(index).setBackground(3, QColor(25, 135, 84, 255) )
                self.ui.pay_list_widget.topLevelItem(index).setBackground(4, QColor(25, 135, 84, 255) )

    def payForClient(self,serviceID=NULL,paymentAmount=NULL):
        if (self.ui.pay_search_list.currentItem()):
            
            object = Database_Class()
            clientId = int(self.ui.pay_search_list.currentItem().text(4))
            today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if (serviceID!=NULL):
                paymentId = object.createPayment(customerId=clientId, paymentAmount=paymentAmount, paymentDate= today, paymentType="", serviceID=serviceID)
                ReportFunctions.printReceiptWithService(ReportFunctions, customerID=clientId, serviceID=serviceID)

            else:
                amount_received = 0.0
                if (self.ui.pay_services_amt_recieved_2.text() != ''):
                    amount_received = float(self.ui.pay_services_amt_recieved_2.text())                  
                
                paymentId = object.createPayment(customerId=clientId, paymentAmount=amount_received, paymentDate= today, paymentType="", serviceID=NULL)
                ReportFunctions.printReceiptWithoutService(ReportFunctions, customerID=clientId, paymentID=paymentId)

            PaymentFunctions.refreshPaymentPage(self)
            
        else:
            MainWindow.show_popup(self,"Invalid Operation!","Please select a customer to take payment!")

    def refreshPaymentPage(self):
        PaymentFunctions.findAllReservations(self)
        PaymentFunctions.DisplayDetail(self)
        PaymentFunctions.updatePaymentList(self)
