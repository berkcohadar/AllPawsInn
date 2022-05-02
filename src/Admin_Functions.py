
from AdditionalPet_Functions import *
day_swicher = 0
# admin_discount
# admin_is_active
# adminProfile

selectedAdminProfile = -1
class AdminFunctions(MainWindow):

    def DisplayAdminList(self):
        self.ui.admin_profile_list.setHeaderHidden(False)
        self.ui.admin_service_list.setHeaderHidden(False)
        object = Database_Class()

        result = object.GetAdminListWithID()
        
        self.ui.admin_profile_list.clear()
        for obj in result:  
            ProfileName = obj[0]
            DayCareRate = str(obj[1] )  
            Tax =str( obj[2])
            IsActive =str(obj[3])
            ID = str(obj[4])
            item = QtWidgets.QTreeWidgetItem(self.ui.admin_profile_list,[ ProfileName,DayCareRate,Tax, IsActive,ID])
            self.ui.admin_profile_list.addTopLevelItem(item)

    def AddAdminSetting(self):
        object = Database_Class()

        profilename = self.ui.admin_profile_name.text()
        daycarerate = self.ui.admin_daycare_rate.text()
        tax = self.ui.admin_tax.text()
        active = self.ui.admin_is_active.currentText()

        if active == "False":
            active = 0
        else: 
            active = 1

        if(profilename=='' or daycarerate=='' or tax==''):
            MainWindow.show_popup(self,"Invalid Action!","Required fields are missing! You must enter a profile name, daycare rate, and tax.")
        else:
            try:
                daycare = float(daycarerate)
            except:
                MainWindow.show_popup(self,"Invalid Action!","Daycare field is not valid. Please enter a number to continue!")
                return
            try:
                tax = float(tax)
            except:
                MainWindow.show_popup(self,"Invalid Action!","Tax field is not valid. Please enter a number to continue!")
                return
            profileId = object.SetAdminSetting(profilename,daycare,tax,active)
            AdminFunctions.AddServices(self,"food",25.0,profileId)
            AdminFunctions.AddServices(self,"nails",10.0,profileId)
            AdminFunctions.AddServices(self,"hair",10.0,profileId)

            self.ui.admin_profile_name.clear()
            self.ui.admin_daycare_rate.clear()
            self.ui.admin_tax.clear()
            AdminFunctions.DisplayAdminList(self)

    def ActivateProfile(self):
        object = Database_Class()
        if (self.ui.admin_profile_list.currentItem()):
            active = self.ui.admin_profile_list.currentItem().text(3)
            if(active == "False"):
                id = self.ui.admin_profile_list.currentItem().text(4)
                object.SetAllInActive()
                object.SetActive(int(id))
                AdminFunctions.DisplayAdminList(self)
        else:
            MainWindow.show_popup(self,"Invalid Action!","Please select a profile to operate the action.")

    def DeleteProfile(self):
        object = Database_Class()
        if (self.ui.admin_profile_list.currentItem()):
            active = self.ui.admin_profile_list.currentItem().text(3)
            if(active == "False"):
                id = self.ui.admin_profile_list.currentItem().text(4)
            
                object.DeleteProfile(int(id))
                AdminFunctions.DisplayAdminList(self)
            else:
                MainWindow.show_popup(self,"Invalid Action!","You cannot delete an active profile. First activate another profile.")
        else:
            MainWindow.show_popup(self,"Invalid Action!","Please select a profile to operate the action.")
            

    def GetServices(self):
        global selectedAdminProfile
        object = Database_Class()
        adminProfile = int(self.ui.admin_profile_list.currentItem().text(4))
        selectedAdminProfile = adminProfile
        services = object.GetServices(adminProfile)
        self.ui.admin_service_list.clear()

        for obj in services:  
            Name = obj[0]
            Cost = str(obj[1] )  
          
            item = QtWidgets.QTreeWidgetItem(self.ui.admin_service_list,[ Name,Cost,str(adminProfile)])
            self.ui.admin_service_list.addTopLevelItem(item)


    def AddServices(self,name,cost,adminProfile):
        if (name and cost and adminProfile):
            pass
        else:
            name =self.ui.admin_service_name.text()
            cost = self.ui.admin_service_cost.text()
            adminProfile = selectedAdminProfile

        isActive = 1

        object = Database_Class()
        if (name and cost and adminProfile):
            object.AddService(name,int(cost),isActive,adminProfile)

            services = object.GetServices(adminProfile)
            self.ui.admin_service_list.clear()
            self.ui.admin_service_name.clear()
            self.ui.admin_service_cost.clear()
            for obj in services:  
                Name = obj[0]
                Cost = str(obj[1] )  
            
                item = QtWidgets.QTreeWidgetItem(self.ui.admin_service_list,[ Name,Cost,str(adminProfile)])
                self.ui.admin_service_list.addTopLevelItem(item)
        else:
            MainWindow.show_popup(self,"Invalid Action!","Please enter Service Name and Cost!")



    def ChangeServiceCost(self):
        object = Database_Class()
        if (self.ui.admin_service_list.currentItem()):
            newcost = self.ui.admin_service_cost_box.text()
            adminProfile = selectedAdminProfile

            name = self.ui.admin_service_list.currentItem().text(0)
            object.ChangeServiceCost(float(newcost),name, adminProfile)

            services = object.GetServices(adminProfile)
            self.ui.admin_service_list.clear()
            self.ui.admin_service_name_label.clear()
            self.ui.admin_service_cost_box.clear()
            for obj in services:  
                Name = obj[0]
                Cost = str(obj[1] )  
            
                item = QtWidgets.QTreeWidgetItem(self.ui.admin_service_list,[ Name,Cost,str(adminProfile)])
                self.ui.admin_service_list.addTopLevelItem(item)
        else:
            MainWindow.show_popup(self,"Invalid Action!","Please select a profile to operate the action.")
        
    def ChangeCurrentService(self):  
        name = self.ui.admin_service_list.currentItem().text(0)
        cost = self.ui.admin_service_list.currentItem().text(1)
        
        self.ui.admin_service_name_label.setText(name)
        self.ui.admin_service_cost_box.setText(cost) 


        
    