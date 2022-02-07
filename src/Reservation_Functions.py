from socket import ntohl
from Payment_Functions import *
day_swicher = 0
selectedDays=[]
class ReservationFunctions(MainWindow):

    def clear_reservations(self):
        self.ui.res_list.clear()
        self.ui.res_selected_days.clear()
        
    def updateReservationDisplay(self):  
        self.ui.res_list.clear()
        for obj in self.paws:  
            animalID = str(obj[3])  
            animalName = obj[2] 
            ownerName = obj[0] + " " + obj[1]
            self.ui.res_list.addTopLevelItem( QtWidgets.QTreeWidgetItem([ownerName , animalName,animalID ] ) )
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
            print(selectedDays)
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

    def DisplayReservations(self,today,tommorrow):
        object = Database_Class()

        result = object.GetReservations(today,tommorrow)
        
    
        self.ui.treeWidget.clear()
        for obj in result:  
            animalID = str(obj[3])  
            animalName = obj[2] 
            status = obj[4]
            date = str(obj[6])          
            ownerName = obj[0] + " " + obj[1]
            item = QtWidgets.QTreeWidgetItem(self.ui.treeWidget,[ownerName , animalName,status,date ])
            self.ui.treeWidget.addTopLevelItem(item)
           # QTreeWidgetItem *items = new QTreeWidgetItem(self.ui.treeWidget)
           # items.setText(0, tr("Owner Name"))
           # self.ui.treeWidget.addTopLevelItem( QtWidgets.QTreeWidgetItem([ownerName , animalName,status,date,animalID ] ) )

    def SubmitReservation(self):
     
        global selectedDays
        if(self.ui.res_list.currentItem()):
            AnimalID =self.ui.res_list.currentItem().text(2)
            KennelID= 1
            date = self.ui.res_calendar.selectedDate()
            stringdate =date.toString("yyyy-MM-dd")
    

        
            if selectedDays != []:

            #UpdateStatus()
                for days in selectedDays:

                    row = (AnimalID,KennelID,"Reserved",days)
                    print(row)
                    object = Database_Class()
                    object.SubmitReservation(row)
                selectedDays=[]
                ReservationFunctions.clear_reservations(self)
                self.ui.res_search_bar.setText("")
                self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home)
            else:
                MainWindow.show_popup(self,"Invalid Operation!","Please select a day")
            
        else:
          
            MainWindow.show_popup(self,"Invalid Operation!","Please search for a client or pet name, then choose one")
         

    def NextDay(self):

       
        global day_swicher
        day_swicher= day_swicher+1
        day = QtCore.QDate.currentDate().addDays(day_swicher)
        day1 = QtCore.QDate.currentDate().addDays(day_swicher).toString("yyyy-MM-dd")
   
        day2 = QtCore.QDate.currentDate().addDays(day_swicher+1).toString("yyyy-MM-dd")
        print(day1 +""+day2)
        self.ui.dateEdit.setDate(day)
        ReservationFunctions.DisplayReservations(self,day1,day2)
        

    def PreviosDay(self):

        global day_swicher
        day_swicher= day_swicher-1
        day = QtCore.QDate.currentDate().addDays(day_swicher)
        day1 = QtCore.QDate.currentDate().addDays(day_swicher+1).toString("yyyy-MM-dd")
   
        day2 = QtCore.QDate.currentDate().addDays(day_swicher).toString("yyyy-MM-dd")
        print(day2 +""+day1)
        self.ui.dateEdit.setDate(day)
        ReservationFunctions.DisplayReservations(self,day2,day1)
        

    def GenerateDaylyView(self, row0):
        
        object = Database_Class()
        
        result = object.GetDaycareForCurrentDate(row0)
        mytalbe = self.ui.Widget
        i=0
        j=0
        for k in result:
            array.append(k)
            self.ui.tableWidget.setItem(i,j, QtWidgets.QTableWidgetItem(k[0]+" "+k[1]+"\n"+k[2]))
         #   if(j ==  9):
         #       i+= 1
         #       j= 0
         #   else:
         #       j+=1


             