from DATABASE_SETTINGS import SERVER, DATABASE

class Client:
	def _init_(LastName, FirstName, Title, Adress1, Adress2, Adress3,
				Region, PostCodeZIP, Country, Email, TelHome, TelWork,
				CellMobile, Discount, VetSugeryID,Clientnotes,ClientID,
				Mailings, WebContact, ClientIdent, Referred, PartnerName,
				Archived, AccountBalance, Town):

		self.LastName = LastName
		self.FirstName = FirstName
		self.Title = Title
		self.Adress1 = Adress1
		self.Adress2 = Adress2
		self.Adress3 = Adress3
		self.Region = Region
		self.PostCodeZIP = PostCodeZIP
		self.Country = Country
		self.Email = Email
		self.TelHome = TelHome
		self.TelWork = TelWork
		self.CellMobile = CellMobile
		self.Discount = Discount
		self.VetSugeryID = VetSugeryID
		self.Clientnotes = Clientnotes
		self.ClientID = ClientID
		self.Mailings = Mailings
		self.WebContact = WebContact
		self.ClientIdent = ClientIdent
		self.Referred = Referred
		self.PartnerName = PartnerName
		self.Archived = Archived
		self.AccountBalance = AccountBalance
		self.Town = Town

		self.AnimalName = AnimalName
		self.Breed = Breed
		self.Sex = Sex
		self.Food1Amount = Food1Amount
		self.Food1Type = Food1Type
		self.Age = Age
		self.ShareKennel = ShareKennel
		self.MedicalConditions = MedicalConditions
		self.DiscountA = DiscountA
		self.Food1Freq = Food1Freq

		self.PracticeName = PracticeName
		self.VetName = VetName
		self.ContactNo = ContactNo
		self.Address1Vet = Address1Vet
		self.TownVet = TownVet

	def getFirstName(self):
		self.FirstName = input()

	def getLastName(self):
		self.LastName = input()

	def getTitle(self):
		self.Title = input()

	def getAdress1(self):
		self.Adress1 = input()

	def getAdress2(self):
		self.Adress2 = input()

	def getAdress3(self):
		self.Adress3 = input()

	def getRegion(self):
		self.Region = input()

	def getPostCodeZIP(self):
		self.PostCodeZIP = input()

	def getCountry(self):
		self.Country = input()

	def getEmail(self):
		self.Email = input()

	def getTelHome(self):
		self.TelHome = input()

	def getCellMobile(self):
		self.CellMobile = input()

	def getDiscount(self):
		self.Discount = input()

	def getVetSugeryID(self):
		self.VetSugeryID = input()

	def getClientnotes(self):
		self.Clientnotes = input()

	def getClientID(self):
		self.ClientID = input()

	def getMailings(self):
		self.Mailings = input()

	def getWebContact(self):
		self.WebContact = input()

	def getClientIdent(self):
		self.ClientIdent = input()

	def getReferred(self):
		self.Referred = input()

	def getArchived(self):
		self.Archived = input()

	def getAccountBalance(self):
		self.AccountBalance = input()

	def getTown(self):
		self.Town = input()
