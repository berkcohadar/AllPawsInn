
from ui_functions import *
day_swicher = 0
week_list =[]
dayofweek = 0
class WeeklyScheduleFunctions(MainWindow):
    def DisplayWeeklyList(self):

        
        global dayofweek
        global day_swicher
        date = QtCore.QDate.currentDate()
        dayofweek = date.dayOfWeek()
     
    
        while dayofweek !=0:
            day_swicher -=1
            date = QtCore.QDate.currentDate().addDays(day_swicher)
            dayofweek=dayofweek - 1
        
        self.ui.weekly_date_sunday.setDate(QtCore.QDate.currentDate().addDays(day_swicher))
        self.ui.weekly_date_monday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+1))
        self.ui.weekly_date_tuesday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+2))
        self.ui.weekly_date_wednesday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+3))
        self.ui.weekly_date_thursday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+4))
        self.ui.weekly_date_friday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+5))
        self.ui.weekly_date_saturday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+6))

        WeeklyScheduleFunctions.DisplayWeeklySchedule(self,day_swicher)



     #   item = QtWidgets.QTreeWidgetItem(self.ui.res_selected_days,[stringdate ])
     #               self.ui.res_selected_days.addTopLevelItem(item)
    def DisplayWeeklySchedule(self,day_swicher):
        obj= Database_Class()
      
        #self.ui.weekly_date_sunday.getDate()
        days =[]
        
        myswicher = day_swicher
        for i in range(7):

            day1= QtCore.QDate.currentDate().addDays(myswicher).toString("yyyy-MM-dd")
            day2 =QtCore.QDate.currentDate().addDays(myswicher+1).toString("yyyy-MM-dd")
            days.append(day1)
            days.append(day2)
            myswicher +=1
        
 
        self.ui.weekly_shedule_table.setRowCount(0)
       # self.ui.weekly_shedule_table.clear()
        for i in range (20):
            rowPosition = self.ui.weekly_shedule_table.rowCount()
            self.ui.weekly_shedule_table.insertRow(rowPosition)
        sunday = obj.GetReservations(days[0],days[1])
        j = 0
        for name in sunday:
            
            asd =name[0]+" "+name[1] + " / "+ name[2] 
            self.ui.weekly_shedule_table.setItem(j, 0, QtWidgets.QTableWidgetItem(asd));
            j+=1
        monday = obj.GetReservations(days[2],days[3])
        j = 0
        for name in monday:
            
            asd =name[0]+" "+name[1] + " / "+ name[2] 
            self.ui.weekly_shedule_table.setItem(j, 1, QtWidgets.QTableWidgetItem(asd));
            j+=1
        tuesday = obj.GetReservations(days[4],days[5])
        j = 0
        for name in tuesday:
            
            asd =name[0]+" "+name[1] + " / "+ name[2] 
            self.ui.weekly_shedule_table.setItem(j, 2, QtWidgets.QTableWidgetItem(asd));
            j+=1
        wednesday = obj.GetReservations(days[6],days[7])
        j = 0
        for name in wednesday:
            
            asd =name[0]+" "+name[1] + " / "+ name[2] 
            self.ui.weekly_shedule_table.setItem(j, 3, QtWidgets.QTableWidgetItem(asd));
            j+=1
        thursday = obj.GetReservations(days[8],days[9])
        j = 0
        for name in thursday:
            
            asd =name[0]+" "+name[1] + " / "+ name[2] 
            self.ui.weekly_shedule_table.setItem(j, 4, QtWidgets.QTableWidgetItem(asd));
            j+=1
        friday = obj.GetReservations(days[10],days[11])
        j = 0
        for name in friday:
            
            asd =name[0]+" "+name[1] + " / "+ name[2] 
            self.ui.weekly_shedule_table.setItem(j, 5, QtWidgets.QTableWidgetItem(asd));
            j+=1
        saturday = obj.GetReservations(days[12],days[13])
        j = 0
        for name in saturday:
            
            asd =name[0]+" "+name[1] + " / "+ name[2] 
            self.ui.weekly_shedule_table.setItem(j, 6, QtWidgets.QTableWidgetItem(asd));
            j+=1
      

        
       
    

      

        # pazartesi olan hepsi 
        # sali hepsi

       
     
     
            

    def NextWeek(self):
        
        global dayofweek
        global day_swicher
        day_swicher +=7
        date = QtCore.QDate.currentDate()
        dayofweek = date.dayOfWeek()
     
    
        
        
        self.ui.weekly_date_sunday.setDate(QtCore.QDate.currentDate().addDays(day_swicher))
        self.ui.weekly_date_monday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+1))
        self.ui.weekly_date_tuesday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+2))
        self.ui.weekly_date_wednesday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+3))
        self.ui.weekly_date_thursday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+4))
        self.ui.weekly_date_friday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+5))
        self.ui.weekly_date_saturday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+6))
        WeeklyScheduleFunctions.DisplayWeeklySchedule(self,day_swicher)
    def PreviousWeek(self):
        
        global dayofweek
        global day_swicher
        day_swicher -=7
        date = QtCore.QDate.currentDate()
        dayofweek = date.dayOfWeek()
        
    
        
        
        self.ui.weekly_date_sunday.setDate(QtCore.QDate.currentDate().addDays(day_swicher))
        self.ui.weekly_date_monday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+1))
        self.ui.weekly_date_tuesday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+2))
        self.ui.weekly_date_wednesday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+3))
        self.ui.weekly_date_thursday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+4))
        self.ui.weekly_date_friday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+5))
        self.ui.weekly_date_saturday.setDate(QtCore.QDate.currentDate().addDays(day_swicher+6))
        WeeklyScheduleFunctions.DisplayWeeklySchedule(self,day_swicher)
    def ThisWeek(self):
        global day_swicher
        day_swicher = 0
        WeeklyScheduleFunctions.DisplayWeeklyList(self)
       
       