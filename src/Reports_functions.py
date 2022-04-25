from reportlab.pdfgen.canvas import Canvas
from DatabaseClass import Database_Class
from Home_Functions import *
import time
import os

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
        self.ui.report_search_list.setHeaderHidden(False)
        self.ui.payment_history_table.setHeaderHidden(False)

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
        self.ui.payment_history_table.clear()

        for item in result:
            paymentDetails = 'Payment towards Balance'
            print(str(item["BookingID"]))
            print(str(item["BookingID"]) != "None")
            if (str(item["BookingID"]) != "None"):
                paymentDetails = 'Payment with Service'
            self.ui.payment_history_table.addTopLevelItem(QtWidgets.QTreeWidgetItem([  item["PaymentDate"].strftime("%m/%d/%Y"), paymentDetails, "{:.2f}".format(float(item["AmountReceived"])), item["PaymentType"], str(clientId), str(item["PaymentId"]), str(item["BookingID"])] ))

    def createReportsFolder(self):
        path = os.getcwd()  + '\docs'

        isExist = os.path.exists(path)
        if not isExist: # Check whether the specified path exists or not
            os.makedirs(path) # Create a new directory because it does not exist 

    def printReceipt(self):
        if (self.ui.payment_history_table.currentItem()):
            ReportFunctions.createReportsFolder(self)
            for item in self.ui.payment_history_table.selectedItems():
                if (item.text(6) != "None"):
                    serviceID = int(item.text(6))
                    customerID = int(self.ui.report_search_list.currentItem().text(4))
                    ReportFunctions.printReceiptWithService(self, customerID, serviceID)
                else:
                    paymentID = int(item.text(5))
                    customerID = int(self.ui.report_search_list.currentItem().text(4))
                    ReportFunctions.printReceiptWithoutService(self, customerID, paymentID)
                time.sleep(1)

        else:
            MainWindow.show_popup(self,"Invalid Operation!","Please select a customer & payment to take a receipt!")

    def printReceiptWithService(self,customerID, serviceID):
        object = Database_Class()
        customer = object.GetClientInfo(id=customerID)[0]
        service = object.getSingleServicesDetails(serviceID=serviceID)[0]
        animal = object.GetAnimalInfo(id=service['animalID'])[0]
        payment = object.GetPaymentsbyService(serviceID=serviceID)[0]

        # customer['Address1'] # customer['Town'] # customer['PostcodeZIP']
        # customer['CellMobile']  # customer['Email']
        # payment["PaymentType"]

        startingLineY = 700 
        line_height_counter = 24

        startingLineX = 100
        endingLineX = 250

        name = customer['FirstName'] + "_" + customer['LastName'] + "_"
        today = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        canvas = Canvas('./docs/'+name+today+".pdf")
        canvas.setFont('Helvetica', 12)

        name = customer['FirstName'] + " " + customer['LastName']
        canvas.drawString(startingLineX, startingLineY, "Customer")
        canvas.drawString(endingLineX, startingLineY, name)
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Pet Name")
        canvas.drawString(endingLineX, startingLineY, animal["AnimalName"])
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Balance")
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(endingLineX, startingLineY, "$"+"{:.2f}".format(customer['AccountBalance']))
        canvas.setFont('Helvetica', 12) 
        startingLineY -= line_height_counter

        startingLineY -= line_height_counter
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(startingLineX, startingLineY, "Reservation Details")
        canvas.setFont('Helvetica', 12)
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Reservation Dates")
        canvas.drawString(endingLineX, startingLineY, service['dateIn'].strftime("%m/%d/%Y") + " - " + service['dateIn'].strftime("%m/%d/%Y"))
        startingLineY -= line_height_counter

        if (int(service['dayCareRate']) > 0):
            canvas.drawString(startingLineX, startingLineY, "Day Care Fee")
            canvas.drawString(endingLineX, startingLineY, "+ $"+"{:.2f}".format(service['dayCareRate']))
            startingLineY -= line_height_counter

        if (int(service['nails']) > 0):
            canvas.drawString(startingLineX, startingLineY, "Nails Fee")
            canvas.drawString(endingLineX, startingLineY, "+ $"+"{:.2f}".format(service['nails']))
            startingLineY -= line_height_counter

        if (int(service['food']) > 0):
            canvas.drawString(startingLineX, startingLineY, "Food Fee")
            canvas.drawString(endingLineX, startingLineY, "+ $"+"{:.2f}".format(service['food']))
            startingLineY -= line_height_counter

        if (int(service['otherGoods']) > 0):
            canvas.drawString(startingLineX, startingLineY, "Other Goods")
            canvas.drawString(endingLineX, startingLineY, "+ $"+"{:.2f}".format(service['otherGoods']))
            startingLineY -= line_height_counter

        if (int(service['discount']) > 0):
            canvas.drawString(startingLineX, startingLineY, "Discount")
            canvas.drawString(endingLineX, startingLineY, "- $"+"{:.2f}".format(service['discount']))
            startingLineY -= line_height_counter

        startingLineY -= line_height_counter
        canvas.drawString(startingLineX, startingLineY, "Subtotal")
        canvas.drawString(endingLineX, startingLineY, "$"+"{:.2f}".format(float(service['subTotal']) - float(service['tax'])))
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Tax")
        canvas.drawString(endingLineX, startingLineY, "+ $"+"{:.2f}".format(service['tax']))
        startingLineY -= line_height_counter

        startingLineY -= line_height_counter
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(startingLineX, startingLineY, "Payment Details")
        canvas.setFont('Helvetica', 12)
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Payment Date")
        canvas.drawString(endingLineX, startingLineY, payment['PaymentDate'].strftime("%m/%d/%Y"))
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Total")
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(endingLineX, startingLineY, "$"+"{:.2f}".format(service['subTotal']))
        canvas.setFont('Helvetica', 12)
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Deposit")
        canvas.setFont('Helvetica-Bold', 12)    
        canvas.drawString(endingLineX, startingLineY, "- $"+"{:.2f}".format(payment["AmountReceived"]))
        canvas.setFont('Helvetica', 12) 
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Remaining")
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(endingLineX, startingLineY, "$"+"{:.2f}".format(float(service['subTotal']) - float(payment["AmountReceived"])))
        canvas.setFont('Helvetica', 12)
        startingLineY -= line_height_counter

        canvas.save()

    def printReceiptWithoutService(self, customerID, paymentID):
        object = Database_Class()
        customer = object.GetClientInfo(id=customerID)[0]
        payment = object.GetPaymentsbyID(paymentID=paymentID)[0]

        startingLineY = 700 
        line_height_counter = 24

        startingLineX = 100
        endingLineX = 250

        name = customer['FirstName'] + "_" + customer['LastName'] + "_"
        today = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        canvas = Canvas('./docs/'+name+today+".pdf")
        canvas.setFont('Helvetica', 12)

        name = customer['FirstName'] + " " + customer['LastName']
        canvas.drawString(startingLineX, startingLineY, "Customer")
        canvas.drawString(endingLineX, startingLineY, name)
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Balance")
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(endingLineX, startingLineY, "$"+"{:.2f}".format(customer['AccountBalance']))
        canvas.setFont('Helvetica', 12) 
        startingLineY -= line_height_counter

        startingLineY -= line_height_counter
        canvas.setFont('Helvetica-Bold', 12)
        canvas.drawString(startingLineX, startingLineY, "Payment Details")
        canvas.setFont('Helvetica', 12)
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Payment Date")
        canvas.drawString(endingLineX, startingLineY, payment['PaymentDate'].strftime("%m/%d/%Y"))
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Deposit")
        canvas.setFont('Helvetica-Bold', 12)    
        canvas.drawString(endingLineX, startingLineY, "- $"+"{:.2f}".format(payment["AmountReceived"]))
        canvas.setFont('Helvetica', 12) 
        startingLineY -= line_height_counter

        canvas.save()

    def printReceiptWithinDates(self):
        if (self.ui.report_search_list.currentItem()):
            object = Database_Class()
            customerID = int(self.ui.report_search_list.currentItem().text(4))
            startDate = self.ui.report_date_start.date().toString("yyyy-MM-dd")
            endDate = self.ui.report_date_end.date().toString("yyyy-MM-dd")

            customer = object.GetClientInfo(id=customerID)[0]
            payments = object.GetPaymentsbyDateRange(customerID=customerID, startDate=startDate, endDate=endDate)

            startingLineY = 750 
            line_height_counter = 24

            startingLineX = 100
            endingLineX = 250

            total_paid = 0

            name = customer['FirstName'] + "_" + customer['LastName'] + "_"
            today = datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
            canvas = Canvas('./docs/'+name+today+".pdf")

            canvas.setFont('Helvetica', 12)
            name = customer['FirstName'] + " " + customer['LastName']
            canvas.drawString(startingLineX, startingLineY, "Customer")
            canvas.drawString(endingLineX, startingLineY, name)
            startingLineY -= line_height_counter

            canvas.drawString(startingLineX, startingLineY, "Balance")
            canvas.setFont('Helvetica-Bold', 12)
            canvas.drawString(endingLineX, startingLineY, "$"+"{:.2f}".format(customer['AccountBalance']))
            canvas.setFont('Helvetica', 12) 
            startingLineY -= line_height_counter

            startingLineY -= line_height_counter
            canvas.setFont('Helvetica-Bold', 12)
            canvas.drawString(startingLineX, startingLineY, "Payments")
            canvas.setFont('Helvetica', 12)
            startingLineY -= line_height_counter

            for payment in payments:
                total_paid += float(payment["AmountReceived"])

                canvas.drawString(startingLineX, startingLineY, "Date")
                canvas.drawString(endingLineX, startingLineY, payment['PaymentDate'].strftime("%m/%d/%Y"))
                startingLineY -= line_height_counter

                if (startingLineY<115):
                    canvas.showPage() # adds a blank page
                    startingLineY = 750

                canvas.drawString(startingLineX, startingLineY, "Amount")
                canvas.setFont('Helvetica-Bold', 12)    
                canvas.drawString(endingLineX, startingLineY, "$"+"{:.2f}".format(payment["AmountReceived"]))
                canvas.setFont('Helvetica', 12) 
                startingLineY -= line_height_counter

                startingLineY -= line_height_counter

                if (startingLineY<115):
                    canvas.showPage() # adds a blank page
                    startingLineY = 750

            startingLineY -= line_height_counter
            canvas.drawString(startingLineX, startingLineY, "Total Paid")
            canvas.setFont('Helvetica-Bold', 12)
            canvas.drawString(endingLineX, startingLineY, "$"+"{:.2f}".format(total_paid))
            canvas.setFont('Helvetica', 12) 
            startingLineY -= line_height_counter

            canvas.save()
  
        else:
            MainWindow.show_popup(self,"Invalid Operation!","Please select a customer & payment to take a receipt!")

    def printReportMonthly(self):
        ReportFunctions.createReportsFolder(self)
        dayStart = "01"
        dayEnd = "30"

        months = {
            "January":"1",
            "February":"2",
            "March":"3",
            "April":"4",
            "May":"5",
            "June":"6",
            "July":"7",
            "August":"8",
            "September":"9",
            "October":"10",
            "November":"11",
            "December":"12",
        }

        month = self.ui.comboBox_4.currentText()
        year = self.ui.comboBox_5.currentText()

        startDate = year+"-"+months[month]+"-"+dayStart
        endDate = year+"-"+months[month]+"-"+dayEnd

        object = Database_Class()
        payments = object.GetPaymentsbyDateRange(customerID=-1,startDate=startDate, endDate=endDate)
        timeInfo = month + '_' + year + "_"
        ReportFunctions.printReport(self, payments, "Monthly", timeInfo)

    def printReportYearly(self):
        ReportFunctions.createReportsFolder(self)

        year = self.ui.comboBox_5.currentText()
        startDate = year+"-01-01"
        endDate = year+"-12-31"

        object = Database_Class()
        payments = object.GetPaymentsbyDateRange(customerID=-1,startDate=startDate, endDate=endDate)
        timeInfo = year + '_'
        ReportFunctions.printReport(self, payments, "Yearly", timeInfo)

    def printReport(self,payments, type, timeInfo):
        object = Database_Class()
        servicesinfo= object.GetDayCareRateAndTax(4)

        tax = 0
        for  service in servicesinfo:
            tax = service[1]

        total_paid = 0

        startingLineY = 750 
        startingLineX = 100
        endingLineX = 250
        line_height_counter = 24

        # 2021_Yearly_Report.pdf
        # 2021_April_Monthly_Report.pdf

        canvas = Canvas('./docs/'+timeInfo+type+"_Report.pdf")

        for payment in payments:
            total_paid += float(payment["AmountReceived"])

        canvas.setFont('Helvetica-Bold', 14)  
        canvas.drawString(50,startingLineY+line_height_counter,(timeInfo+type+"_Report").replace("_"," "))
        startingLineY -= line_height_counter
        canvas.setFont('Helvetica', 14) 

        total_tax = float(total_paid)*(tax/100)
        canvas.drawString(startingLineX, startingLineY, "Total Income")
        canvas.drawString(endingLineX, startingLineY, "$"+"{:.2f}".format(total_paid))
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Total Tax")
        canvas.drawString(endingLineX, startingLineY, "$"+ "{:.2f}".format(total_tax) )
        startingLineY -= line_height_counter

        canvas.drawString(startingLineX, startingLineY, "Taxable Income")
        canvas.drawString(endingLineX, startingLineY, "$"+"{:.2f}".format(total_paid-total_tax))
        startingLineY -= line_height_counter

        canvas.save()

# taxable income - total income
