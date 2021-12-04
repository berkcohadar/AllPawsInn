#MAKE COMMENT PURPOSE OF THIS MODULE:
import pyodbc
import sys
from DATABASE_SETTINGS import SERVER, DATABASE
conn=pyodbc.connect('Driver={SQL Server};'
                      'Server='+SERVER+';'
                      'Database='+DATABASE+';'
                      'Trusted_Connection=yes;')

class Database_Class(object):


    def getByClientID(self,table_name,row_number,Client_ID):
        
        if(table_name=='dbo.AmountSpent'):
            print('Will discuss')
        elif(table_name=='dbo.Animals'):
            cursor = conn.cursor()
            query="""SELECT * FROM dbo.Animals WHERE ClientID='%d' ORDER BY AnimalName"""%(int(Client_ID))
            results=cursor.execute(query)
            return results
        elif(table_name=='dbo.ClientDetails'):
            cursor = conn.cursor()
            query="""SELECT * FROM dbo.ClientDetails WHERE ClientID='%d'"""%(int(Client_ID))
            row=cursor.execute(query)
            result = row.fetchone()
            return result
        elif(table_name=='dbo.Payments'):
            cursor = conn.cursor()
            query="""DECLARE @n int='%d' SELECT TOP (@n) * FROM dbo.Payments WHERE ClientID='%d' ORDER BY PaymentDate"""%(int(row_number),int(Client_ID))
            results=cursor.execute(query)
            return results
        else:
            return {-1}

    def setNewClient(self,row,animalrow,vetrow):
        cursor = conn.cursor()
        query="""INSERT INTO ClientDetails (LastName,FirstName,Title,Address1,Address2,Address3,Region,PostcodeZip,Country,Email,TelHome,TelWork,CellMobile,Discount,VetSurgeryID,ClientNotes,Mailings,WebContact,ClientIdent,Referred,PartnerName,Archived,AccountBalance,Town) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%s','%s','%s','%s','%s','%s','%s','%f','%s')"""%(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],int(row[13]),int(row[14]),row[15],row[16],row[17],row[18],row[19],row[20],row[21],float(row[22]),row[23])
        cursor.execute(query)
        conn.commit()
        query2="""SELECT TOP (1) [ClientID] FROM [ClientDetails] ORDER BY ClientID DESC"""
        row=cursor.execute(query2)
        result1=row.fetchone()
        query="""INSERT INTO Animals (ClientID,AnimalName,TypeID,Breed,Sex,NeuteredSpayed,Bites,ShareKennel,MedicalConditions,AnimalNotes,Food1Type,Food1Freq,Food1Amount,FoodChews,Age,DateOfBirth,FoodNotes,Image,Size,TagRef,Food2Type,Food2Freq,Food2Amount,Food1TypeName,Food2TypeName,AnimalType,DailyCharge,DayCareCharge,Archived,Colour) VALUES ('%d','%s','%d','%s','%s','%s','%s','%s','%s','%s','%d','%s','%s','%s','%d','%s','%s','%s','%s','%s','%d','%s','%s','%s','%s','%s','%f','%f','%s','%s')"""%(int(result1[0]),animalrow[0],int(animalrow[1]),animalrow[2],animalrow[3],animalrow[4],animalrow[5],animalrow[6],animalrow[7],animalrow[8],int(animalrow[9]),animalrow[10],animalrow[11],animalrow[12],int(animalrow[13]),animalrow[14],animalrow[15],animalrow[16],animalrow[17],animalrow[18],int(animalrow[19]),animalrow[20],animalrow[21],animalrow[22],animalrow[23],animalrow[24],float(animalrow[25]),float(animalrow[26]),animalrow[27],animalrow[28])
        cursor.execute(query)
        conn.commit()
        query="""INSERT INTO VetDetails (PracticeName,VetName,ContactNo,Address1,Address2,Town,PostcodeZIP,Email,AddRegion) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"""%(vetrow[0],vetrow[1],vetrow[2],vetrow[3],vetrow[4],vetrow[5],vetrow[6],vetrow[7],vetrow[8])
        cursor.execute(query)
        conn.commit()
        print(result1[0])
        return True
    def DirectCheckInDB(self ,row):
        cursor = conn.cursor()
        query="""Update BookingObjects SET Status='%s' Where BookingID ='%d'"""%(row[1],int(row[0])) 
        cursor.execute(query)
        conn.commit()

    def SetNewDaycare(self,row):
        cursor = conn.cursor()
        query="""INSERT INTO BookingObjects (AnimalID,KennelID,DateIn,DateOut,Status,Shared,NoDays,BoardingRate,PeakPeriodSurcharge,Notes,CollectionDayDiscount,TaskCharges,DayCare,DayCareRate,HalfDayDiscount,ExtendedStayPeriod,ExtendedStayDiscount,SharedKennelSlot,BookingCharge,Discount,Linked,LinkedBookingDiscount,EmergencyContactNo,StaffCode,EditDate,UnitTypeSurcharge,MiscSurcharge,PeakPeriodSurRate,Days,TotalToPay,TodayDate,CheckDateIn,CheckDateOut) VALUES ('%d','%d','%s','%s','%s','%s','%f','%f','%f','%s','%f','%f','%s','%f','%f','%d','%f','%d','%f','%f','%s','%f','%s','%s','%s','%f','%f','%f','%s','%f','%s','%s','%s')"""%(int(row[0]),int(row[1]),row[2],row[3],row[4],row[5],float(row[6]),float(row[7]),float(row[8]),row[9],float(row[10]),float(row[11]),row[12],float(row[13]),float(row[14]),int(row[15]),float(row[16]),int(row[17]),float(row[18]),float(row[19]),row[20],float(row[21]),row[22],row[23],row[24],float(row[25]),float(row[26]),float(row[27]),row[28],float(row[29]),row[30],row[31],row[32])
        cursor.execute(query)
        conn.commit()

    def GetDaycareBetweenDates(self,row):
        cursor = conn.cursor()
        query="""SELECT * FROM BookingObjects WHERE DateIn>='%s' AND DateOut<='%s'"""%(row[0],row[1])
        results=cursor.execute(query)
        return results

    #gets owner and dog name for current date
    def GetDaycareForCurrentDate(self,row):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, Animals.AnimalName
                     FROM ClientDetails,Animals,BookingObjects 
                        WHERE BookingObjects.AnimalID=Animals.AnimalID 
                            AND Animals.ClientID=ClientDetails.ClientID 
                                AND BookingObjects.DateIn>='%s' AND BookingObjects.DateOut>='%s'"""%(row[0],row[1])
        results=cursor.execute(query)
        return results
    def GetInfoForSearch(self):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, Animals.AnimalName, Animals.AnimalID, BookingObjects.Status, BookingObjects.BookingID
                     FROM ClientDetails,Animals,BookingObjects 
                     WHERE Animals.ClientID=ClientDetails.ClientID and BookingObjects.AnimalID = Animals.AnimalID"""
        results=cursor.execute(query)
        return results


    def GetClientAccountBalance(self,ClientID):
        cursor = conn.cursor()
        query="""SELECT AccountBalance FROM ClientDetails WHERE ClientID='%d'"""%(int(ClientID))
        row=cursor.execute(query)
        result = row.fetchone()
        return result

    def SetClientAccountBalance(self,ClientID,NewBalance):
        cursor = conn.cursor()
        query="""UPDATE ClientDetails SET AccountBalance='%2f' WHERE ClientiD='%d'"""%(float(NewBalance),int(ClientID))
        cursor.execute(query)
        conn.commit()

    def GetBookingStatusbyAnimalID(self,AnimalID,row):
        cursor = conn.cursor()
        query="""SELECT Status FROM BookingObjects WHERE AnimalID='%d' AND DateIn>='%s' AND DateOut<='%s'"""%(int(AnimalID),row[0],row[1])
        results=cursor.execute(query)
        return results.fetchone()

    def GetBookingStatusbyBookingID(self,BookingID):
        cursor = conn.cursor()
        query="""SELECT Status FROM BookingObjects WHERE BookingID='%d'"""%(int(BookingID))
        results=cursor.execute(query)
        return results.fetchone()

    def SetBookingStatusbyAnimalID(self,AnimalID,row,NewStatus):
        cursor = conn.cursor()
        query="""UPDATE BookingObjects SET Status='%s' WHERE AnimalID='%d' AND DateIn>='%s' AND DateOut<='%s'"""%(NewStatus,int(AnimalID),row[0],row[1])
        cursor.execute(query)
        conn.commit()

    def SetBookingStatusbyBookingID(self,BookingID,NewStatus):
        cursor = conn.cursor()
        query="""UPDATE BookingObjects SET Status='%s' WHERE BookingID='%d'"""%(NewStatus,int(BookingID))
        cursor.execute(query)
        conn.commit()

    def GetAllPaymentsbyClientID(self,ClientID):
        cursor = conn.cursor()
        query="""SELECT * FROM Payments WHERE ClientID='%d'"""%(int(ClientID))
        results=cursor.execute(query)
        return results

    def GetAllPaymentsbyClientIDBetweenDates(self,ClientID,row):
        cursor = conn.cursor()
        query="""SELECT * FROM Payments WHERE ClientID='%d' AND DateIn>='%s' AND DateOut<='%s'"""%(int(ClientID),row[0],row[1])
        results=cursor.execute(query)
        return results

    #--------------- RESERVARTION FUCNTIONS START-------------------

    def SearchForReservation(self):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, Animals.AnimalName, Animals.AnimalID
                     FROM ClientDetails,Animals 
                     WHERE Animals.ClientID=ClientDetails.ClientID"""
        results=cursor.execute(query)
        return results
    def SearchForClientPet(self,id):
        cursor = conn.cursor()
        query="""SELECT  Animals.AnimalID
                     FROM ClientDetails,Animals 
                     WHERE Animals.ClientID=ClientDetails.ClientID and ClientDetails.ClientID='%d'"""%(int(id))
        results=cursor.execute(query)
        return results

    def SubmitReservation(self, row):
        cursor = conn.cursor()
        query="""INSERT INTO BookingObjects (AnimalID,KennelID,Status,EditDate) VALUES ('%d','%d','%s','%s')"""%(int(row[0]),int(row[1]),row[2],row[3])
        cursor.execute(query)
        conn.commit()

    def GetReservations(self,today,tommrw):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, Animals.AnimalName, Animals.AnimalID, BookingObjects.Status, BookingObjects.BookingID, BookingObjects.EditDate
                     FROM ClientDetails,Animals,BookingObjects 
                     WHERE Animals.ClientID=ClientDetails.ClientID and BookingObjects.AnimalID = Animals.AnimalID  and BookingObjects.Status = 'Reserved' and BookingObjects.EditDate >='%s' and BookingObjects.EditDate <'%s' """%(today,tommrw)
        results=cursor.execute(query)
        return results


     
    #---------------RESERVATION FUNCTIONS END-----------------------


    #---------------PAYMENT FUCNTIONS START-------------------

    def SearchForPayment(self):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, Animals.AnimalName, Animals.AnimalID,ClientDetails.ClientID
                     FROM ClientDetails,Animals 
                     WHERE Animals.ClientID=ClientDetails.ClientID"""
        results=cursor.execute(query)
        return results

    def SubmitPayment(self, row):
        cursor = conn.cursor()
        query="""INSERT INTO BookingObjects (AnimalID,KennelID,Status,EditDate) VALUES ('%d','%d','%s','%s')"""%(int(row[0]),int(row[1]),row[2],row[3])
        cursor.execute(query)
        conn.commit()

    def GetPayment(self,today,tommrw):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, Animals.AnimalName, Animals.AnimalID, BookingObjects.Status, BookingObjects.BookingID, BookingObjects.EditDate
                     FROM ClientDetails,Animals,BookingObjects 
                     WHERE Animals.ClientID=ClientDetails.ClientID and BookingObjects.AnimalID = Animals.AnimalID  and BookingObjects.Status = 'Reserved' and BookingObjects.EditDate >='%s' and BookingObjects.EditDate <'%s' """%(today,tommrw)
        results=cursor.execute(query)
        return results

    def GetAnimalInfo(self,id,status="Current"):
        cursor = conn.cursor()
        query="""SELECT  Animals.AnimalName,Animals.Size, Animals.Breed, Animals.animalID
                     FROM Animals
                     WHERE Animals.AnimalID='%d'"""%(id)
        result = cursor.execute(query)
        columns = [column[0] for column in result.description]
        results = []
        for row in result.fetchall():
            results.append(dict(zip(columns, row)))
        
        query = """SELECT BookingObjects.DateIn,BookingObjects.DateOut, BookingObjects.NoDays 
                    FROM BookingObjects 
                    WHERE BookingObjects.AnimalID='%d' AND Status='%s'"""%(id,status)
        result = cursor.execute(query)
        columns = [column[0] for column in result.description]
        results2 = []
        for row in result.fetchall():
            results2.append(dict(zip(columns, row)))

        print("1", results)
        print("2", results2)
        if len(results2) == 0 :
            results2.append({"DateIn":"Never","DateOut":"Never","NoDays":0})
        print("updated", results2)

        for i in range(len(results)):
            results[i]["DateIn"] = results2[i]["DateIn"]
            results[i]["DateOut"] = results2[i]["DateOut"]
            results[i]["NoDays"] = results2[i]["NoDays"]
        print(results)
        #reservation da bu kisim degsitirilcek
        # WHERE BookingObjects.AnimalID = Animals.AnimalID  and BookingObjects.Status = 'Reserved' and BookingObjects.EditDate >='%s' and BookingObjects.EditDate <'%s' """%(today,tommrw)
        return results

    def GetClientInfo(self,id):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, ClientDetails.Address1, ClientDetails.CellMobile, ClientDetails.Email, ClientDetails.AccountBalance,ClientDetails.Town,ClientDetails.PostcodeZIP
                     FROM ClientDetails
                     WHERE ClientDetails.ClientID='%d' """%(id)
        result=cursor.execute(query)
        columns = [column[0] for column in result.description]
        results = []
        for row in result.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def DecreaseAccountBalance(self,id,num): 
        currentbalance=0
        cursor = conn.cursor()
        prew ="""SELECT ClientDetails.AccountBalance
                    FROM ClientDetails
                    WHERE ClientDetails.ClientID='%d' """%(id)
        results=cursor.execute(prew)
        for item in results:
            currentbalance= item[0]
            print("curbalance "+str(currentbalance))
        newbalance =   float(currentbalance)-num 
        print("newbalance "+str(newbalance))
        query="""UPDATE ClientDetails SET AccountBalance='%2f' WHERE ClientID='%d'"""%(newbalance,int(id))
        cursor.execute(query)
        conn.commit()
        domates=2
        print(domates)
          
    #---------------PAYMENT FUNCTIONS END-----------------------

  #---------------ADDITIONAL PET FUNCTIONS STARTS-----------------------

    def DeleteAnimal(self,id):
        cursor = conn.cursor()
        query="""DELETE from Animals  WHERE AnimalID='%d'"""%(int(id))
        cursor.execute(query)
        conn.commit()
    def CreateAnimal(self,clientid,animalrow):
        cursor = conn.cursor()
        query="""INSERT INTO Animals (ClientID,AnimalName,TypeID,Breed,Sex,MedicalConditions,Food1Type,Food1Freq,Food1Amount,Age) VALUES ('%d','%s','%d','%s','%s','%s','%d','%s','%s','%d')"""%(int(clientid),animalrow[0],1,animalrow[1],animalrow[2],animalrow[3],int(animalrow[4]),animalrow[5],animalrow[6],int(animalrow[7]))
        cursor.execute(query)
        conn.commit()
  #---------------ADDITIONAL PET FUNCTIONS END-----------------------



  
    #---------------SERVICE FUNCTIONS STARTS-----------------------
    def addServicesDetails(self,dayCareRate, nails, food, hair, otherGoods, subTotal, discount, paymentType, Client_ID, tax):
        cursor = conn.cursor()

        query="""SELECT TOP (1) [serviceID] FROM [ServicesDetails] ORDER BY serviceID DESC"""
        row=cursor.execute(query)
        serviceID=row.fetchone()
        if (serviceID) :
            serviceID = serviceID[0] + 1
        else:
            serviceID = 0

        query="""INSERT INTO ServicesDetails (dayCareRate, nails, food, hair, otherGoods, subTotal, discount, paymentType, customerID, tax, serviceID) VALUES ('%d','%d','%d','%d','%d','%d','%d','%s','%d','%d','%d')"""%(dayCareRate,nails,food,hair,otherGoods,subTotal,discount,paymentType,Client_ID,tax,serviceID)
        row=cursor.execute(query)

        query="""SELECT TOP (1) [AccountBalance] FROM [ClientDetails] WHERE ClientiD='%d'"""%(int(Client_ID))
        row=cursor.execute(query)
        result2=row.fetchone()

        if (result2) :
            oldBalance = result2[0]
        else:
            oldBalance = 0.0

        NewBalance = float(oldBalance) + float(subTotal)

        query="""UPDATE ClientDetails SET AccountBalance='%2f' WHERE ClientiD='%d'"""%(float(NewBalance),int(Client_ID))
        cursor.execute(query)
        conn.commit()

        return int(serviceID)

    def removeServicesDetails(self, serviceID, Client_ID, subTotal):
        cursor = conn.cursor()
        query="""DELETE FROM ServicesDetails WHERE serviceID='%d' """%(int(serviceID))
        cursor.execute(query)

        query="""SELECT TOP (1) [AccountBalance] FROM [ClientDetails] WHERE ClientiD='%d'"""%(int(Client_ID))
        row=cursor.execute(query)
        result2=row.fetchone()

        if (result2) :
            oldBalance = result2[0]
        else:
            oldBalance = 0.0

        NewBalance = float(oldBalance) - float(subTotal)
        query="""UPDATE ClientDetails SET AccountBalance='%2f' WHERE ClientiD='%d'"""%(float(NewBalance),int(Client_ID))
        cursor.execute(query)
        conn.commit()
    #---------------SERVICE FUNCTIONS STARTS-----------------------

    def GetDayCareRateAndTax(self, id):
        cursor = conn.cursor()
        query="""SELECT AdminSetting.DayCareRate , AdminSetting.Tax
                     FROM AdminSetting
                     WHERE AdminSetting.IsActive='%d' """%(1)
        results=cursor.execute(query)
        return results
    def IncreaseClientBalance(self,id,num):
        currentbalance=0
        cursor = conn.cursor()
        prew ="""SELECT ClientDetails.AccountBalance
                     FROM ClientDetails
                     WHERE ClientDetails.ClientID='%d' """%(id)
        results=cursor.execute(prew)
        for item in results:
            currentbalance= item[0]
            print("curbalance "+str(currentbalance))
        newbalance = num +  float(currentbalance)
        print("newbalance "+str(newbalance))
        query="""UPDATE ClientDetails SET AccountBalance='%2f' WHERE ClientID='%d'"""%(float(newbalance),int(id))
        cursor.execute(query)
        conn.commit()
    def GetAccountBalance(id):
        cursor = conn.cursor()
        prew ="""SELECT ClientDetails.AccountBalance,ClientDetails.ClientID
                     FROM ClientDetails
                     WHERE ClientDetails.ClientID='%d' """%(id)
        results=cursor.execute(prew)
        return results
    def GetServicesFees(self,name):
        cursor = conn.cursor()
        query="""SELECT Services.Cost
                     FROM Services
                     WHERE Services.ServiceName='%s' """%(name)
        results=cursor.execute(query)
        return results

    def ChangeAccountBalance(self,id,num):
        cursor = conn.cursor()
        query="""UPDATE ClientDetails SET AccountBalance='%2f' WHERE ClientID='%d'"""%(float(num),int(id))
        cursor.execute(query)
        conn.commit()
    def EditClient(self,email,address,town,zipcode,contact1,contact2,id):
        cursor = conn.cursor()
        query="""UPDATE ClientDetails SET Email='%s',Address1='%s',Town='%s',PostcodeZIP='%s',CellMobile='%s',TelHome='%s' WHERE ClientID='%d'"""%(email,address,town,zipcode,contact1,contact2,int(id))
        cursor.execute(query)
        conn.commit()

    def GetServices(self):
        cursor = conn.cursor()
        query="""SELECT Services.ServiceName, Services.Cost
                     FROM Services
                     """
        results=cursor.execute(query)
        return results
    def ChangeServiceCost(self,cost,name):
        cursor = conn.cursor()
        query="""UPDATE Services SET Cost='%f' WHERE ServiceName='%s'"""%(cost,name)
        cursor.execute(query)
        conn.commit()
    def AddService(self,name,cost):
        cursor = conn.cursor()
        query="""INSERT INTO Services (Name,Cost) VALUES ('%s','%d')"""%(name,cost)
        cursor.execute(query)
        conn.commit()
   


    #---------------SERVICE FUNCTIONS END-----------------------


    #---------------HOME PAGE  FUNCTIONS STARTS-----------------------
    def GetCheckedIn(self,today,tommrw):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, Animals.AnimalName, Animals.AnimalID, BookingObjects.Status, BookingObjects.BookingID, BookingObjects.EditDate,ClientDetails.ClientID
                        FROM ClientDetails,Animals,BookingObjects 
                        WHERE Animals.ClientID=ClientDetails.ClientID and BookingObjects.AnimalID = Animals.AnimalID  and BookingObjects.Status = 'CheckedIn' and BookingObjects.EditDate >='%s' and BookingObjects.EditDate <'%s' """%(today,tommrw)
        results=cursor.execute(query)
        return results


    
    def GetCheckedOut(self,today,tommrw):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, Animals.AnimalName, Animals.AnimalID, BookingObjects.Status, BookingObjects.BookingID, BookingObjects.EditDate
                        FROM ClientDetails,Animals,BookingObjects 
                        WHERE Animals.ClientID=ClientDetails.ClientID and BookingObjects.AnimalID = Animals.AnimalID  and BookingObjects.Status = 'CheckedOut' and BookingObjects.EditDate >='%s' and BookingObjects.EditDate <'%s' """%(today,tommrw)
        results=cursor.execute(query)
        return results


        #---------------HOME PAGE FUNCTIONS END-----------------------

            #---------------ADMIN PAGE  FUNCTIONS STARTS-----------------------

    def GetAdminList(self):
        cursor = conn.cursor()
        query=""" SELECT AdminSetting.ProfileName,AdminSetting.DayCareRate, AdminSetting.Tax, AdminSetting.Discount, AdminSetting.IsActive,AdminSetting.BookingRate
                        FROM AdminSetting """
        results=cursor.execute(query)
        return results

    def GetAdminListWithID(self):
        cursor = conn.cursor()
        query=""" SELECT AdminSetting.ProfileName,AdminSetting.DayCareRate, AdminSetting.Tax, AdminSetting.Discount, AdminSetting.IsActive,AdminSetting.BookingRate,AdminSetting.ID
                        FROM AdminSetting """
        results=cursor.execute(query)
        return results

    def SetAdminSetting(self,profilename,daycarerate,tax,discount,IsActive,bookingrate):
        cursor = conn.cursor()
        query="""INSERT INTO AdminSetting (ProfileName,DayCareRate,Tax,Discount,IsActive,BookingRate) VALUES ('%s','%f','%f','%f','%d','%f')"""%(profilename,daycarerate,tax,discount,IsActive,bookingrate)
        cursor.execute(query)
        conn.commit()

    def SetAllInActive(self):
        cursor = conn.cursor()
        query="""UPDATE AdminSetting SET IsActive='%d' WHERE IsActive='%d'"""%(0,1)
        cursor.execute(query)
        conn.commit()
    def SetActive(self,id):
        cursor = conn.cursor()
        query="""UPDATE AdminSetting SET IsActive='%d' WHERE ID='%d'"""%(1,id)
        cursor.execute(query)
        conn.commit()

    def GetActiveProfile(self,id):
        cursor = conn.cursor()
        query=""" SELECT AdminSetting.DayCareRate, AdminSetting.Tax, AdminSetting.Discount, AdminSetting.BookingRate
                        FROM AdminSetting WHERE AdminSetting.IsActive=%d """%(1) 
        results=cursor.execute(query)
        return results

    def DeleteProfile(self,id):
        cursor = conn.cursor()
        query="""DELETE FROM AdminSetting WHERE AdminSetting.ID='%d' """%(id)
        cursor.execute(query)
        conn.commit()
        #---------------ADMIN PAGE FUNCTIONS END-----------------------


if __name__ == "__main__":
    object=Database_Class()
    row_Clientinfo=('LastName','FirstName','Title','Address1','Address2','Address3','Region','PostcodeZIP','Country','Email','TelHome','TelWork','CellMobile','Discount(int)','VetSurgeryID(int)','ClientNotes','Mailings(boolean)','Webcontact','ClientIdent','Referred','PartnerName','Archived(boolean)','Accountbalance(float)','Town')
    row_Animalinfo=('Animalname','TypeID(1(cat) or 2(dog))','Breed','Sex','NeuteredSpayed(boolean)','Bites(boolean)','ShareKennel(boolean)','MedicalConditions','AnimalNotes','Food1Type(int)','Food1Freq','Food1Amount','FoodChews(boolean)','Age(int)','DateOfBirth(2000-07-18 00:00:00.000)','FoodNotes','Image(bos koy)','Size','TagRef','Food2Type(int)','Food2Freq','Food2Amount','Food1TypeName','Food2TypeName','AnimalType','DailyCharge(float)','DayCareCharge(float)','Archived(boolean)','Colour')
    row_Vetinfo=('PracticeName','VetName','ContactNo','Address1','Address2','Town','PostcodeZIP','Email','AddRegion')
    row_set_daycare=('AnimalID','KennelID(1to86 needs a check for occupancy)','DateIn','DateOut','Status(Confirmed basla)','Shared(boolean)','NODays(float)(find by datein-dateout)','BoardingRate(float)','PeakPeriodSurcharge(float)','Notes','CollectionDayDiscount(float)','TaskCharges(float)','DayCare(boolean)','DayCareRate(float)','HalfDayDiscount(float)','ExtendedStayPeriod(int)','ExtendedStayDiscount(float)','SharedKennelSlot(int)','BookingCharge(float)','Discount(float)','Linked(boolean)','LinkedBookingDiscount(float)','EmergincyContactNo','StaffCode','EditDate(date)','UnitTypeSurcharge(float)','MiscSurcharge(float)','PeakPeriodSurRate(float)','Days','TotalToPay(float)','TodayDate','CheckDateIn','CheckDateOut')
    row_get_daycare=('Datein(date)','DateOut(date)')


   # today=datetime.now()  #sadece gunu alir 2020-27-11
    #print(today)
    #print(str(today))
    #print(type(today))

    datet = today.strftime("%Y-%m-%d, %H:%M:%S")
    print(datet)
    row0=('2020-04-24 08:00:00.000','2017-04-25 08:00:00.000')
    result=object.GetDaycareForCurrentDate(row0)
    for i in result or []:
         print(i)
         print("\n")


    row0=('2020-05-21 08:00:00.000','2017-04-25 08:00:00.000')
    #row1=('2017-04-24 08:00:00.000')
    result=object.GetDaycareBetweenDates(row0)
    print(result)
    for i in result or []:
        print(i)
        print("\n")
    wait = input("PRESS ENTER TO CONTINUE.4")


    row1=('2017-04-24 08:00:00.000','2017-04-25 14:00:00.000')
    result=object.GetBookingStatusbyAnimalID(76,row1)
    for i in result or []:
        print(i)
    wait = input("PRESS ENTER TO CONTINUE.4")


 #
 #