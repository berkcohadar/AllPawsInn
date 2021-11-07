

from Admin_Functions import *
day_swicher = 0
class HomeFunctions(MainWindow):

    def ReservedToday(self):
        object=Database_Class()
        info = object.GetReservations(self,)




    def DisplayReservations(self,today,tommorrow):
        object = Database_Class()

        result = object.GetReservations(today,tommorrow)


        self.ui.home_reserved_tree.clear()
        for obj in result:
            animalID = str(obj[3])
            animalName = obj[2]
            bookingID = str(obj[5])
            status = obj[4]
            date = str(obj[6])
            ownerName = obj[0] + " " + obj[1]
            item = QtWidgets.QTreeWidgetItem(self.ui.home_reserved_tree,[ ownerName,animalName,animalID,bookingID ])
            self.ui.home_reserved_tree.addTopLevelItem(item)



    def DisplayCheckedIn(self,today,tommorrow):
        object = Database_Class()

        result = object.GetCheckedIn(today,tommorrow)


        self.ui.home_checked_in_tree.clear()
        for obj in result:
            animalID = str(obj[3])
            animalName = obj[2]
            bookingID = str(obj[5])
            status = obj[4]
            date = str(obj[6])
            ownerName = obj[0] + " " + obj[1]
            ownerID= str(obj[7])
            item = QtWidgets.QTreeWidgetItem(self.ui.home_checked_in_tree,[ ownerName,animalName,animalID,bookingID,ownerID ])
            self.ui.home_checked_in_tree.addTopLevelItem(item)
           # QTreeWidgetItem *items = new QTreeWidgetItem(self.ui.treeWidget)
           # items.setText(0, tr("Owner Name"))
           # self.ui.treeWidget.addTopLevelItem( QtWidgets.QTreeWidgetItem([ownerName , animalName,status,date,animalID ] ) )

    def DisplayCheckedOut(self,today,tommorrow):
        object = Database_Class()

        result = object.GetCheckedOut(today,tommorrow)


        self.ui.home_checkout_tree.clear()
        for obj in result:
            animalID = str(obj[3])
            animalName = obj[2]
            bookingID = str(obj[5])
            status = obj[4]
            date = str(obj[6])
            ownerName = obj[0] + " " + obj[1]
            item = QtWidgets.QTreeWidgetItem(self.ui.home_checkout_tree,[ ownerName,animalName,animalID ])
            self.ui.home_checkout_tree.addTopLevelItem(item)
           # QTreeWidgetItem *items = new QTreeWidgetItem(self.ui.treeWidget)
           # items.setText(0, tr("Owner Name"))
           # self.ui.treeWidget.addTopLevelItem( QtWidgets.QTreeWidgetItem([ownerName , animalName,status,date,animalID ] ) )


    def CheckedIn(self):
        if(self.ui.home_reserved_tree.currentItem()):
            print(QtCore.QDate.currentDate().toString("M/d/yyyy") )
            print(self.ui.home_date.text())
            if(QtCore.QDate.currentDate().toString("M/d/yyyy") ==  self.ui.home_date.text()):
                object = Database_Class()
                animalName = self.ui.home_reserved_tree.currentItem().text(1)
                animalId = self.ui.home_reserved_tree.currentItem().text(2)
                bookingId =self.ui.home_reserved_tree.currentItem().text(3)
                print(bookingId)
                object.SetBookingStatusbyBookingID(bookingId,'CheckedIn')
            else:
                MainWindow.show_popup(self,"Invalid Operation!","Please go to current day to check-in")
        else:
             MainWindow.show_popup(self,"Invalid Operation!","Please choose client to check-in")
    def CheckedOut(self):
        if(QtCore.QDate.currentDate().toString("M/d/yyyy") ==  self.ui.home_date.text()):
            object = Database_Class()
            animalName = self.ui.home_checked_in_tree.currentItem().text(1)
            animalId = self.ui.home_checked_in_tree.currentItem().text(2)
            bookingId =self.ui.home_checked_in_tree.currentItem().text(3)

        print(bookingId)
        object.SetBookingStatusbyBookingID(bookingId,'CheckedOut')
    def CheckedOutWithoutPayment(self):

        if(self.ui.home_checked_in_tree.currentItem()):
            HomeFunctions.CheckoutWithPaymentServices(self)
            object = Database_Class()

            animalName = self.ui.home_checked_in_tree.currentItem().text(1)
            animalId = self.ui.home_checked_in_tree.currentItem().text(2)
            bookingId =self.ui.home_checked_in_tree.currentItem().text(3)
            clientId =self.ui.home_checked_in_tree.currentItem().text(4)
            animalInfo = object.GetAnimalInfo(int(animalId))

            for item in animalInfo:
                animalName= item[0]
                animalSize = item[1]
                animalBreed = item[2]

            self.ui.pay_animal_name_3.setText(animalName)
            self.ui.pay_animal_size_3.setText(animalSize)
            self.ui.pay_animal_breed_3.setText(animalBreed)

            clientInfo = object.GetClientInfo(int(clientId))

            for client in clientInfo:
                clientName= client[0] + " "+ client[1]
                clientAddress= client[2]
                clientCell= client[3]
                clientNotes= client[4]
                clientBalance= client[5]
            self.ui.pay_client_name_3.setText(clientName)
            self.ui.pay_client_address_3.setText(clientAddress)
            self.ui.pay_client_cellphone_3.setText(clientCell)
            self.ui.pay_client_notes_3.setText(clientNotes)
            self.ui.pay_client_balance_3.setText(str(clientBalance))

            servicesinfo= object.GetDayCareRateAndTax(4)

            for  service in servicesinfo:
                daycarerate = service[0]

                tax = service[1]


            self.ui.mpayment_daycare_rate_2.setText(str(daycarerate))

            self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page)
            #self.ui.pay_nys_tax.setText(str(tax))
        else:
            MainWindow.show_popup(self,"Invalid Operation!","Please choose client to check-out")


    def CheckoutWithoutPaymentServices(self):

        object = Database_Class()
        clientId =self.ui.home_checked_in_tree.currentItem().text(4)
        othergoods = self.ui.mpayment_other_goods_2.text()
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

        for  service in servicesinfo:
            daycarerate = service[0]
            tax = service[1]

        servicesSubTotal = 0
        if self.ui.mpayment_food_2.isChecked() :


            servicesSubTotal += foodFee

        # returns false / true
        if self.ui.mpayment_hair_2.isChecked():

            servicesSubTotal += hairFee
        if self.ui.mpayment_nails_2.isChecked():

            servicesSubTotal += nailFee

        floatTotal= float(servicesSubTotal)
        floatTotal+= float(daycarerate) + float(othergoods) #- float(discount)

        totalCharges =   floatTotal * tax/100 + floatTotal


        #self.ui.pay_subtotal.setText(str(totalCharges))

        object.IncreaseClientBalance(int(clientId),totalCharges)
        bookingId =self.ui.home_checked_in_tree.currentItem().text(3)

        print(bookingId)
        object.SetBookingStatusbyBookingID(bookingId,'CheckedOut')
        HomeFunctions.UpdateDisplay(self)

    def CheckedOutWithPayment(self):
        print(self.ui.home_date.text())
        print(QtCore.QDate.currentDate().toString("M/d/yyyy"))
        if(self.ui.home_checked_in_tree.currentItem() ):

            if(QtCore.QDate.currentDate().toString("M/d/yyyy") ==  self.ui.home_date.text()):
                #change this line <= current day or before

                object = Database_Class()

                animalName = self.ui.home_checked_in_tree.currentItem().text(1)
                animalId = self.ui.home_checked_in_tree.currentItem().text(2)
                bookingId =self.ui.home_checked_in_tree.currentItem().text(3)
                clientId =self.ui.home_checked_in_tree.currentItem().text(4)
                animalInfo = object.GetAnimalInfo(int(animalId))

                for item in animalInfo:
                    animalName= item[0]
                    animalSize = item[1]
                    animalBreed = item[2]

                self.ui.pay_animal_name_2.setText(animalName)
                self.ui.pay_animal_size_2.setText(animalSize)
                self.ui.pay_animal_breed_2.setText(animalBreed)

                clientInfo = object.GetClientInfo(int(clientId))

                for client in clientInfo:
                    clientName= client[0] + " "+ client[1]
                    clientAddress= client[2]
                    clientCell= client[3]
                    clientNotes= client[4]
                    clientBalance= client[5]
                self.ui.pay_client_name_2.setText(clientName)
                self.ui.pay_client_address_2.setText(clientAddress)
                self.ui.pay_client_cellphone_2.setText(clientCell)
                self.ui.pay_client_notes_2.setText(clientNotes)
                self.ui.pay_client_balance_2.setText(str(clientBalance))

                servicesinfo= object.GetDayCareRateAndTax(4)

                for  service in servicesinfo:
                    daycarerate = service[0]

                    tax = service[1]


                self.ui.mpayment_daycare_rate.setText(str(daycarerate))
                self.ui.mpayment_ny_tax.setText(str(tax))
                HomeFunctions.CheckoutWithPaymentServices(self)
                self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.mpayment_page)
                #self.ui.pay_nys_tax.setText(str(tax))
            else:
                MainWindow.show_popup(self,"Invalid Operation!","Please go to current day to check-in")
        else:
            MainWindow.show_popup(self,"Invalid Operation!","Please choose client to check-out")
    def CheckoutWithPaymentServices(self):
        object = Database_Class()
        clientId =self.ui.home_checked_in_tree.currentItem().text(4)
        othergoods = self.ui.mpayment_other_goods.text()
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
        discount = self.ui.mpayment_discount.text()
        if discount == '':
            discount= '0'
        print("discount"+discount)
        for  service in servicesinfo:
            daycarerate = service[0]
            tax = service[1]

        servicesSubTotal = 0
        if self.ui.mpayment_food.isChecked() :


            servicesSubTotal += foodFee

        # returns false / true
        if self.ui.mpayment_hair.isChecked():

            servicesSubTotal += hairFee
        if self.ui.mpayment_nails.isChecked():

            servicesSubTotal += nailFee

        floatTotal= float(servicesSubTotal)
        floatTotal+= float(daycarerate) + float(othergoods) - float(discount)

        totalCharges =   floatTotal * tax/100 + floatTotal
        x = Decimal(totalCharges)
        output = round(x,2)
        print(output)

        self.ui.mpayment_subtotal.setText(str(output))
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

            amtReceive =  self.ui.mpayment_amt_recieved.text()
            object = Database_Class()
            bookingId =self.ui.home_checked_in_tree.currentItem().text(3)
            clientId =self.ui.home_checked_in_tree.currentItem().text(4)

            totalBalance = self.ui.mpayment_total_bal.text()
            #paymentType = self.ui.comboBox_3.currentText()
            #print(paymentType)
            newbalance = float(totalBalance)- float(amtReceive)
            object.ChangeAccountBalance(clientId,newbalance)
            object.SetBookingStatusbyBookingID(bookingId,'CheckedOut')
            HomeFunctions.UpdateDisplay(self)
            self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home)
        else:
            MainWindow.show_popup(self,"Missing Arguments!","Please enter amount received")

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
    # def ChangeColor(self):
    #     print(self.ui.Content_stacked_Widget.currentWidget().)
    #     qss = """
    #     QPushButton {
    #     background-image: url(:/16x16/icons/16x16/cil-house.png);
    #     background-position: left center;
    #     background-repeat: no-repeat;
    #     border: none;
    #     border-left: 28px solid rgb(85, 170, 255);

    #     background-color: rgb(85, 170, 255);
    #     text-align: left;
    #     padding-left: 45px;
    #     }
    #     QPushButton:hover {
    #         background-color: rgb(33, 37, 43);
    #         border-left: 28px solid rgb(33, 37, 43);
    #     }
    #     QPushButton:pressed {
    #         background-color: rgb(85, 170, 255);
    #         border-left: 28px solid rgb(85, 170, 255);
    #     }
    #     """
    #     self.ui.menu_btn_daily.setStyleSheet(qss)
