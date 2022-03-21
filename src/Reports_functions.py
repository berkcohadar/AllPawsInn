from reportlab.pdfgen.canvas import Canvas
from DatabaseClass import Database_Class
from Home_Functions import *

#from main import MainWindow

class ReportFunctions(MainWindow):

    def clearSearch(self):
        self.ui.report_search_list.clear()

    def updatePaymentDisplay(self):  
        self.ui.report_search_list.clear()
        object = Database_Class()
        for obj in self.paws:  
            animalID = str(obj[3]) 
            clientID = str(obj[4]) 
            animalName = obj[2] 
            ownerName = obj[0] + " " + obj[1]
            clientInfo = object.GetClientInfo(int(clientID))
            for client in clientInfo:
                clientBalance = client['AccountBalance']
            self.ui.report_search_list.addTopLevelItem( QtWidgets.QTreeWidgetItem([ownerName , animalName, str(clientBalance) ,animalID,clientID] ) )

    def updateClientsList(self):
        #   Payments.ClientID Payments.AmountReceived Payments.PaymentType Payments.BookingID
        # ClientDetails.LastName ClientDetails.FirstName ClientDetails.AccountBalance

        text = self.ui.report_search_bar.text()
            
        if len(text) < 3:
            ReportFunctions.clearSearch(self)
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
            ReportFunctions.updatePaymentDisplay(self)        

    def updatePaymentsList(self):
        clientId = int(self.ui.report_search_list.currentItem().text(4))
        object = Database_Class()

        result = object.GetPaymentsbyClient(clientID=clientId)

        for item in result:
            self.ui.payment_history_table.addTopLevelItem(QtWidgets.QTreeWidgetItem([  item["PaymentDate"].strftime("%m/%d/%Y"), item["PaymentType"], "{:.2f}".format(float(item["AmountReceived"])), str(clientId), str(item["PaymentId"]), str(item["BookingID"])] ))

