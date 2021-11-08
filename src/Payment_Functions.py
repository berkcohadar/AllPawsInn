TotalCharges=0
clients=[]
from Home_Functions import *
from reportlab.pdfgen.canvas import Canvas

class PaymentFunctions(MainWindow):

    def clearPayments(self):
        self.ui.pay_search_list.clear()

    def updatePaymentDisplay(self):  
        self.ui.pay_search_list.clear()
        for obj in self.paws:  
            animalID = str(obj[3]) 
            clientID = str(obj[4]) 
            animalName = obj[2] 
            ownerName = obj[0] + " " + obj[1]
            self.ui.pay_search_list.addTopLevelItem( QtWidgets.QTreeWidgetItem([ownerName , animalName,animalID,clientID] ) )

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

    def DisplayDetail(self):
      
        object = Database_Class()
      
        animalId= self.ui.pay_search_list.currentItem().text(2)
    
        clientId = self.ui.pay_search_list.currentItem().text(3)
      
  
        animalInfo = object.GetAnimalInfo(int(animalId))
       
        #animalInfo[0]
        for item in animalInfo:
            animalName= item[0]
            animalSize = item[1]
            animalBreed = item[2]
            
        self.ui.pay_animal_name.setText(animalName)  
        self.ui.pay_animal_size.setText(animalSize)
        self.ui.pay_animal_breed.setText(animalBreed)
        clientInfo = object.GetClientInfo(int(clientId))
        for client in clientInfo:
            clientName= client[0] + " "+ client[1]
            clientAddress= client[2]
            clientCell= client[3]
            clientNotes= client[4]
            clientBalance= client[5]
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
        print("othergoods"+othergoods)


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
        print("discount"+discount)
        for  service in servicesinfo:
            daycarerate = service[0]
            tax = service[1]

        servicesSubTotal = 0
        if self.ui.pay_services_food.isChecked() :
            
            
            servicesSubTotal += foodFee
        
        # returns false / true 
        if self.ui.pay_services_hair.isChecked():
            
            servicesSubTotal += hairFee
        if self.ui.pay_services_nails.isChecked():
            
            servicesSubTotal += nailFee

        floatTotal= float(servicesSubTotal)
        floatTotal+= float(daycarerate) + float(othergoods) - float(discount)

        totalCharges =   format((floatTotal * tax/100 + floatTotal),'.2f' )
        
        x = Decimal(totalCharges)
        output = round(x,2)
        print(output)
        self.ui.pay_subtotal.setText("{:.2f}".format(output))

    def AddToList(self):
        global clients
        global TotalCharges     
        if(self.ui.pay_search_list.currentItem()):
            clientId =self.ui.pay_search_list.currentItem().text(3)
            if(clients !=[]):
                for id in clients:
                    if(clientId == id):
                        sub =  self.ui.pay_subtotal.text()

                        object = Database_Class()

                        animalId= self.ui.pay_search_list.currentItem().text(2)
                        clients.append(clientId)
                        animalInfo = object.GetAnimalInfo(int(animalId))
                        for item in animalInfo:
                            animalName= item[0]


                        self.ui.pay_list_widget.addTopLevelItem(QtWidgets.QTreeWidgetItem([ animalName, str(sub)] ))
                        # sub : animal name subtotal 
                        
                        TotalCharges += float(sub)
                        TotalCharges = round(TotalCharges,2)
                        
                        #TotalCharges += float(self.ui.pay_list_widget.topLevelItem(i))
                        balance =self.ui.pay_client_balance.text()
                        totalBalance = TotalCharges + float(balance)
                        totalBalance = round(totalBalance,2)

                        self.ui.pay_total_balance.setText("{:.2f}".format(totalBalance))
                        self.ui.pay_total_charge.setText("{:.2f}".format(TotalCharges))
                        break
                    else:
                        MainWindow.show_popup(self,"Wrong Client!","Client are not same.")
            else:
                sub =  self.ui.pay_subtotal.text()

                object = Database_Class()

                animalId= self.ui.pay_search_list.currentItem().text(2)
                clients.append(clientId)
                animalInfo = object.GetAnimalInfo(int(animalId))
                for item in animalInfo:
                    animalName= item[0]


                self.ui.pay_list_widget.addTopLevelItem(QtWidgets.QTreeWidgetItem([ animalName,str(sub)] ))
                # sub : animal name subtotal 
                
                
                TotalCharges += float(sub)
                TotalCharges = round(TotalCharges,2)
                
                    #TotalCharges += float(self.ui.pay_list_widget.topLevelItem(i))
                balance =self.ui.pay_client_balance.text()
                totalBalance = TotalCharges + float(balance)
                totalBalance = round(totalBalance,2)

                self.ui.pay_total_balance.setText("{:.2f}".format(totalBalance))
                self.ui.pay_total_charge.setText("{:.2f}".format(TotalCharges))
        else:
            MainWindow.show_popup(self,"Missing Client!","Please search and choose a pet")

    def removeFromList(self):
        # ADD =>
        # ` self.ui.BUTTON_NAME.clicked.connect(lambda: PaymentFunctions.removeFromList(self)) `
        # to main.py
        global clients
        global TotalCharges 
        if(self.ui.pay_search_list.currentItem()):
            if (self.ui.pay_list_widget.currentItem()):
                sub = self.ui.pay_list_widget.currentItem().text(1) # this is the subtotal that will be reducted from total charge.

                # find item and remove it from list.
                index = self.ui.pay_list_widget.indexOfTopLevelItem(self.ui.pay_list_widget.currentItem()) # this is the index of desired row.
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

    def SubmitPayments(self):
        global TotalCharges
        global clients
        if(self.ui.pay_services_amt_recieved):
            object = Database_Class()
            received = 0
            if(self.ui.pay_services_amt_recieved.text()):
                received=self.ui.pay_services_amt_recieved.text()
            newbalance=0
            if(self.ui.pay_search_list.currentItem()):
                if(self.ui.pay_list_widget.currentItem()):
                    clientId =self.ui.pay_search_list.currentItem().text(3)
                    total =self.ui.pay_total_balance.text()
                    newbalance = float(total) - float(received)
                    print(clientId)
                    object.SetClientAccountBalance(int(clientId),float(newbalance)) #!!!!!!!!!!!!!
                    PaymentFunctions.DisplayDetail(self)
                    self.ui.pay_services_amt_recieved.clear()
                    self.ui.pay_total_balance.clear()
                    self.ui.pay_total_charge.clear()
                    
                    ######
                    name =self.ui.pay_search_list.currentItem().text(0)
                    canvas = Canvas(name+" receipt.pdf")
                    canvas.drawString(100, 500, "Name")
                    canvas.drawString(200, 500, name)
                    
                    line_height_counter=0
                    counter=1
                    total=0
                    canvas.drawString(100, 470, "Service Costs")
                    iterator = QtWidgets.QTreeWidgetItemIterator(self.ui.pay_list_widget)
                    while iterator.value():
                        item = iterator.value()
                        canvas.drawString(100, 455-line_height_counter, "Service-"+str(counter))
                        canvas.drawString(200, 455-line_height_counter, item.text(1))
                        line_height_counter += 15
                        iterator += 1
                        counter+=1
                        total+=round(float(item.text(1)),2)

                    canvas.drawString(100, 440-line_height_counter, "Total Cost")
                    canvas.drawString(200, 440-line_height_counter, str(total))

                    canvas.drawString(100, 410-line_height_counter, "Amount Paid")
                    canvas.drawString(100, 395-line_height_counter, "Updated Balance")   

                    canvas.drawString(200, 410-line_height_counter, "{:.2f}".format(float(received)))
                    canvas.drawString(200, 395-line_height_counter, "{:.2f}".format(newbalance))
                    canvas.save()
                    
                    self.ui.pay_list_widget.clear()
                    
                    TotalCharges = 0 
                    clients=[]
                    self.ui.pay_search_list.clear()
                else:
                    MainWindow.show_popup(self,"Missing service!","Please add a service first.")
            else:
                MainWindow.show_popup(self,"Missing Client!","Please search and choose a client")
            
        else:

            MainWindow.show_popup(self,"Missing Arguments!","Please enter amount of received")
        
        #print(row)
    
    def DecreaseAccountBalance(self):
        object = Database_Class()
        
        if(self.ui.pay_remaining_amt_recieved.text()):
            if(self.ui.pay_search_list.currentItem()):
                received = self.ui.pay_remaining_amt_recieved.text()
                clientId =self.ui.pay_search_list.currentItem().text(3)
                print(clientId)
                object.DecreaseAccountBalance(int(clientId),float(received))
                PaymentFunctions.DisplayDetail(self)
                self.ui.pay_remaining_amt_recieved.clear()
            else:
                MainWindow.show_popup(self,"Missing Client!","Please search and choose a client or pet")
        else:
            MainWindow.show_popup(self,"Missing Arguments!","Please enter amount of received")
       # object = Database_Class()
       # object.SubmitPayment(row)
        