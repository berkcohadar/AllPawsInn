TotalCharges=0
current_client=-1
from http import client
from Reports_functions import *
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime

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

        for item in animalInfo:
            animalName = item['AnimalName']
            animalSize = item['Size']
            animalBreed = item['Breed']
            animalDateIn = item['DateIn']
            animalDateOut = item['DateOut']
            animalDaysIn = item['NoDays']
            
        self.ui.pay_animal_name.setText(animalName)
        self.ui.pay_animal_size.setText(animalSize)
        self.ui.pay_animal_breed.setText(animalBreed)
        self.ui.pay_animal_date_in.setText(str(animalDateIn))
        self.ui.pay_animal_date_out.setText(str(animalDateOut))
        self.ui.pay_animal_day.setText(str(animalDaysIn))

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
        PaymentFunctions.AddServices(self)
       
    def AddServices(self):
        object = Database_Class()
        othergoods = self.ui.pay_services_other_goods.text()
        if (othergoods == ''):
            othergoods = '0'

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
        
        x = Decimal(totalCharges)
        output = round(x,2)

        round(Decimal(),2)   
        self.ui.pay_subtotal.setText("{:.2f}".format(output))
        
    def AddServiceDetail(self,received):
        global TotalCharges
        object = Database_Class()

        foodFee = 0.0
        hairFee = 0.0
        nailFee = 0.0
        careFee = 0.0

        othergoods = self.ui.pay_services_other_goods.text()
        discount = self.ui.pay_services_discount.text()

        if (othergoods == ''):
            othergoods = 0.0
        else:
            othergoods = float(othergoods)

        if (discount == ''):
            discount = 0.0
        else:
            discount = float(discount)
        
        
        dayCare = object.GetDayCareRateAndTax(4)
        for item in dayCare:
            if self.ui.pay_daycare_checkbox.isChecked():
                careFee = float(item[0])
            tax = float(item[1])/100

        subTotal = 0.0
        if self.ui.pay_services_food.isChecked():
            food = object.GetServicesFees('food')
            for i in food:
                foodFee = float(i[0])
            subTotal += foodFee
        if self.ui.pay_services_hair.isChecked():
            hair = object.GetServicesFees('hair')
            for i in hair:
                hairFee = float(i[0])
            subTotal += hairFee
        if self.ui.pay_services_nails.isChecked():
            nail = object.GetServicesFees('nails')
            for i in nail:
                nailFee = float(i[0])
            subTotal += nailFee
        
        subTotal += (careFee + othergoods - discount)
        subTotal += subTotal * tax 

        paid = subTotal == received
        Client_ID = int(self.ui.pay_search_list.currentItem().text(4))

        dateIn = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        dateOut = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        #DATE CONVERSION FAILS
        serviceID = object.addServicesDetails(careFee, nailFee, foodFee, hairFee, othergoods, subTotal, discount, "", Client_ID, tax, dateIn, dateOut, paid)
        return subTotal

    def SubmitPayments(self):
        global TotalCharges
        if(self.ui.pay_services_amt_recieved.text()):
            object = Database_Class()
            if(self.ui.pay_search_list.currentItem()):
                clientId =self.ui.pay_search_list.currentItem().text(4) # CAN BE SELECTED FROM clients ARRAY
                received = float(self.ui.pay_services_amt_recieved.text())

                PaymentFunctions.AddServiceDetail(self,received)
                PaymentFunctions.findUnpaidReservations(self)
                # if (iterator.value()): # Receipt
                #     name =self.ui.pay_search_list.currentItem().text(0)
                #     canvas = Canvas(name+" receipt.pdf")
                #     canvas.drawString(100, 500, "Name")
                #     canvas.drawString(200, 500, name)
                    
                #     line_height_counter=0
                #     counter=1
                #     total=0
                #     canvas.drawString(100, 470, "Service Costs")
                #     while iterator.value():
                #         item = iterator.value()
                #         canvas.drawString(100, 455-line_height_counter, "Service-"+str(counter))
                #         canvas.drawString(200, 455-line_height_counter, item.text(1))
                #         line_height_counter += 15
                #         iterator += 1
                #         counter+=1
                #         total+=round(float(item.text(2)),2)

                #     canvas.drawString(100, 440-line_height_counter, "Total Cost")
                #     canvas.drawString(200, 440-line_height_counter, str(total))

                #     canvas.drawString(100, 410-line_height_counter, "Amount Paid")
                #     canvas.drawString(100, 395-line_height_counter, "Updated Balance")   

                #     canvas.drawString(200, 410-line_height_counter, "{:.2f}".format(float(received)))
                #     canvas.drawString(200, 395-line_height_counter, "{:.2f}".format(newbalance))
                #     canvas.save()
            else:
                MainWindow.show_popup(self,"Missing Client!","Please search and choose a client")
            
        else:
            MainWindow.show_popup(self,"Missing Arguments!","Please enter amount of received")
        
    def DecreaseAccountBalance(self):
        object = Database_Class()
        
        if(self.ui.pay_remaining_amt_recieved.text()):
            if(self.ui.pay_search_list.currentItem()):
                received = self.ui.pay_remaining_amt_recieved.text()
                clientId =self.ui.pay_search_list.currentItem().text(4)
                print(clientId)
                object.DecreaseAccountBalance(int(clientId),float(received))
                PaymentFunctions.DisplayDetail(self)
                self.ui.pay_remaining_amt_recieved.clear()
            else:
                MainWindow.show_popup(self,"Missing Client!","Please search and choose a client or pet")
        else:
            MainWindow.show_popup(self,"Missing Arguments!","Please enter amount of received")
        
    def findUnpaidReservations(self):
        self.ui.pay_list_widget.clear()
        animalId= 1
        clientId = int(self.ui.pay_search_list.currentItem().text(4))

        object = Database_Class()

        result = object.findUnpaidReservations(animalID=animalId,clientID=clientId)
        
        for item in result:
            self.ui.pay_list_widget.addTopLevelItem(QtWidgets.QTreeWidgetItem([  item["dateIn"].strftime("%m/%d/%Y"), item["dateOut"].strftime("%m/%d/%Y"), str(float(item["subTotal"]) - float(item["paidAmount"])) , str(float(item["subTotal"])), str(clientId), str(animalId), str(item["serviceID"])] ))

    def payForUnpaidReservation(self):
        if (self.ui.pay_list_widget.currentItem()):
            clientId = int(self.ui.pay_list_widget.currentItem().text(4))
            animalId = int(self.ui.pay_list_widget.currentItem().text(5))
            serviceId = int(self.ui.pay_list_widget.currentItem().text(6))

            unpaid_balance = float(self.ui.pay_list_widget.currentItem().text(2))
            total_balance = float(self.ui.pay_list_widget.currentItem().text(3))

            amount_received = float(self.ui.pay_services_amt_recieved_2.text())
            object = Database_Class()

            if (amount_received > unpaid_balance):
                MainWindow.show_popup(self,"Invalid Amount!","Received amaount must be less than Unpaid Balance")
            else:
                totalPaid = amount_received + (total_balance - unpaid_balance)
                debtClosed = totalPaid == total_balance
                object.payForUnpaidReservation(amount=totalPaid,paid=debtClosed,animalID=animalId,clientID=clientId,serviceID=serviceId)

                self.ui.pay_services_amt_recieved_2.clear()
                PaymentFunctions.findUnpaidReservations(self)

        else:
            MainWindow.show_popup(self,"Invalid Operation!","Please select a reservation to take payment!")




#self.ui.pay_add_list_btn_2.clicked.connect(lambda: PaymentFunctions.AddToList(self))
#self.ui.deleteRow_button.clicked.connect(lambda: PaymentFunctions.removeFromList(self))