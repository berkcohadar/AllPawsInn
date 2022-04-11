
from EditClient_Functions import *
day_swicher = 0
class AddPetFunctions(MainWindow):


    def add_new_pet(self):
        if(self.ui.addpet_search_list.currentItem()):

            
            clientId = self.ui.addpet_search_list.currentItem().text(2)
            if(self.ui.addpet_name_input_4.text()):
                object = Database_Class()
                animalRow = {}

                animalRow["ClientID"] = int(clientId)
                animalRow["AnimalName"] = self.ui.addpet_name_input_4.text()
                animalRow["Size"] = self.ui.addpet_pet_size_4.text()
                animalRow["Breed"] = self.ui.addpet_breed_input_4.text()
                animalRow["DateOfBirth"] = self.ui.addpet_age_input_4.text()
                animalRow["MedicalConditions"] = self.ui.addpet_medical_input_4.text()
                animalRow["AnimalNotes"] = self.ui.addpet_notes_input_4.text()
                animalRow["FoodNotes"] = self.ui.addpet_foodtype_input_4.text()
                animalRow["Weight"] = float(self.ui.addpet_weight_input_4.text())
                animalRow["MicrochipID"] = self.ui.addpet_chip_input_4.text()
                animalRow["animalVetname"] = self.ui.addpet_vetname_input_4.text()

                animalRow["NeuteredSpayed"] = self.ui.addpet_pet_neutered_4.currentText()
                animalRow["AnimalType"] = self.ui.addpet_pet_type_4.currentText()
                animalRow["Sex"] = self.ui.addpet_pet_gender_4.currentText()
                animalRow["Vaccinated"] = self.ui.addpet_pet_vaccinated_4.currentText()
                animalRow["Deceased"] = self.ui.addpet_pet_inactive_4.currentText()

                if animalRow["AnimalType"] == "Dog":
                    animalRow["TypeID"] = 2
                else:
                    animalRow["TypeID"] = 1

                if (animalRow["NeuteredSpayed"] == "Yes"):
                    animalRow["NeuteredSpayed"] = 1
                else:
                    animalRow["NeuteredSpayed"] = 0

                if (animalRow["Vaccinated"] == "Yes"):
                    animalRow["Vaccinated"] = 1
                else:
                    animalRow["Vaccinated"] = 0

                if (animalRow["Deceased"] == "Yes"):
                    animalRow["Deceased"] = 1
                else:
                    animalRow["Deceased"] = 0

                if (animalRow["DateOfBirth"]):
                    today = datetime.datetime.now()
                    birthdate = datetime.datetime.strptime(animalRow["DateOfBirth"], '%Y-%m-%d')
                    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
                    animalRow["Age"] = int(age)

                object.CreateAnimal(animalRow)
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


        self.ui.addpet_name_input.setText("")  
        self.ui.addpet_breed_input.setText("")
        self.ui.addpet_medical_input.setText("")
        self.ui.addpet_foodtype_input.setText("")  

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
            animalSize = item['Size'] # Small Medium Large XLarge
            animalBreed = item['Breed']
            animalGender = item['Sex']
            animalNeutered = item['NeuteredSpayed']
            animalMedicalNotes = item['MedicalConditions']
            animalNotes = item['AnimalNotes']
            animalAge = item['Age']
            animalDateOfBirth = item['DateOfBirth']
            animalFoodNotes = item['FoodNotes']
            animalType = item['AnimalType']
            animalVaccinated = item['Vaccinated']
            animalWeight = item['Weight']
            animalMicrochipID = item['MicrochipID']
            animalInactive = item['Deceased']

        self.ui.addpet_animal_name.setText(animalName)
        self.ui.addpet_animal_age.setText(str(animalAge))
        self.ui.addpet_animal_date_in_2.setText(str(animalDateIn))
        self.ui.addpet_animal_date_out.setText(str(animalDateOut))
        self.ui.addpet_animal_date_in.setText(str(animalDaysIn))
        
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
        self.ui.addpet_client_balance.setText(str(clientBalance))
        
        if (animalNeutered):
            animalNeutered = 'Yes'
        else:
            animalNeutered = 'No'
 
        if (animalVaccinated):
            animalVaccinated = 'Yes'
        else:
            animalVaccinated = 'No'
            
        if (animalInactive ):
            animalInactive = 'Yes'
        else:
            animalInactive = 'No'

        if (animalDateOfBirth):
            animalDateOfBirth = animalDateOfBirth.strftime("%Y-%m-%d")

        if (animalWeight == None):
            animalWeight = 0.0
        
        # Edit Pet
        self.ui.addpet_name_input.setText(animalName)
        self.ui.addpet_breed_input.setText(animalBreed)
        self.ui.addpet_age_input.setText(animalDateOfBirth)
        self.ui.addpet_medical_input.setText(animalMedicalNotes)
        self.ui.addpet_weight_input.setText(str(animalWeight))
        self.ui.addpet_pet_size.setText(animalSize)
        self.ui.addpet_foodtype_input.setText(animalFoodNotes) # food notes
        self.ui.addpet_notes_input.setText(animalNotes)
        self.ui.addpet_chip_input.setText(animalMicrochipID)
        # self.ui.addpet_vetname_input.setText()

        # combo box
        self.ui.addpet_pet_neutered.setCurrentText(animalNeutered)
        self.ui.addpet_pet_type.setCurrentText(animalType)
        self.ui.addpet_pet_gender.setCurrentText(animalGender)
        self.ui.addpet_pet_vaccinated.setCurrentText(animalVaccinated)
        self.ui.addpet_pet_inactive.setCurrentText(animalInactive)


    def updateAnimalDetails(self):
        object = Database_Class()

        row = {}
        row["AnimalName"] = self.ui.addpet_name_input.text()
        row["Size"] = self.ui.addpet_pet_size.text()
        row["Breed"] = self.ui.addpet_breed_input.text()
        row["DateOfBirth"] = self.ui.addpet_age_input.text()
        row["MedicalConditions"] = self.ui.addpet_medical_input.text()
        row["AnimalNotes"] = self.ui.addpet_notes_input.text()
        row["FoodNotes"] = self.ui.addpet_foodtype_input.text() # food notes
        row["Weight"] = float(self.ui.addpet_weight_input.text())
        row["MicrochipID"] = self.ui.addpet_chip_input.text()
        row["AnimalID"] = int(self.ui.addpet_search_list.currentItem().text(1))
        # row["animalVetname"] = self.ui.addpet_vetname_input.text()

        row["NeuteredSpayed"] = self.ui.addpet_pet_neutered.currentText()
        row["AnimalType"] = self.ui.addpet_pet_type.currentText()
        row["Sex"] = self.ui.addpet_pet_gender.currentText()
        row["Vaccinated"] = self.ui.addpet_pet_vaccinated.currentText()
        row["Deceased"] = self.ui.addpet_pet_inactive.currentText()


        if (row["NeuteredSpayed"] == "Yes"):
            row["NeuteredSpayed"] = 1
        else:
            row["NeuteredSpayed"] = 0

        if (row["Vaccinated"] == "Yes"):
            row["Vaccinated"] = 1
        else:
            row["Vaccinated"] = 0

        if (row["Deceased"] == "Yes"):
            row["Deceased"] = 1
        else:
            row["Deceased"] = 0

        if (row["DateOfBirth"]):
            today = datetime.datetime.now()
            birthdate = datetime.datetime.strptime(row["DateOfBirth"], '%Y-%m-%d')
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            row["Age"] = int(age)

        object.UpdateAnimalDetails(row)    