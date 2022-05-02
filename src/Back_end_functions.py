from Reservation_Functions import *

c = 1
_translate = QtCore.QCoreApplication.translate
array = []
result = []
class BackEndFunctions(MainWindow):
    
    def Clear_Bars(self):
        nothing = ""
        self.ui.first_name_bar.setText("")
        self.ui.last_name_bar.setText("")
        self.ui.email_bar.setText("")
        self.ui.address_bar.setText("")
        self.ui.country_bar.setText("")
        self.ui.region_bar.setText("")
        self.ui.town_bar.setText("")
        self.ui.home_phone_bar.setText("")
        self.ui.zip_bar.setText("")
        self.ui.cellphone_bar.setText("")
        self.ui.archive_box.setText("")
        self.ui.allow_mail_box.setText("")

        self.ui.animal_name_bar.setText("")
        self.ui.animal_breed_bar.setText("")
        self.ui.animal_sex_bar.setText("")
        self.ui.f_amount_bar.setText("")
        self.ui.food_type_bar.setText("")
        self.ui.age_bar.setText("")
        self.ui.k_unit_bar.setText("")
        self.ui.medical_details_bar.setText("")
        self.ui.discount_bar.setText("")
        self.ui.f_freq_bar.setText("")

        self.ui.practice_name_bar.setText("")
        self.ui.vet_name_bar.setText("")
        self.ui.contact_no_bar.setText("")
        self.ui.address_bar.setText("")  #clienttada address var?
        self.ui.town_bar.setText("")

    def GenerateDaylyView(self, row0):
        object = Database_Class()
        result = object.GetDaycareForCurrentDate(row0)
        i=0
        j=0
        for k in result:
            array.append(k)
            self.ui.home_reserved_tree.setItem(i,j, QtWidgets.QTableWidgetItem(k[0]+" "+k[1]+"\n"+k[2]))
            if(j ==  9):
                i+= 1
                j= 0
            else:
                j+=1
            #for i in range (0 , 9):
                #for j in range (0 , 7):
                
                #self.ui.tableWidget_3.setItem(i,j, QtWidgets.QTableWidgetItem("hello"))
                
                    #print(k)
                    #self.ui.tableWidget_3.setItem(i,j, QtWidgets.QTableWidgetItem(k[0]+k[1]+k[2]))
                    #self.ui.tableWidget_3.setItem(1,j, QtWidgets.QTableWidgetItem(k))
                    #mtable.setItem(0,1, new QTableWidgetItem("Hello"))
                
                    #item = self.ui.tableWidget_3.item(0 , 0)
                    
                    #item.setText(_translate("MainWindow", "omer"))
    def update_display(self):  
        self.ui.treeWidget_2.clear()
        for obj in self.paws:  
            animalID = str(obj[3])  
            bookingID = str(obj[5])  
            ownerName = obj[0] + " " + obj[1]
            self.ui.treeWidget_2.addTopLevelItem( QtWidgets.QTreeWidgetItem([ownerName , obj[2],obj[4],animalID,bookingID ] ) )
             
        
    def clear_display(self):
        self.ui.treeWidget_2.clear()

    def update_list(self):

        text = self.ui.search_bar.text()
        
        
        if len(text) < 3:
            BackEndFunctions.clear_display(self)
            self.paws= []
        else:
            object = Database_Class()
            #result = object.GetDaycareForCurrentDate(('2020-04-24 08:00:00.000' , '2017-04-25 08:00:00.000'))
            result = object.GetInfoForSearch()
           
            for paw in result:
                
                if text.lower() in paw[0].lower() or text.lower() in paw[1].lower() or text.lower() in paw[2].lower():
                  #  paw.setVisible(True)
                    if paw not in self.paws:
                        self.paws.append(paw)
                #print(paw)    
                else:
                #if text.lower() not in paw[0].lower() or text.lower() not in paw[1].lower() or text.lower() not in paw[2].lower():
                   # paw.setVisible(False)
                    if paw in self.paws:
                        print(paw)
                        self.paws.remove(paw)
            BackEndFunctions.update_display(self)

    def DirectCheckIn(self):
        bookingID = self.ui.treeWidget_2.currentItem().text(4)
        row = (bookingID ,"CheckedIn")
        object = Database_Class()
        object.DirectCheckInDB(row)

    def show(self):
        for w in self:
            w.setVisible(True)

    def hide(self):
        for w in self:
            w.setVisible(False)                    
            
    def clearCreateClientForms(self):
        self.ui.client_fname.clear()
        self.ui.client_lname.clear()
        self.ui.client_address.clear()
        self.ui.client_town.clear()
        self.ui.client_zipcode.clear()
        self.ui.client_email.clear()
        self.ui.client_hcontact.clear()
        self.ui.client_wcontact.clear()
        self.ui.client_emergency_name.clear()
        self.ui.client_emergency_phone.clear()

        self.ui.addpet_name_input_2.clear()
        self.ui.addpet_pet_size_2.clear()
        self.ui.addpet_breed_input_2.clear()
        self.ui.addpet_age_input_2.clear()
        self.ui.addpet_medical_input_2.clear()
        self.ui.addpet_notes_input_2.clear()
        self.ui.addpet_foodtype_input_2.clear()
        self.ui.addpet_weight_input_2.clear()
        self.ui.addpet_chip_input_2.clear()
        self.ui.addpet_vetname_input_2.clear()
        self.ui.addpet_pet_neutered_2.clear()
        self.ui.addpet_pet_type_2.clear()
        self.ui.addpet_pet_gender_2.clear()
        self.ui.addpet_pet_inactive_2.clear()

    def CREATE_CLIENT(self):
        client = {}
        pet = {}

        result = 1
        errorStyle = "border:1px solid rgb(255,0,0);"

        if not self.ui.client_fname.text():
            self.ui.client_fname.setStyleSheet(errorStyle)
            result = 0 
        else:
            client["FirstName"] = self.ui.client_fname.text()

        if not self.ui.client_lname.text():
            self.ui.client_lname.setStyleSheet(errorStyle)
            result = 0 
        else:
            client["LastName"] = self.ui.client_lname.text()
        
        client["Address1"] = self.ui.client_address.text()
        client["Town"] = self.ui.client_town.text()
        client["PostcodeZIP"] = self.ui.client_zipcode.text()
        client["Email"] = self.ui.client_email.text()
        client["CellMobile"] = self.ui.client_hcontact.text()
        client["TelHome"] = self.ui.client_wcontact.text()
        client["EmergencyContact"] = self.ui.client_emergency_name.text()
        client["EmergencyPhone"] = self.ui.client_emergency_phone.text()
        client["Mailings"] = self.ui.client_amailing_check.isChecked()

        if (client["Mailings"] == True):
            client["Mailings"] = 1
        else:
            client["Mailings"] = 0

        #----------------------------------------------------------------

        if not self.ui.addpet_name_input_2.text():
            self.ui.addpet_name_input_4.setStyleSheet(errorStyle)
            result = 0 
        else:
            pet["AnimalName"] = self.ui.addpet_name_input_2.text()

        pet["Size"] = self.ui.addpet_pet_size_2.text()
        pet["Breed"] = self.ui.addpet_breed_input_2.text()
        pet["DateOfBirth"] = self.ui.addpet_age_input_2.text()
        pet["MedicalConditions"] = self.ui.addpet_medical_input_2.text()
        pet["AnimalNotes"] = self.ui.addpet_notes_input_2.text()
        pet["FoodNotes"] = self.ui.addpet_foodtype_input_2.text() # food notes
        try:
            pet["Weight"] = float(self.ui.addpet_weight_input_2.text())
        except:
            MainWindow.show_popup(self,"Invalid Action!","Weight field must be a number!")
            self.ui.addpet_weight_input_2.setText("0.00")
            return
        pet["MicrochipID"] = self.ui.addpet_chip_input_2.text()
        pet["AnimalVet"] = self.ui.addpet_vetname_input_2.text()

        pet["NeuteredSpayed"] = self.ui.addpet_pet_neutered_2.currentText()
        pet["AnimalType"] = self.ui.addpet_pet_type_2.currentText()
        pet["Sex"] = self.ui.addpet_pet_gender_2.currentText()
        pet["Vaccinated"] = self.ui.addpet_pet_vaccinated_2.currentText()
        pet["Deceased"] = self.ui.addpet_pet_inactive_2.currentText()

        if pet["AnimalType"] == "Dog":
            pet["TypeID"] = 2
        else:
            pet["TypeID"] = 1

        if (pet["NeuteredSpayed"] == "Yes"):
            pet["NeuteredSpayed"] = 1
        else:
            pet["NeuteredSpayed"] = 0

        if (pet["Vaccinated"] == "Yes"):
            pet["Vaccinated"] = 1
        else:
            pet["Vaccinated"] = 0

        if (pet["Deceased"] == "Yes"):
            pet["Deceased"] = 1
        else:
            pet["Deceased"] = 0

        
        try:
            if (pet["DateOfBirth"]):
                today = datetime.now()
                birthdate = datetime.strptime(pet["DateOfBirth"], '%Y-%m-%d')
                age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
                pet["Age"] = int(age)
        except:
            pet["DateOfBirth"] = ""

        #----------------------------------------------------------------

        if(result == 1):
            object=Database_Class()
            object.setNewClient(client, pet)

            BackEndFunctions.clearCreateClientForms(self)
        else:
            print("Error")


    #======================================================================
    def nextday(self):
        global c
        d = QtCore.QDate.currentDate().addDays(c)
        self.ui.dateEdit.setDate(d)
        self.ui.textEdit_31.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">"+d.toString(QtCore.Qt.ISODate)+"</span></p></body></html>"))
        c= c+1
        

    def previousday(self):
        global c
        d = QtCore.QDate.currentDate().addDays(c-1)
        self.ui.dateEdit.setDate(d)
        self.ui.textEdit_31.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">"+d.toString(QtCore.Qt.ISODate)+"</span></p></body></html>"))
        c= c-1

    def getcurrentday(self):
        global c
        d = QtCore.QDate.currentDate()
        self.ui.dateEdit.setDate(d)
        self.ui.textEdit_31.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">"+d.toString(QtCore.Qt.ISODate)+"</span></p></body></html>"))
        c= 0


