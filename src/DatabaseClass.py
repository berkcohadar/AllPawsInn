#MAKE COMMENT PURPOSE OF THIS MODULE:
from numpy import var
import pyodbc
import sys
from DATABASE_SETTINGS import SERVER, DATABASE
from datetime import datetime
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

    def setNewClient(self, client, pet):
        cursor = conn.cursor()
        query="INSERT INTO ClientDetails ("
        query_add = " VALUES ("
        variables = []
        for key in client:
            if (client[key] != ""):
                varType = ""

                if (type(client[key]) == type(1)):
                    varType = "d"

                if (type(client[key]) == type("string")):
                    client[key] = client[key].replace("'","`")
                    varType = "s"

                query += key+","
                query_add += "'%{}'".format(varType)+","
                variables.append(client[key])

        query = query[:-1]
        query_add = query_add[:-1]
        query +=  ")" + query_add + ")"
        query= query%(tuple(variables))
        cursor.execute(query)
        conn.commit()

        query = """SELECT TOP (1) [ClientID] FROM [ClientDetails] ORDER BY ClientID DESC""" # Get the lastly created Client's ID. Client is the one we created above.
        res = cursor.execute(query)
        result = res.fetchone()

        pet["ClientID"] = result[0] # index 0 is the ClientID

        query="INSERT INTO Animals ("
        query_add = " VALUES ("
        variables = []
        for key in pet:
            if (pet[key] != ""):
                varType = ""

                if (type(pet[key]) == type(1)):
                    varType = "d"
                
                if (type(pet[key]) == type(1.1)):
                    varType = "2f"

                if (type(pet[key]) == type("string")):
                    pet[key] = pet[key].replace("'","`")
                    varType = "s"

                query += key+","
                query_add += "'%{}'".format(varType)+","
                variables.append(pet[key])

        query = query[:-1]
        query_add = query_add[:-1]
        query +=  ")" + query_add + ")"
        query= query%(tuple(variables))
        cursor.execute(query)
        conn.commit()

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

    def SetBookingStatusbyBookingID(self,BookingID,Date):
        cursor = conn.cursor()
        if 'DateIn' in Date:
            query="""UPDATE ServicesDetails SET checkedIn='%d', dateIn='%s' WHERE serviceID='%d'"""%(1,Date['DateIn'].toString("yyyy-MM-dd"),int(BookingID))
        elif 'DateOut' in Date:
            dateIn = self.getSingleServicesDetails(BookingID)[0]['dateIn']
            dateOut =  datetime.strptime(Date['DateOut'].toString("yyyy-MM-dd"), '%Y-%m-%d')
            days = dateOut - dateIn # calculate daysIn
            days = days.days + 1 
            print(days)
            query="""UPDATE ServicesDetails SET checkedOut='%d', dateOut='%s', daysIn='%d' WHERE serviceID='%d'"""%(1,Date['DateOut'].toString("yyyy-MM-dd"),days,int(BookingID))

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
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, Animals.AnimalName, Animals.AnimalID, ClientDetails.ClientID
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

    def submitReservation(self, Client_ID, animalID, resStartDate, resEndDate, days):
        cursor = conn.cursor()

        query="""SELECT TOP (1) [serviceID] FROM [ServicesDetails] ORDER BY serviceID DESC"""
        row=cursor.execute(query)
        serviceID=row.fetchone()
        if (serviceID) :
            serviceID = serviceID[0] + 1
        else:
            serviceID = 1

        query="""INSERT INTO ServicesDetails (dayCareRate, nails, food, hair, otherGoods, subTotal, discount, tax, customerID, resStartDate, resEndDate, serviceID, animalID, daysIn, checkedIn, checkedOut, completed) VALUES ('%2f','%2f','%2f','%2f','%2f','%2f','%2f','%2f','%d','%s','%s','%d','%d','%d','%d','%d','%d')"""%(0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, Client_ID, resStartDate, resEndDate, serviceID, animalID, days, 0, 0, 0)
        row=cursor.execute(query)
        conn.commit()

        return int(serviceID)

    def GetReservations(self,today, checkedIn, checkedOut):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, Animals.AnimalName, Animals.AnimalID, ServicesDetails.serviceID, ClientDetails.ClientID, ServicesDetails.resStartDate, ServicesDetails.dateIn, ServicesDetails.dateOut
                     FROM ClientDetails,Animals,ServicesDetails 
                     WHERE Animals.ClientID=ClientDetails.ClientID 
                      AND ServicesDetails.animalID = Animals.AnimalID
                      AND ServicesDetails.checkedIn = '%d'
                      AND ServicesDetails.checkedOut = '%d'
                      AND ServicesDetails.completed = '%d'
                      AND ServicesDetails.resStartDate <='%s' 
                      AND ServicesDetails.resEndDate >='%s' """%(checkedIn,checkedOut,0,today,today)
        results=cursor.execute(query)
        return results

    def GetReservationsNoDate(self, checkedIn, checkedOut):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName, ClientDetails.LastName, Animals.AnimalName, Animals.AnimalID, ServicesDetails.serviceID, ClientDetails.ClientID, ServicesDetails.resStartDate, ServicesDetails.dateIn, ServicesDetails.dateOut
                     FROM ClientDetails,Animals,ServicesDetails 
                     WHERE Animals.ClientID=ClientDetails.ClientID 
                      AND ServicesDetails.animalID = Animals.AnimalID
                      AND ServicesDetails.checkedIn = '%d'
                      AND ServicesDetails.checkedOut = '%d'
                      AND ServicesDetails.completed = '%d'
                       """%(checkedIn,checkedOut,0)
        results=cursor.execute(query)
        return results

    def GetReservationByDate(self,today, tomorrow):
        cursor = conn.cursor()
        query="""SELECT ClientDetails.FirstName,
        ClientDetails.LastName,
        Animals.AnimalName,
        Animals.AnimalID,
        ServicesDetails.serviceID,
        ClientDetails.ClientID 
        FROM ClientDetails,Animals,ServicesDetails 
        WHERE Animals.ClientID = ClientDetails.ClientID 
        AND ServicesDetails.animalID = Animals.AnimalID 
        AND ServicesDetails.checkedIn = '%d' 
        AND ServicesDetails.checkedOut = '%d' 
        AND ServicesDetails.resStartDate <='%s' 
        AND ServicesDetails.resEndDate >='%s' """%(0,0,today,today)
        results=cursor.execute(query)
        return results

    def findAllReservations(self, animalID, clientID):
        cursor = conn.cursor()
        query="""SELECT ServicesDetails.subTotal, ServicesDetails.dateIn, ServicesDetails.dateOut, ServicesDetails.serviceID, ServicesDetails.resStartDate, ServicesDetails.resEndDate, ServicesDetails.checkedIn, ServicesDetails.checkedOut, ServicesDetails.completed 
                     FROM ServicesDetails
                     WHERE ServicesDetails.animalID='%d' AND ServicesDetails.customerID='%d' ORDER BY resEndDate DESC"""%(animalID,clientID)
        result = cursor.execute(query)
        columns = [column[0] for column in result.description]
        results = []
        for row in result.fetchall():
            results.append(dict(zip(columns, row)))

        return results  
   
    def createPayment(self, customerId, paymentAmount, paymentDate, paymentType, serviceID):
        cursor = conn.cursor()
        query="""INSERT INTO Payments 
                    (PaymentDate,ClientID,AmountReceived,PaymentType) 
                    VALUES ('%s','%d','%2f','%s')"""%(paymentDate, customerId, paymentAmount,  paymentType)
        
        if (serviceID):
            query="""INSERT INTO Payments 
                    (BookingID,PaymentDate,ClientID,AmountReceived,PaymentType) 
                    VALUES ('%d','%s','%d','%2f','%s')"""%(serviceID, paymentDate, customerId, paymentAmount,  paymentType)

        cursor.execute(query)
        conn.commit()

        currentBalance = float(Database_Class.GetClientAccountBalance(self, ClientID=customerId)[0])
        newBalance = currentBalance-paymentAmount
        Database_Class.SetClientAccountBalance(self, ClientID=customerId,NewBalance=newBalance)

        query="""SELECT TOP (1) [PaymentId] FROM [Payments] ORDER BY PaymentId DESC"""
        row=cursor.execute(query)
        paymentID=row.fetchone()
        return paymentID[0]

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

    def GetAnimalInfo(self,id,status=''):
        cursor = conn.cursor()
        query="""SELECT 
                    Animals.AnimalName
                    ,Animals.Size
                    ,Animals.Breed
                    ,Animals.animalID
                    ,Animals.TypeID
                    ,Animals.Sex
                    ,Animals.NeuteredSpayed
                    ,Animals.MedicalConditions
                    ,Animals.AnimalNotes
                    ,Animals.Age
                    ,Animals.DateOfBirth
                    ,Animals.FoodNotes
                    ,Animals.AnimalType
                    ,Animals.Vaccinated
                    ,Animals.Weight
                    ,Animals.MicrochipID
                    ,Animals.Deceased
                    ,Animals.AnimalVet
                     FROM Animals
                     WHERE Animals.AnimalID='%d'"""%(id)
  
        result = cursor.execute(query)
        columns = [column[0] for column in result.description]
        results = []
        for row in result.fetchall():
            results.append(dict(zip(columns, row)))
            
        # if (status!=''):
        #     query = """SELECT BookingObjects.DateIn,BookingObjects.DateOut, BookingObjects.NoDays 
        #             FROM BookingObjects 
        #             WHERE BookingObjects.AnimalID='%d' AND Status='%s'
        #             ORDER BY BookingObjects.DateIn DESC """%(id,status)
        # else :
        #     query = """SELECT BookingObjects.DateIn,BookingObjects.DateOut, BookingObjects.NoDays 
        #             FROM BookingObjects 
        #             WHERE BookingObjects.AnimalID='%d'
        #             ORDER BY BookingObjects.DateIn DESC """%(id)
        # result = cursor.execute(query)
        # columns = [column[0] for column in result.description]
        # results2 = []
        # for row in result.fetchall():
        #     results2.append(dict(zip(columns, row)))

        # if len(results2) == 0 :
        #     results2.append({"DateIn":"Never","DateOut":"Never","NoDays":0})

        # for i in range(len(results)):
        #     results[i]["DateIn"] = results2[i]["DateIn"]
        #     results[i]["DateOut"] = results2[i]["DateOut"]
        #     results[i]["NoDays"] = results2[i]["NoDays"]

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
    
    def GetPaymentsbyClient(self,clientID):
        cursor = conn.cursor()
        query="""SELECT Payments.PaymentId, Payments.BookingID, Payments.PaymentDate, Payments.PaymentType, Payments.AmountReceived
                     FROM Payments 
                     WHERE ClientID='%d' """%(clientID)
        result = cursor.execute(query)
        columns = [column[0] for column in result.description]
        results = []
        for row in result.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def GetPaymentsbyService(self,serviceID):
        cursor = conn.cursor()
        query="""SELECT Payments.PaymentId, Payments.BookingID, Payments.PaymentDate, Payments.PaymentType, Payments.AmountReceived
                     FROM Payments 
                     WHERE BookingID='%d' """%(serviceID)
        result = cursor.execute(query)
        columns = [column[0] for column in result.description]
        results = []
        for row in result.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def GetPaymentsbyID(self, paymentID):
        cursor = conn.cursor()
        query="""SELECT Payments.PaymentId, Payments.BookingID, Payments.PaymentDate, Payments.PaymentType, Payments.AmountReceived
                     FROM Payments 
                     WHERE PaymentId='%d' """%(paymentID)
        result = cursor.execute(query)
        columns = [column[0] for column in result.description]
        results = []
        for row in result.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def GetPaymentsbyDateRange(self, customerID, startDate, endDate):
        cursor = conn.cursor()
        query="""SELECT Payments.PaymentId, Payments.BookingID, Payments.PaymentDate, Payments.PaymentType, Payments.AmountReceived
                     FROM Payments 
                     WHERE ClientID='%d' and  Payments.PaymentDate >='%s' and Payments.PaymentDate  <='%s' """%(customerID, startDate, endDate)
        if (customerID == -1): ## No customer is specified
            query="""SELECT Payments.PaymentId, Payments.BookingID, Payments.PaymentDate, Payments.PaymentType, Payments.AmountReceived
                     FROM Payments 
                     WHERE Payments.PaymentDate >='%s' and Payments.PaymentDate  <='%s' """%(startDate, endDate)

        result = cursor.execute(query)
        columns = [column[0] for column in result.description]
        results = []
        for row in result.fetchall():
            results.append(dict(zip(columns, row)))
        return results
          
    #---------------PAYMENT FUNCTIONS END-----------------------

    #---------------ADDITIONAL PET FUNCTIONS STARTS-----------------------

    def DeleteAnimal(self,id):
        cursor = conn.cursor()
        query="""DELETE from Animals  WHERE AnimalID='%d'"""%(int(id))
        cursor.execute(query)
        conn.commit()

    def CreateAnimal(self,row):
        cursor = conn.cursor()
        query="INSERT INTO Animals ("
        query_add = " VALUES ("
        variables = []
        for key in row:
            if (row[key] != "" and key != "AnimalID"):
                varType = ""

                if (type(row[key]) == type(1)):
                    varType = "d"

                if (type(row[key]) == type(1.0)):
                    varType = "2f"

                if (type(row[key]) == type("string")):
                    row[key] = row[key].replace("'","`")
                    varType = "s"

                query += key+","
                query_add += "'%{}'".format(varType)+","
                variables.append(row[key])

        query = query[:-1]
        query_add = query_add[:-1]
        query +=  ")" + query_add + ")"

        query= query%(tuple(variables))
        print(query)
        cursor.execute(query)
        conn.commit()

    def UpdateAnimalDetails(self, row):     
        cursor = conn.cursor()
        query="UPDATE Animals SET "
        variables = []
        for key in row:
            if (row[key] != "" and key != "AnimalID"):
                varType = ""

                if (type(row[key]) == type(1)):
                    varType = "d"

                if (type(row[key]) == type(1.0)):
                    varType = "2f"

                if (type(row[key]) == type("string")):
                    row[key] = row[key].replace("'","`")
                    varType = "s"

                query += key+"='%{}'".format(varType)+","
                variables.append(row[key])
        query = query[:-1]

        query += " WHERE AnimalID='%d'"
        variables.append(row["AnimalID"])

        query= query%(tuple(variables))
        cursor.execute(query)
        conn.commit()

    #---------------ADDITIONAL PET FUNCTIONS END-----------------------



  
    #---------------SERVICE FUNCTIONS STARTS-----------------------
    def addServicesDetails(self,dayCareRate, nails, food, hair, otherGoods, subTotal, discount, Client_ID, animalID, tax, dateIn, dateOut, resStartDate, resEndDate, daysIn, checkedIn, checkedOut, completed):
        cursor = conn.cursor()

        query="""SELECT TOP (1) [serviceID] FROM [ServicesDetails] ORDER BY serviceID DESC"""
        row=cursor.execute(query)
        serviceID=row.fetchone()
        if (serviceID) :
            serviceID = serviceID[0] + 1
        else:
            serviceID = 1

        query="""INSERT INTO ServicesDetails (dayCareRate, nails, food, hair, otherGoods, subTotal, discount, customerID, tax, dateIn, dateOut, serviceID, animalID, resStartDate, resEndDate, daysIn, checkedIn, checkedOut, completed) VALUES ('%2f','%2f','%2f','%2f','%2f','%2f','%2f','%d','%2f','%s','%s','%d','%d','%s','%s','%d','%d','%d','%d')"""%(dayCareRate,nails,food,hair,otherGoods,subTotal,discount,Client_ID,tax, dateIn, dateOut, serviceID, animalID, resStartDate, resEndDate, daysIn, checkedIn, checkedOut, completed)
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

    def getSingleServicesDetails(self, serviceID):
        cursor = conn.cursor()
        query="""SELECT * FROM ServicesDetails WHERE serviceID='%d' """%(int(serviceID))
        result = cursor.execute(query)
        columns = [column[0] for column in result.description]
        results = []
        for row in result.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def getLastServicesDetails(self, animalID):
        cursor = conn.cursor()
        query="""SELECT TOP (1) * FROM [ServicesDetails] WHERE animalID='%d' AND checkedOut=1 """%(int(animalID))
        result = cursor.execute(query)
        columns = [column[0] for column in result.description]
        results = []
        for row in result.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    
    def updateServicesDetails(self, customerId, serviceID, dayCareRate, nailFee, foodFee, hairFee, othergoods, discount, totalTax, subTotal, completed):
        cursor = conn.cursor()
        query="""UPDATE ServicesDetails 
                SET dayCareRate='%2f', nails='%2f', food='%2f', hair='%2f', otherGoods='%2f', discount='%2f', tax='%2f', subTotal='%2f', completed='%d'
                WHERE serviceID='%d' """%(dayCareRate, nailFee, foodFee, hairFee, othergoods, discount, totalTax, subTotal, completed, serviceID)
                
        cursor.execute(query)
        conn.commit()

        currentBalance = float(Database_Class.GetClientAccountBalance(self, ClientID=customerId)[0])
        newBalance = currentBalance + float(subTotal)
        Database_Class.SetClientAccountBalance(self, ClientID=customerId,NewBalance=newBalance)

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
    def EditClient(self,name,surname,email,address,town,zipcode,contact1,contact2,id):
        cursor = conn.cursor()
        query="""UPDATE ClientDetails SET FirstName='%s',LastName='%s',Email='%s',Address1='%s',Town='%s',PostcodeZIP='%s',CellMobile='%s',TelHome='%s' WHERE ClientID='%d'"""%(name,surname,email,address,town,zipcode,contact1,contact2,int(id))
        cursor.execute(query)
        conn.commit()

    def GetServices(self, adminProfile):
        cursor = conn.cursor()
        query="""SELECT Services.ServiceName, Services.Cost, Services.ID
                     FROM Services
                     WHERE adminProfile='%d'
                     """%(int(adminProfile))
        results=cursor.execute(query)
        return results

    def ChangeServiceCost(self,cost,serviceID,adminProfile):
        cursor = conn.cursor()
        query="""UPDATE Services SET Cost='%.2f' WHERE ID='%d' AND adminProfile='%d' """%(cost,serviceID,adminProfile)
        cursor.execute(query)
        conn.commit()

    def AddService(self,name,cost,isActive,adminProfile):
        cursor = conn.cursor()
        query="""INSERT INTO Services (ServiceName, Cost, IsActive, adminProfile) VALUES ('%s','%.2f','%d','%d')"""%(name,cost,isActive,adminProfile)
        cursor.execute(query)
        conn.commit()
        
    def DeleteService(self,serviceID):
        cursor = conn.cursor()
        query="""DELETE FROM Services WHERE ID='%d'"""%(serviceID)
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

    def GetAdminListWithID(self):
        cursor = conn.cursor()
        query=""" SELECT AdminSetting.ProfileName,AdminSetting.DayCareRate, AdminSetting.Tax, AdminSetting.IsActive,AdminSetting.ID
                        FROM AdminSetting """
        results=cursor.execute(query)
        return results

    def SetAdminSetting(self,profilename,daycarerate,tax,IsActive):
        if (IsActive):
            Database_Class.SetAllInActive(self)
        cursor = conn.cursor()
        query="""INSERT INTO AdminSetting (ProfileName,DayCareRate,Tax,IsActive) VALUES ('%s','%f','%f','%d')"""%(profilename,daycarerate,tax,IsActive)
        cursor.execute(query)

        query="""SELECT TOP (1) [ID] FROM [AdminSetting] ORDER BY ID DESC"""
        row=cursor.execute(query)
        profileID=row.fetchone()

        conn.commit()
        return profileID[0]



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

    def DeleteProfile(self,id):
        cursor = conn.cursor()

        query="""DELETE FROM AdminSetting WHERE AdminSetting.ID='%d' """%(id)
        cursor.execute(query)

        query="""DELETE FROM Services WHERE adminProfile='%d' """%(id)
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


    today=datetime.now()  #sadece gunu alir 2020-27-11

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