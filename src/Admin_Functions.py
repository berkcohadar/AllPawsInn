
from AdditionalPet_Functions import *
day_swicher = 0
class AdminFunctions(MainWindow):

    def DisplayAdminList(self):
        object = Database_Class()

        result = object.GetAdminListWithID()
        
    
        self.ui.admin_profile_list.clear()
        for obj in result:  
            ProfileName = obj[0]
            DayCareRate = str(obj[1] )  
            Tax =str( obj[2])
            Discount =str( obj[3])
            IsActive =str(obj[4]  )        
            BookingRate = str(obj[5])
            ID = str(obj[6])
            item = QtWidgets.QTreeWidgetItem(self.ui.admin_profile_list,[ ProfileName,DayCareRate,BookingRate,Tax,Discount, IsActive,ID])
            self.ui.admin_profile_list.addTopLevelItem(item)

    def AddAdminSetting(self):
        object = Database_Class()

        profilename = self.ui.admin_profile_name.text()
        daycarerate = self.ui.admin_daycare_rate.text()
        tax = self.ui.admin_tax.text()
        discount = self.ui.admin_discount.text()

        if(profilename=='' or daycarerate=='' or tax=='' or discount=='' or daycarerate==''):
            print("error")
        else:
            daycare = float(daycarerate)
            bookingrate = daycare + daycare*float(tax)/100


      
       
            object.SetAdminSetting(profilename,daycare,float(tax),float(discount),False,bookingrate)
            AdminFunctions.DisplayAdminList(self)

    def ActivateProfile(self):
        object = Database_Class()

        active = self.ui.admin_profile_list.currentItem().text(5)
        if(active == "False"):
            id = self.ui.admin_profile_list.currentItem().text(6)
            object.SetAllInActive()
            object.SetActive(int(id))
            AdminFunctions.DisplayAdminList(self)
       

    def DeleteProfile(self):
        object = Database_Class()
        active = self.ui.admin_profile_list.currentItem().text(5)
        if(active == "False"):
            id = self.ui.admin_profile_list.currentItem().text(6)
          
            object.DeleteProfile(int(id))
            AdminFunctions.DisplayAdminList(self)


    def GetServices(self):
        object = Database_Class()
        services = object.GetServices()
        self.ui.admin_service_list.clear()
        for obj in services:  
            Name = obj[0]
            Cost = str(obj[1] )  
          
            item = QtWidgets.QTreeWidgetItem(self.ui.admin_service_list,[ Name,Cost])
            self.ui.admin_service_list.addTopLevelItem(item)


    def AddServices(self):

        name =self.ui.admin_service_name.text()
        cost = self.ui.admin_service_cost.text()
        object = Database_Class()
        object.AddService(name,int(cost))


    def ChangeServiceCost(self):
        object = Database_Class()
       
        newcost = self.ui.admin_service_cost_box.text()

        name = self.ui.admin_service_list.currentItem().text(0)
        object.ChangeServiceCost(float(newcost),name)
        AdminFunctions.GetServices(self)
        self.ui.admin_service_name_label.clear()
        self.ui.admin_service_cost_box.clear()
        
    def ChangeCurrentService(self):  
        name = self.ui.admin_service_list.currentItem().text(0)
        cost = self.ui.admin_service_list.currentItem().text(1)
        
        self.ui.admin_service_name_label.setText(name)
        self.ui.admin_service_cost_box.setText(cost) 


        
    