"""
    def DisplayDetail(self): # THIS FUNCTION IS CALLED WHEN A CUSTOMER IS CHOSEN FROM THE SEARCH LIST IN THE PAYMENT PAGE
        global current_client   
        
        animalId= self.ui.report_search_list.currentItem().text(3)
        clientId = self.ui.report_search_list.currentItem().text(4)
        index = self.ui.pay_list_widget.topLevelItemCount() # index of the first element on the payListWidget. If -1, then the list is empty

        print("\n\nclients : ",current_client, clientId, index)
        if(current_client != -1 and current_client != clientId and index != 0): # IF A CLIENT IS CHOSEN BEFORE, AND THIS CLIENT IS NOT THE SAME AS THE NEWLY CHOSEN CLIENT, AND THE SERVICES LIST IS NOT EMPTY.
            ReportFunctions.clearServicesList(self)
        
        current_client = clientId # selected client's id is saved to the global instance.
        print("\n\nclients : ",current_client, clientId, index)

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
        ReportFunctions.AddServices(self)
       
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

        for  service in servicesinfo:
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
        
    def AddToList(self):
        global current_client
        global TotalCharges     
        if(self.ui.report_search_list.currentItem()):
            clientId =self.ui.report_search_list.currentItem().text(4)
            if(clientId == current_client):
                object = Database_Class()
                animalId= self.ui.report_search_list.currentItem().text(3)
                animalInfo = object.GetAnimalInfo(int(animalId))
                for item in animalInfo:
                    animalName= item['AnimalName']
                    
                ReportFunctions.AddServiceDetail(self,animalName)
            else:
                MainWindow.show_popup(self,"Wrong Client!","Client are not same.")
        else:
            MainWindow.show_popup(self,"Missing Client!","Please search and choose a pet")

    def AddServiceDetail(self, animalName):
        global TotalCharges
        object = Database_Class()

        sub =  self.ui.pay_subtotal.text()

        foodFee = 0.0
        hairFee = 0.0
        nailFee = 0.0
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
            dayCareRate = float(item[0])
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
        
        subTotal += (dayCareRate + othergoods - discount)
        subTotal += subTotal * tax 

        Client_ID = int(self.ui.report_search_list.currentItem().text(4))

        serviceID = object.addServicesDetails(dayCareRate, nailFee, foodFee, hairFee, othergoods, subTotal, discount, "", Client_ID, tax)

        self.ui.pay_list_widget.addTopLevelItem(QtWidgets.QTreeWidgetItem([  animalName, str(sub), str(serviceID)] ))

        TotalCharges += float(sub)
        TotalCharges = round(TotalCharges,2)

        balance =self.ui.pay_client_balance.text()

        totalBalance = TotalCharges + float(balance)
        totalBalance = round(totalBalance,2)

        self.ui.pay_total_balance.setText("{:.2f}".format(totalBalance))
        self.ui.pay_total_charge.setText("{:.2f}".format(TotalCharges))

    def removeFromList(self):
        # ADD =>
        # ` self.ui.BUTTON_NAME.clicked.connect(lambda: ReportFunctions.removeFromList(self)) `
        # to main.py
        global TotalCharges         
        if(self.ui.report_search_list.currentItem()):
            if (self.ui.pay_list_widget.currentItem()):
                object = Database_Class()
                
                sub = self.ui.pay_list_widget.currentItem().text(1) # this is the subtotal that will be reducted from total charge.

                serviceID = self.ui.pay_list_widget.currentItem().text(2)
                Client_ID = int(self.ui.report_search_list.currentItem().text(4))

                object.removeServicesDetails(serviceID=serviceID,Client_ID=Client_ID,subTotal=sub)

                # find item and remove it from list.
                index = self.ui.pay_list_widget.indexOfTopLevelItem(self.ui.pay_list_widget.currentItem()) # this is the index of desired row.
                print(index)
                item = self.ui.pay_list_widget.takeTopLevelItem(index)

                # subtract sub_total from total charges.
                TotalCharges -= float(sub)
                TotalCharges = round(TotalCharges,2)

                # calculate total balance again.
                balance =self.ui.pay_client_balance.text()
                totalBalance = TotalCharges + float(balance)
                totalBalance = round(totalBalance,2)
                self.ui.pay_total_balance.setText("{:.2f}".format(totalBalance))
                self.ui.pay_total_charge.setText("{:.2f}".format(TotalCharges))
            else:
                MainWindow.show_popup(self,"Missing item!","Please choose an item from list and try again!")
        else:
            MainWindow.show_popup(self,"Missing Client!","Please search and choose a pet")

    def createService(self):
        global TotalCharges
        if(self.ui.pay_services_amt_recieved.text()):
            object = Database_Class()
            if(self.ui.report_search_list.currentItem()):
                clientId =self.ui.report_search_list.currentItem().text(4) # CAN BE SELECTED FROM clients ARRAY

                total = float(self.ui.pay_client_balance.text())

                if (self.ui.pay_total_charge.text()):
                    total += float(self.ui.pay_total_charge.text())
            
                received = self.ui.pay_services_amt_recieved.text()

                newbalance = float(total) - float(received)

                iterator = QtWidgets.QTreeWidgetItemIterator(self.ui.pay_list_widget)

                object.SetClientAccountBalance(int(clientId),float(newbalance)) #!!!!!!!!!!!!!
                ReportFunctions.DisplayDetail(self)
                self.ui.pay_services_amt_recieved.clear()
                self.ui.pay_total_balance.clear()
                self.ui.pay_total_charge.clear()

                if (iterator.value()): # Receipt
                    name =self.ui.report_search_list.currentItem().text(0)
                    canvas = Canvas(name+" receipt.pdf")
                    canvas.drawString(100, 500, "Name")
                    canvas.drawString(200, 500, name)
                    
                    line_height_counter=0
                    counter=1
                    total=0
                    canvas.drawString(100, 470, "Service Costs")
                    while iterator.value():
                        item = iterator.value()
                        canvas.drawString(100, 455-line_height_counter, "Service-"+str(counter))
                        canvas.drawString(200, 455-line_height_counter, item.text(1))
                        line_height_counter += 15
                        iterator += 1
                        counter+=1
                        total+=round(float(item.text(2)),2)

                    canvas.drawString(100, 440-line_height_counter, "Total Cost")
                    canvas.drawString(200, 440-line_height_counter, str(total))

                    canvas.drawString(100, 410-line_height_counter, "Amount Paid")
                    canvas.drawString(100, 395-line_height_counter, "Updated Balance")   

                    canvas.drawString(200, 410-line_height_counter, "{:.2f}".format(float(received)))
                    canvas.drawString(200, 395-line_height_counter, "{:.2f}".format(newbalance))
                    canvas.save()
            
                self.ui.pay_list_widget.clear()
                TotalCharges = 0

            else:
                MainWindow.show_popup(self,"Missing Client!","Please search and choose a client")
            
        else:
            MainWindow.show_popup(self,"Missing Arguments!","Please enter amount of received")
        
    def DecreaseAccountBalance(self):
        object = Database_Class()
        
        if(self.ui.pay_remaining_amt_recieved.text()):
            if(self.ui.report_search_list.currentItem()):
                received = self.ui.pay_remaining_amt_recieved.text()
                clientId =self.ui.report_search_list.currentItem().text(4)
                print(clientId)
                object.DecreaseAccountBalance(int(clientId),float(received))
                ReportFunctions.DisplayDetail(self)
                self.ui.pay_remaining_amt_recieved.clear()
            else:
                MainWindow.show_popup(self,"Missing Client!","Please search and choose a client or pet")
        else:
            MainWindow.show_popup(self,"Missing Arguments!","Please enter amount of received")
       # object = Database_Class()
       # object.SubmitPayment(row)
        
    def clearServicesList(self):
        global TotalCharges
        object = Database_Class()

        root = self.ui.pay_list_widget.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count-1,-1,-1):
            item = root.child(i)
            if (item):
                sub = item.text(1)
                serviceID = item.text(2)
                Client_ID = current_client
                object.removeServicesDetails(serviceID=serviceID,Client_ID=Client_ID,subTotal=sub)

                # remove the row
                self.ui.pay_list_widget.takeTopLevelItem(i)

                # subtract sub_total from total charges.
                TotalCharges -= float(sub)
                TotalCharges = round(TotalCharges,2)

                # calculate total balance again.
                balance =self.ui.pay_client_balance.text()
                totalBalance = TotalCharges + float(balance)
                totalBalance = round(totalBalance,2)

                self.ui.pay_total_balance.setText("{:.2f}".format(totalBalance))
                self.ui.pay_total_charge.setText("{:.2f}".format(TotalCharges))
                #self.ui.pay_total_balance.clear()
            else:
                break

"""