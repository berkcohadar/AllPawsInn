
from EditClient_Functions import *
day_swicher = 0
class AddPetFunctions(MainWindow):


    def Set_newPet(self):
        if(self.ui.addpet_search_list.currentItem()):
            
            clientId = self.ui.addpet_search_list.currentItem().text(2)
            if(self.ui.addpet_name_input.text() and self.ui.addpet_breed_input.text() and self.ui.addpet_gender_input.text() and self.ui.addpet_age_input.text()  and self.ui.addpet_foodtype_input.text() and self.ui.addpet_foodfreq_input.text() and self.ui.addpet_medical_input.text() and self.ui.addpet_foodamount_input.text()):
                animalrow=(self.ui.addpet_name_input.text(),self.ui.addpet_breed_input.text(),self.ui.addpet_gender_input.text() ,self.ui.addpet_medical_input.text(),self.ui.addpet_foodtype_input.text(),self.ui.addpet_foodfreq_input.text() ,self.ui.addpet_foodamount_input.text() ,self.ui.addpet_age_input.text())
                object = Database_Class()
               

                
                object.CreateAnimal(clientId,animalrow)
                AddPetFunctions.clearSearchList(self)

                MainWindow.show_popup(self,"Success!","new Pet is added")
            else:
                MainWindow.show_popup(self,"Missing Information!","Please fill all areas missing!")
        else:

            MainWindow.show_popup(self,"Missing Client!","Please choose any client from List")
    def Delete_pet(self):
        i=0
        object = Database_Class()
        if(self.ui.addpet_search_list.currentItem()):
            clientId = self.ui.addpet_search_list.currentItem().text(2)
            pets= object.SearchForClientPet(int(clientId))
            for pet in pets:
                i+=1
            if(i==1):
                MainWindow.show_popup(self,"Warning!","This Client doesnt have another pet. Cant be removed!")
            else:    
                animalId= self.ui.addpet_search_list.currentItem().text(1)

                

                object.DeleteAnimal(animalId)
                AddPetFunctions.clearSearchList(self)
                self.ui.addpet_search_bar.clear()
                MainWindow.show_popup(self,"Warning!","Pet is removed")
        else:

            MainWindow.show_popup(self,"Missing Pet!","Please choose any pet from List")
    def clearSearchList(self):
        self.ui.addpet_search_list.clear()
                 
        self.ui.addpet_client_name.setText("")  
        self.ui.addpet_client_address.setText("")
        self.ui.addpet_client_cellphone.setText("")
        self.ui.addpet_client_email.setText("")
        self.ui.addpet_animal_name.setText("")  
        self.ui.addpet_animal_size.setText("")
        self.ui.addpet_animal_breed.setText("")

        self.ui.addpet_name_input.setText("")  
        self.ui.addpet_breed_input.setText("")
        self.ui.addpet_gender_input.setText("")
        self.ui.addpet_medical_input.setText("")
        self.ui.addpet_foodtype_input.setText("")  
        self.ui.addpet_foodfreq_input.setText("")
        self.ui.addpet_foodamount_input.setText("")
        self.ui.addpet_age_input.setText("")
    def updateSearchListDisplay(self):  
        self.ui.addpet_search_list.clear()
        for obj in self.paws:  
            animalID = str(obj[3]) 
            clientID = str(obj[4]) 
            animalName = obj[2] 
            ownerName = "Client: "+obj[0] + " " + obj[1] + " Pet: ("+obj[2]+")"
            self.ui.addpet_search_list.addTopLevelItem( QtWidgets.QTreeWidgetItem([ownerName ,animalID,clientID] ) )
    def updateSearchList(self):

            text = self.ui.addpet_search_bar.text()
                
            if len(text) < 3:
                AddPetFunctions.clearSearchList(self)
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
                AddPetFunctions.updateSearchListDisplay(self)  
    def DisplayDetail(self):
      
        object = Database_Class()
      
        animalId= self.ui.addpet_search_list.currentItem().text(1)
    
        clientId = self.ui.addpet_search_list.currentItem().text(2)
      
  
        animalInfo = object.GetAnimalInfo(int(animalId))
       

  
        for item in animalInfo:
            animalName = item['AnimalName']
            animalSize = item['Size']
            animalBreed = item['Breed']
            animalDateIn = item['DateIn']
            animalDateOut = item['DateOut']
            animalDaysIn = item['NoDays']
            
        self.ui.addpet_animal_name.setText(animalName)
        self.ui.addpet_animal_size.setText(animalSize)
        self.ui.addpet_animal_breed.setText(animalBreed)
        # self.ui.addpet_animal_date_in.setText(str(animalDateIn))
        # self.ui.addpet_animal_date_out.setText(str(animalDateOut))
        # self.ui.addpet_animal_day.setText(str(animalDaysIn))
        
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
                clientBalance = 0
                object.SetClientAccountBalance(int(clientId),float(0))

        self.ui.addpet_client_name.setText(clientName)  
        self.ui.addpet_client_address.setText(clientAddress)
        self.ui.addpet_client_cellphone.setText(clientCell)
        self.ui.addpet_client_email.setText(clientNotes)
        #TODO
        #client notes will be changed with client email
        self.ui.addpet_client_balance.setText(str(clientBalance))


