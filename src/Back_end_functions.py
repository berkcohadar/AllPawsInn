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
        mytalbe = self.ui.home_reserved_tree
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
        #animalName = self.ui.treeWidget_2.currentItem().text(2)
        bookingID =self.ui.treeWidget_2.currentItem().text(4)
        #UpdateStatus()
        row = (bookingID ,"CheckedIn")
        print(row)
        object = Database_Class()
        object.DirectCheckInDB(row)
        
        x=2
    def show(self):
        for w in self:
            w.setVisible(True)

    def hide():
        for w in self:
            w.setVisible(False)                    
            
            
    def CREATE_CLIENT(self):
        obj=Client()
        result =1
        errorStyle = "border:1px solid rgb(255,0,0);"
        if not self.ui.client_fname.text():
            self.ui.client_fname.setStyleSheet(errorStyle)
            result =0 
        else:
            obj.FirstName=self.ui.client_fname.text()

            #--------------------------
        if not self.ui.client_lname.text():
            self.ui.client_lname.setStyleSheet(errorStyle)
            result =0 
        else:
            obj.LastName=self.ui.client_lname.text()

        if not self.ui.client_email.text():
            self.ui.client_email.setStyleSheet(errorStyle)
            result =0 
        else:
            obj.Email=self.ui.client_email.text()

        if not self.ui.client_address.text():
            self.ui.client_address.setStyleSheet(errorStyle)
            result =0 
        else:
            obj.Address1=self.ui.client_address.text()
    
        #obj.Country=self.ui.clientco.text()
        #obj.Region=self.ui.region_bar.text()
        obj.Town=self.ui.client_town.text()   
        obj.TelHome=self.ui.client_wcontact.text()     
        obj.PostCodeZIP=self.ui.client_zipcode.text()       
        obj.CellMobile=self.ui.client_hcontact.text()     
       # obj.Archived=bool(self.ui.clientma.text())
        obj.Mailings=bool(self.ui.client_amailing_check.text())
        #----------------------------------------------------------------
        if not self.ui.pet_name.text():
            self.ui.pet_name.setStyleSheet(errorStyle)
            result =0 
        else:
            obj.AnimalName=self.ui.pet_name.text()

        if not self.ui.pet_breed.text():
            self.ui.pet_breed.setStyleSheet(errorStyle)
            result =0 
        else:
            obj.Breed=self.ui.pet_breed.text()

        obj.Sex=self.ui.comboBox.currentText()
        print(obj.Sex)
        obj.Food1Amount=self.ui.pet_food_amount.text()
        obj.Food1Type=self.ui.pet_food_type.text()
        obj.Age=self.ui.pet_age.text()
        obj.ShareKennel=self.ui.pet_kennel_unit.text()
        obj.MedicalConditions=self.ui.pet_medical_details.text()
        obj.DiscountA=self.ui.pet_discount.text()
        obj.Food1Freq=self.ui.pet_food_frequency.text()

        #-------------------------------------------------------
        if not self.ui.vet_pname.text():
            self.ui.vet_pname.setStyleSheet(errorStyle)
            result =0 
        else:
            obj.PracticeName=self.ui.vet_pname.text()

        if not self.ui.vet_vname.text():
            self.ui.vet_vname.setStyleSheet(errorStyle)
            result =0 
        else:
            obj.VetName=self.ui.vet_vname.text()

    
        obj.ContactNo=self.ui.vet_contact.text()     
        obj.Address1Vet=self.ui.vet_address.text()   
        obj.TownVet=self.ui.vet_town.text() 

        
        
        
          #clienttada address var?
                 #clientda da town var iki tane town oluyor?
    
        
        
        if(result ==1):
            print(obj.FirstName)
            object=Database_Class()
            client_row=(obj.LastName, obj.FirstName, '?', obj.Address1, '?', '?', '?', obj.PostCodeZIP, '?', obj.Email, obj.TelHome, '?', obj.CellMobile, 1, 1, '?', obj.Mailings, '?', '?', '?', '?', False, 2.0, obj.Town)
            animal_row = (obj.AnimalName, 2, obj.Breed, obj.Sex, False, True, obj.ShareKennel, obj.MedicalConditions, 'AnimalNotes', obj.Food1Type, obj.Food1Freq, obj.Food1Amount, True, obj.Age, '', '', '', '', '', 0, '', '', '', '', '', 0, 0, '', '')
            vet_row=(obj.PracticeName, obj.VetName, obj.ContactNo, obj.Address1Vet,'' ,obj.TownVet, '', '','')
            print(client_row,animal_row,vet_row)
            object.setNewClient(client_row, animal_row, vet_row)
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


