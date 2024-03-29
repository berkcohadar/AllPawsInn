
from WeeklySchedule_Functions import *
day_swicher = 0
class EditClientFunctions(MainWindow):

    def clearSearchList(self):
        self.ui.editclient_search_list.clear()
      
    def updateSearchListDisplay(self):  
        self.ui.editclient_search_list.clear()
        for obj in self.paws:  
            animalID = str(obj[3]) 
            clientID = str(obj[4]) 
         
            ownerName = "Client: "+obj[0] + " " + obj[1] 
            self.ui.editclient_search_list.addTopLevelItem( QtWidgets.QTreeWidgetItem([ownerName ,animalID,clientID] ) )
    def updateSearchList(self):

            text = self.ui.editclient_search_bar.text()
                
            if len(text) < 3:
                EditClientFunctions.clearSearchList(self)
                self.paws= []
            else:
                object = Database_Class()

                result = object.SearchForPayment()
            
                for paw in result:
                    
                    if text.lower() in paw[0].lower() or text.lower() in paw[1].lower():
                
                        if paw not in self.paws:
                            self.paws.append(paw)           
                    else:
                        if paw in self.paws:
                            print(paw)
                            self.paws.remove(paw)
                EditClientFunctions.updateSearchListDisplay(self)  
    def DisplayDetail(self):
      
        object = Database_Class()
      
        animalId= self.ui.editclient_search_list.currentItem().text(1)
    
        clientId = self.ui.editclient_search_list.currentItem().text(2)
      
  
        animalInfo = object.GetAnimalInfo(int(animalId))
        animalDateIn = ""
        animalDateOut = ""
        animalDaysIn = ""
        serviceDetails = ""

        try:
            serviceDetails = object.getLastServicesDetails(animalId)[0]
            animalDateIn = serviceDetails['resStartDate'].strftime("%Y-%m-%d")
            animalDateOut = serviceDetails['resEndDate'].strftime("%Y-%m-%d")
            animalDaysIn = str(serviceDetails['daysIn'])
        except:
            pass

        for item in animalInfo:
            animalName = item['AnimalName']
            animalSize = item['Size']
            animalBreed = item['Breed']

        self.ui.edit_pet_name.setText(animalName)
        self.ui.edit_animal_size.setText(animalSize)
        self.ui.edit_animal_breed.setText(animalBreed)
        self.ui.pay_animal_date_in_4.setText(str(animalDateIn))
        self.ui.pay_animal_date_out_4.setText(str(animalDateOut))
        self.ui.pay_animal_day_4.setText(str(animalDaysIn))

        clientInfo = object.GetClientInfo(int(clientId))
        for client in clientInfo:
            clientName = client['FirstName'] + " " + client['LastName']
            clientFname = client['FirstName']
            clientLname = client['LastName']
            clientAddress = client['Address1']
            clientCell = client['CellMobile']
            clientNotes = client['Email']
            clientown = client['Town']
            clientZIP = client['PostcodeZIP']
            if client['AccountBalance'] :
                clientBalance = client['AccountBalance']
            else:
                clientBalance = 0
                object.SetClientAccountBalance(int(clientId),float(0))

        self.ui.edit_client_name.setText(clientName)  
        self.ui.edit_client_address.setText(clientAddress)
        self.ui.edit_client_cellphone.setText(clientCell)
        self.ui.edit_client_email.setText(clientNotes)
        #TODO
        #client notes will be changed with client email
        self.ui.edit_client_balance.setText(str(clientBalance))

        self.ui.edit_client_name_input.setText(clientFname)
        self.ui.edit_client_surname_input.setText(clientLname)
        self.ui.edit_client_address_input.setText(clientAddress)
        self.ui.edit_client_mobile_input.setText(clientCell)
        self.ui.edit_client_email_input.setText(clientNotes)
        self.ui.edit_client_town_input.setText(clientown)
        self.ui.edit_client_zipcode_input.setText(clientZIP)

    def editClient(self):

        object = Database_Class()
        if(self.ui.editclient_search_list.currentItem()):
            clientId = self.ui.editclient_search_list.currentItem().text(2)
            if(self.ui.edit_client_address_input.text() and self.ui.edit_client_mobile_input.text()
            and self.ui.edit_client_email_input.text()
            and self.ui.edit_client_zipcode_input.text()
            and self.ui.edit_client_name_input.text()
            and self.ui.edit_client_surname_input.text()):

                name=self.ui.edit_client_name_input.text()
                surname=self.ui.edit_client_surname_input.text()
                address=self.ui.edit_client_address_input.text()
                cell=self.ui.edit_client_mobile_input.text()
                email=self.ui.edit_client_email_input.text()
                town= self.ui.edit_client_town_input.text()
                zip=self.ui.edit_client_zipcode_input.text()
                cell2= self.ui.edit_client_alternate_input.text()

                object.EditClient(name,surname,email,address,town,zip,cell,cell2,int(clientId))
                EditClientFunctions.DisplayDetail(self)
            else:
                MainWindow.show_popup(self,"Missing Information!","Please fill missing areas!")
        else:
            MainWindow.show_popup(self,"Missing Information!","Please choose a client!")