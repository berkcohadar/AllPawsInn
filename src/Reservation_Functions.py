from socket import ntohl
from Payment_Functions import *
day_swicher = 0
selectedDays=[] # ARRAYS OF DATES THAT ARE ADDED FROM REZERVATION PAGE FROM THE UI.
class ReservationFunctions(MainWindow):

    def clear_reservations(self):
        self.ui.res_list.clear()
        self.ui.res_selected_days.clear()
        
    def updateReservationDisplay(self):  
        self.ui.res_list.clear()
        for obj in self.paws:  
            animalID = str(obj[3])
            customerID = str(obj[4])
            animalName = obj[2] 
            ownerName = obj[0] + " " + obj[1]

            self.ui.res_list.addTopLevelItem( QtWidgets.QTreeWidgetItem([ownerName , animalName, animalID, customerID ] ) )

    def AddDaysToSelectedDayList(self):
        global selectedDays
        if  self.ui.res_list.currentItem():
            if( self.ui.res_calendar.selectedDate()):
                date = self.ui.res_calendar.selectedDate()
                stringdate = date.toString("yyyy-MM-dd")
                
                if stringdate not in selectedDays:
                    selectedDays.append(stringdate)
               
                    item = QtWidgets.QTreeWidgetItem(self.ui.res_selected_days,[stringdate ])
                    self.ui.res_selected_days.addTopLevelItem(item)
            else:
                MainWindow.show_popup(self,"Invalid Operation!","Please select a day")
        else:
             MainWindow.show_popup(self,"Invalid Operation!","Please search for a client or pet name, then choose one")
                
    def RemoveDay(self):
        global selectedDays
        if(self.ui.res_selected_days.currentItem()    ):
            selectedDays.remove(self.ui.res_selected_days.currentItem().text(0))
            self.ui.res_selected_days.takeTopLevelItem(self.ui.res_selected_days.indexOfTopLevelItem(self.ui.res_selected_days.currentItem()))
        else:
               MainWindow.show_popup(self,"Invalid Operation!","Please choose a day to remove")
          
    def updateReservationList(self):

        text = self.ui.res_search_bar.text()
            
        if len(text) < 3:
            ReservationFunctions.clear_reservations(self)
            self.paws= []
        else:
            object = Database_Class()

            result = object.SearchForReservation()
           
            for paw in result:
                
                if text.lower() in paw[0].lower() or text.lower() in paw[1].lower() or text.lower() in paw[2].lower():
            
                    if paw not in self.paws:
                        self.paws.append(paw)           
                else:
                    if paw in self.paws:
                        print(paw)
                        self.paws.remove(paw)
            ReservationFunctions.updateReservationDisplay(self)  

    def SubmitReservation(self):
        global selectedDays
        if(self.ui.res_list.currentItem()):
            animalID = int(self.ui.res_list.currentItem().text(2))
            customerID = int(self.ui.res_list.currentItem().text(3))

            if selectedDays != []:
                selectedDays = sorted(selectedDays)
                reservationDates = []
                temp = 0
                for i in range(len(selectedDays)-1):
                    duration = datetime.strptime(selectedDays[i+1], '%Y-%m-%d') - datetime.strptime(selectedDays[i], '%Y-%m-%d')
                    if ( duration.days > 1): # if there is a gap between reservation dates. That means we have to create several reservations
                        reservationDates.append(selectedDays[temp:i+1])
                        reservationDates.append("-1") 
                        temp = i+1
                if len(reservationDates) == 0:
                    reservationDates.append(selectedDays)
                if reservationDates[-1] == "-1":
                    reservationDates.append(selectedDays[temp:])                   
                
                print(reservationDates)
                for days in reservationDates:
                    if days != '-1':
                        resStartDate = days[0]
                        resEndDate = days[-1]
                        dayCount = len(days)

                        object = Database_Class()
                        object.submitReservation(customerID, animalID, resStartDate, resEndDate, 0)

                selectedDays=[]
                ReservationFunctions.clear_reservations(self)
                self.ui.res_search_bar.setText("")
                self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home)
            else:
                MainWindow.show_popup(self,"Invalid Operation!","Please select a day")
            
        else:
            MainWindow.show_popup(self,"Invalid Operation!","Please search for a client or pet name, then choose one")

    def GenerateDaylyView(self, row0):
        object = Database_Class()
        
        result = object.GetDaycareForCurrentDate(row0)
        mytalbe = self.ui.Widget
        i=0
        j=0
        for k in result:
            array.append(k)
            self.ui.tableWidget.setItem(i,j, QtWidgets.QTableWidgetItem(k[0]+" "+k[1]+"\n"+k[2]))



             