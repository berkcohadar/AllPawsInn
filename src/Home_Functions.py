

from Admin_Functions import *
from datetime import datetime

day_swicher = 0
class HomeFunctions(MainWindow):

    def ReservedToday(self):
        object=Database_Class()
        info = object.GetReservations(self,)

    def DisplayReservations(self,today,tommorrow):
        self.ui.home_reserved_tree.clear()

        object = Database_Class()
        result = object.GetReservations(today, 0, 0)
        for obj in result:
            customerName = obj[0] + " " + obj[1]
            animalName = obj[2]
            animalID = str(obj[3])
            serviceID = str(obj[4])
            customerID = str(obj[5])
        
            item = QtWidgets.QTreeWidgetItem(self.ui.home_reserved_tree,[customerName , animalName, animalID, serviceID, customerID ])
            self.ui.home_reserved_tree.addTopLevelItem(item)

    def DisplayCheckedIn(self,today,tommorrow):
        self.ui.home_checked_in_tree.clear()

        object = Database_Class()
        result = object.GetReservations(today, 1, 0)
        for obj in result:
            customerName = obj[0] + " " + obj[1]
            animalName = obj[2]
            animalID = str(obj[3])
            serviceID = str(obj[4])
            customerID = str(obj[5])
            
            item = QtWidgets.QTreeWidgetItem(self.ui.home_checked_in_tree,[customerName , animalName, animalID, serviceID, customerID ])
            self.ui.home_checked_in_tree.addTopLevelItem(item)

    def DisplayCheckedOut(self,today,tommorrow):
        self.ui.home_checkout_tree.clear()

        object = Database_Class()
        result = object.GetReservations(today, 1, 1)
        for obj in result:
            customerName = obj[0] + " " + obj[1]
            animalName = obj[2]
            animalID = str(obj[3])
            serviceID = str(obj[4])
            customerID = str(obj[5])
            
            item = QtWidgets.QTreeWidgetItem(self.ui.home_checkout_tree,[customerName , animalName, animalID, serviceID, customerID ])
            self.ui.home_checkout_tree.addTopLevelItem(item)

    def CheckedIn(self):
        if(self.ui.home_reserved_tree.currentItem()):
            if(QtCore.QDate.currentDate().toString("M/d/yyyy") ==  self.ui.home_date.text()):
                object = Database_Class()
                bookingId = self.ui.home_reserved_tree.currentItem().text(3)
                opDate = {"DateIn":QtCore.QDate.currentDate()}
                object.SetBookingStatusbyBookingID(bookingId, opDate)
            else:
                MainWindow.show_popup(self,"Invalid Operation!","Please go to current day to check-in")
        else:
             MainWindow.show_popup(self,"Invalid Operation!","Please choose client to check-in")
    
    def CheckedOut(self):
        if(self.ui.home_checked_in_tree.currentItem()):
            if(QtCore.QDate.currentDate().toString("M/d/yyyy") ==  self.ui.home_date.text()):
                object = Database_Class()
                bookingId = self.ui.home_checked_in_tree.currentItem().text(3)

                result = object.getSingleServicesDetails(bookingId)[0]
                resEnd = result['resEndDate'].strftime("%Y-%m-%d")
                today = datetime.now().strftime("%Y-%m-%d")

                if (resEnd > today):
                    returnValue = MainWindow.show_popup_button(self,"Are you sure?", "The reservation end date for the customer is not today. Do you want to check-out anyway?")
                    if returnValue == QMessageBox.Ok:
                        opDate = {"DateOut":QtCore.QDate.currentDate()}
                        object.SetBookingStatusbyBookingID(bookingId, opDate)
                else:
                    opDate = {"DateOut":QtCore.QDate.currentDate()}
                    object.SetBookingStatusbyBookingID(bookingId, opDate)
            else:
                MainWindow.show_popup(self,"Invalid Operation!","Please go to current day to check-out")
        else:
             MainWindow.show_popup(self,"Invalid Operation!","Please choose client to check-out")

    def ForceCheckOut(self):
        print("calisti")
        if(self.ui.home_checked_in_tree.currentItem()):
            if(QtCore.QDate.currentDate().toString("M/d/yyyy") ==  self.ui.home_date.text()):
                object = Database_Class()
                bookingId = self.ui.home_checked_in_tree.currentItem().text(3)

                result = object.getSingleServicesDetails(bookingId)[0]
                resEnd = result['resEndDate'].strftime("%Y-%m-%d")
                today = datetime.now().strftime("%Y-%m-%d")

                opDate = {"DateOut":QtCore.QDate.currentDate()}
                object.SetBookingStatusbyBookingID(bookingId, opDate)
            else:
                MainWindow.show_popup(self,"Invalid Operation!","Please go to current day to check-out")
        else:
             MainWindow.show_popup(self,"Invalid Operation!","Please choose client to check-out")
    
    def CheckoutWithPaymentServices(self):
        object = Database_Class()
        clientId = self.ui.home_checkout_tree.currentItem().text(4)

        othergoods = self.ui.mpayment_other_goods.text()
        if (othergoods == ''):
            othergoods = '0'

        discount = self.ui.mpayment_discount.text()
        if discount == '':
            discount= '0'

        foodFeeArray = object.GetServicesFees('food')
        print(foodFeeArray)
        for item in foodFeeArray:
            foodFee = item[0]

        hairFeeArray = object.GetServicesFees('hair')
        for item2 in hairFeeArray:
            hairFee = item2[0]

        nailFeeArray = object.GetServicesFees('nails')
        for item3 in nailFeeArray:
            nailFee = item3[0]

        servicesinfo= object.GetDayCareRateAndTax(4)
        for service in servicesinfo:
            daycarerate = service[0]
            tax = service[1]

        servicesSubTotal = 0
        if self.ui.mpayment_food.isChecked() :
            servicesSubTotal += float(foodFee)

        if self.ui.mpayment_hair.isChecked():
            servicesSubTotal += float(hairFee)

        if self.ui.mpayment_nails.isChecked():
            servicesSubTotal += float(nailFee)
        
        totalDayCare = 0
        if self.ui.mpayment_daycare_checkbox.isChecked():
            daysIn = int(self.ui.mpayment_daysIn.text())
            totalDayCare = daysIn*daycarerate
            servicesSubTotal += totalDayCare
        self.ui.mpayment_daycare_total.setText(str(totalDayCare))
            
        floatTotal= float(servicesSubTotal) + float(othergoods) - float(discount)

        totalCharges =   floatTotal * tax/100 + floatTotal
        x = Decimal(totalCharges)
        output = round(x,2)

        self.ui.mpayment_subtotal.setText(str(output))
        self.ui.mpayment_ny_tax.setText(str(floatTotal * tax/100)) # "$"+
        self.ui.mpayment_total_charge.setText(str(output))
        Balance = object.GetClientAccountBalance(clientId)
        for balance in Balance:
            AccountBalance= balance

        AC = Decimal(AccountBalance)
        ACC = round(AC,2)
        TotalBalance = ACC + output
        self.ui.mpayment_prev_bal.setText(str(ACC))
        self.ui.mpayment_total_bal.setText(str(TotalBalance))
    
    def CheckOutWithPaymentMakePayment(self):

        if(self.ui.mpayment_amt_recieved.text()):
            paymentAmount =  float(self.ui.mpayment_amt_recieved.text())
            bookingId = int(self.ui.home_checkout_tree.currentItem().text(3))
            customerId = int(self.ui.home_checkout_tree.currentItem().text(4))
            paymentDate = QtCore.QDate.currentDate().toString("yyyy-MM-dd")
            paymentType = self.ui.comboBox_3.currentText()

            object = Database_Class()

            dayCareRate = float(self.ui.mpayment_daycare_total.text())

            foodFee = 0.0
            hairFee = 0.0
            nailFee = 0.0
            
            if self.ui.mpayment_food.isChecked() :
                foodFeeArray = object.GetServicesFees('food')
                for item in foodFeeArray:
                    foodFee = float(item[0])

            if self.ui.mpayment_hair.isChecked():
                hairFeeArray = object.GetServicesFees('hair')
                for item in hairFeeArray:
                    hairFee = float(item[0])

            if self.ui.mpayment_nails.isChecked():
                nailFeeArray = object.GetServicesFees('nails')
                for item in nailFeeArray:
                    nailFee = float(item[0])

            othergoods = float(self.ui.mpayment_other_goods.text())
            if (othergoods == ''):
                othergoods = 0.0

            discount = float(self.ui.mpayment_discount.text())
            if discount == '':
                discount= 0.0

            totalTax = float(self.ui.mpayment_ny_tax.text())
            subTotal = float(self.ui.mpayment_subtotal.text())

            completed = 1

            object.updateServicesDetails(customerId, bookingId, dayCareRate, nailFee, foodFee, hairFee, othergoods, discount, totalTax, subTotal, completed)
            object.createPayment(customerId, paymentAmount, paymentDate, paymentType, bookingId)
            HomeFunctions.UpdateDisplay(self)
            self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home)
        else:
            MainWindow.show_popup(self,"Missing Arguments!","Please enter amount received")

    def ComleteBooking(self):
        if(self.ui.home_checkout_tree.currentItem() ):
            object = Database_Class()

            animalName = self.ui.home_checkout_tree.currentItem().text(1)
            animalId = self.ui.home_checkout_tree.currentItem().text(2)
            bookingId = self.ui.home_checkout_tree.currentItem().text(3)
            clientId = self.ui.home_checkout_tree.currentItem().text(4)

            animalInfo = object.GetAnimalInfo(int(animalId))
            for item in animalInfo:
                animalName = item['AnimalName']
                animalSize = item['Size']
                animalBreed = item['Breed']
                
            self.ui.pay_animal_name_2.setText(animalName)
            self.ui.pay_animal_size_2.setText(animalSize)
            self.ui.pay_animal_breed_2.setText(animalBreed)

            serviceDetails = object.getSingleServicesDetails(bookingId)[0]

            self.ui.pay_animal_date_in_2.setText(str(serviceDetails["dateIn"]))
            self.ui.pay_animal_date_out_2.setText(str(serviceDetails["dateOut"]))
            self.ui.pay_animal_day_2.setText(str(serviceDetails["daysIn"]))

            clientInfo = object.GetClientInfo(int(clientId))

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
                    clientBalance = 0.00
                    object.SetClientAccountBalance(int(clientId),float(0))

            self.ui.pay_client_name_2.setText(clientName)
            self.ui.pay_client_address_2.setText(clientAddress)
            self.ui.pay_client_cellphone_2.setText(clientCell)
            self.ui.pay_client_notes_2.setText(clientNotes)
            self.ui.pay_client_balance_2.setText(str(clientBalance))

            servicesinfo= object.GetDayCareRateAndTax(4)
            for  service in servicesinfo:
                daycarerate = service[0]
                tax = service[1]
            
            self.ui.mpayment_daycare_rate.setText(str(daycarerate)) # "$"+
            self.ui.mpayment_daysIn.setText(str(serviceDetails["daysIn"]))
            HomeFunctions.CheckoutWithPaymentServices(self)
            self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.mpayment_page)

        else:
            MainWindow.show_popup(self,"Invalid Operation!","Please choose client to make payment")

    def NextDay(self):
        global day_swicher
        day_swicher= day_swicher+1
        day = QtCore.QDate.currentDate().addDays(day_swicher)
        day1 = QtCore.QDate.currentDate().addDays(day_swicher).toString("yyyy-MM-dd")

        day2 = QtCore.QDate.currentDate().addDays(day_swicher+1).toString("yyyy-MM-dd")
        print( "Next bastik" +day1 +""+day2)
        self.ui.home_date.setDate(day)
        HomeFunctions.DisplayReservations(self,day1,day2)
        HomeFunctions.DisplayCheckedIn(self,day1,day2)
        HomeFunctions.DisplayCheckedOut(self,day1,day2)

    def UpdateDisplay(self):
        global day_swicher
        day = QtCore.QDate.currentDate().addDays(day_swicher)
        day1 = QtCore.QDate.currentDate().addDays(day_swicher).toString("yyyy-MM-dd")
        day2 = QtCore.QDate.currentDate().addDays(day_swicher+1).toString("yyyy-MM-dd")

        HomeFunctions.DisplayReservations(self,day1,day2)
        HomeFunctions.DisplayCheckedIn(self,day1,day2)
        HomeFunctions.DisplayCheckedOut(self,day1,day2)

    def PreviosDay(self):

        global day_swicher
        day_swicher= day_swicher-1
        day = QtCore.QDate.currentDate().addDays(day_swicher)
        day1 = QtCore.QDate.currentDate().addDays(day_swicher+1).toString("yyyy-MM-dd")

        day2 = QtCore.QDate.currentDate().addDays(day_swicher).toString("yyyy-MM-dd")
        print( "Prev bastik" +day1 +""+day2)
        self.ui.home_date.setDate(day)
        HomeFunctions.DisplayReservations(self,day2,day1)
        HomeFunctions.DisplayCheckedIn(self,day2,day1)
        HomeFunctions.DisplayCheckedOut(self,day2,day1)

    def ShowToday(self):
        global day_swicher
        day = QtCore.QDate.currentDate()
        day1 = QtCore.QDate.currentDate().toString("yyyy-MM-dd")
        day2 = QtCore.QDate.currentDate().addDays(1).toString("yyyy-MM-dd")
        print("today", day)
        print( "Show Today" +day1 +""+day2)
        self.ui.home_date.setDate(day)
        HomeFunctions.DisplayReservations(self,day1,day2)
        HomeFunctions.DisplayCheckedIn(self,day1,day2)
        HomeFunctions.DisplayCheckedOut(self,day1,day2)
        day_swicher = 0





   # def CheckedOutWithoutPayment(self):
    #     # self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.mpayment_page)
    #     if(self.ui.home_checkout_tree.currentItem()):
    #         HomeFunctions.CheckoutWithPaymentServices(self)
    #         object = Database_Class()

    #         animalName = self.ui.home_checkout_tree.currentItem().text(1)
    #         animalId = self.ui.home_checkout_tree.currentItem().text(2)
    #         bookingId =self.ui.home_checkout_tree.currentItem().text(3)
    #         clientId =self.ui.home_checkout_tree.currentItem().text(4)
    #         animalInfo = object.GetAnimalInfo(int(animalId),status="CheckedIn")

    #         for item in animalInfo:
    #             animalName = item['AnimalName']
    #             animalSize = item['Size']
    #             animalBreed = item['Breed']
    #             animalDateIn = item['DateIn']
    #             animalDateOut = item['DateOut']
    #             animalDaysIn = item['NoDays']

    #         self.ui.pay_animal_name_3.setText(animalName)
    #         self.ui.pay_animal_size_3.setText(animalSize)
    #         self.ui.pay_animal_breed_3.setText(animalBreed)
    #         self.ui.pay_animal_date_in_3.setText(str(animalDateIn))
    #         self.ui.pay_animal_date_out_3.setText(str(animalDateOut))
    #         self.ui.pay_animal_day_3.setText(str(animalDaysIn))

    #         clientInfo = object.GetClientInfo(int(clientId))

    #         for client in clientInfo:
    #             clientName = client['FirstName'] + " " + client['LastName']
    #             clientTown =  client['Town'] +", " if client['Town'] else ""
    #             clientPostCode = client['PostcodeZIP'] if client['PostcodeZIP'] else ""
    #             clientAddress = client['Address1']  + "\n" + clientTown + clientPostCode
    #             clientCell = client['CellMobile']
    #             clientNotes = client['Email']
    #             if client['AccountBalance'] :
    #                 clientBalance = client['AccountBalance']
    #             else:
    #                 clientBalance = 0
    #                 object.SetClientAccountBalance(int(clientId),float(0))    
    #         self.ui.pay_client_name_3.setText(clientName)
    #         self.ui.pay_client_address_3.setText(clientAddress)
    #         self.ui.pay_client_cellphone_3.setText(clientCell)
    #         self.ui.pay_client_notes_3.setText(clientNotes)
    #         self.ui.pay_client_balance_3.setText(str(clientBalance))

    #         servicesinfo= object.GetDayCareRateAndTax(4)

    #         for  service in servicesinfo:
    #             daycarerate = service[0]
    #             tax = service[1]

    #         self.ui.mpayment_daycare_rate_2.setText(str(daycarerate))
    #         self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page) ######
    #     else:
    #         MainWindow.show_popup(self,"Invalid Operation!","Please choose client to check-out")

    # def CheckoutWithoutPaymentServices(self):
    #     object = Database_Class()
    #     clientId =self.ui.home_checkout_tree.currentItem().text(4)
    #     othergoods = self.ui.mpayment_other_goods_2.text()
    #     if (othergoods == ''):
    #         othergoods = '0'

    #     foodFeeArray = object.GetServicesFees('food')
    #     for item in foodFeeArray:
    #         foodFee = item[0]

    #     hairFeeArray = object.GetServicesFees('hair')
    #     for item2 in hairFeeArray:
    #         hairFee = item2[0]

    #     nailFeeArray = object.GetServicesFees('nails')
    #     for item3 in nailFeeArray:
    #         nailFee = item3[0]

    #     servicesinfo= object.GetDayCareRateAndTax(4)

    #     for  service in servicesinfo:
    #         daycarerate = service[0]
    #         tax = service[1]

    #     servicesSubTotal = 0
    #     if self.ui.mpayment_food_2.isChecked() :
    #         servicesSubTotal += foodFee

    #     if self.ui.mpayment_hair_2.isChecked():
    #         servicesSubTotal += hairFee

    #     if self.ui.mpayment_nails_2.isChecked():
    #         servicesSubTotal += nailFee

    #     floatTotal= float(servicesSubTotal)
    #     floatTotal+= float(daycarerate) + float(othergoods) #- float(discount)

    #     totalCharges =   floatTotal * tax/100 + floatTotal

    #     object.IncreaseClientBalance(int(clientId),totalCharges)
    #     bookingId =self.ui.home_checkout_tree.currentItem().text(3)

    #     print(bookingId)
    #     opDate = {"DateOut":QtCore.QDate.currentDate()}
    #     object.SetBookingStatusbyBookingID(bookingId, opDate,'CheckedOut')
    #     HomeFunctions.UpdateDisplay(self)

    # def CheckedOutWithPayment(self):
    #     print(self.ui.home_date.text())
    #     print(QtCore.QDate.currentDate().toString("M/d/yyyy"))
    #     if(self.ui.home_checked_in_tree.currentItem() ):

    #         if(QtCore.QDate.currentDate().toString("M/d/yyyy") ==  self.ui.home_date.text()):
    #             #change this line <= current day or before

    #             object = Database_Class()

    #             animalName = self.ui.home_checked_in_tree.currentItem().text(1)
    #             animalId = self.ui.home_checked_in_tree.currentItem().text(2)
    #             bookingId =self.ui.home_checked_in_tree.currentItem().text(3)
    #             clientId =self.ui.home_checked_in_tree.currentItem().text(4)
    #             animalInfo = object.GetAnimalInfo(int(animalId),status="CheckedIn")

    #             for item in animalInfo:
    #                 animalName = item['AnimalName']
    #                 animalSize = item['Size']
    #                 animalBreed = item['Breed']
    #                 animalDateIn = item['DateIn']
    #                 animalDateOut = item['DateOut']
    #                 animalDaysIn = item['NoDays']
                    
    #             self.ui.pay_animal_name_2.setText(animalName)
    #             self.ui.pay_animal_size_2.setText(animalSize)
    #             self.ui.pay_animal_breed_2.setText(animalBreed)
    #             self.ui.pay_animal_date_in_2.setText(str(animalDateIn))
    #             self.ui.pay_animal_date_out_2.setText(str(animalDateOut))
    #             self.ui.pay_animal_day_2.setText(str(animalDaysIn))


    #             clientInfo = object.GetClientInfo(int(clientId))

    #             for client in clientInfo:
    #                 clientName = client['FirstName'] + " " + client['LastName']
    #                 clientTown =  client['Town'] +", " if client['Town'] else ""
    #                 clientPostCode = client['PostcodeZIP'] if client['PostcodeZIP'] else ""
    #                 clientAddress = client['Address1']  + "\n" + clientTown + clientPostCode
    #                 clientCell = client['CellMobile']
    #                 clientNotes = client['Email']
    #                 if client['AccountBalance'] :
    #                     clientBalance = client['AccountBalance']
    #                 else:
    #                     clientBalance = 0
    #                     object.SetClientAccountBalance(int(clientId),float(0))
    #             self.ui.pay_client_name_2.setText(clientName)
    #             self.ui.pay_client_address_2.setText(clientAddress)
    #             self.ui.pay_client_cellphone_2.setText(clientCell)
    #             self.ui.pay_client_notes_2.setText(clientNotes)
    #             self.ui.pay_client_balance_2.setText(str(clientBalance))

    #             servicesinfo= object.GetDayCareRateAndTax(4)

    #             for  service in servicesinfo:
    #                 daycarerate = service[0]

    #                 tax = service[1]


    #             self.ui.mpayment_daycare_rate.setText(str(daycarerate))
    #             self.ui.mpayment_ny_tax.setText(str(tax))
    #             HomeFunctions.CheckoutWithPaymentServices(self)
    #             self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.mpayment_page)
    #             #self.ui.pay_nys_tax.setText(str(tax))
    #         else:
    #             MainWindow.show_popup(self,"Invalid Operation!","Please go to current day to check-in")
    #     else:
    #         MainWindow.show_popup(self,"Invalid Operation!","Please choose client to check-out")