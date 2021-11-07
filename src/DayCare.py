# class for booking objects, services and payment
class DayCare:
	def _init_(self,BookingID, AnimalID, KennelID, DateIn, DateOut, Status,
				Shared, NoDays, BoardingRate, PeakPeriodSurCharge, Notes, CollectionDayDiscount,
				TaskCharges, DayCare, DayCareRate,HalfDayDiscount,ExtendedStayPeriod,
				ExtendedStayDiscount, SharedKennelSlot, BookingCharge, Discount, Linked,
				LinkedBookingAccount, EmergencyContactNo, StaffCode,EditDate, UnitTypeSurcharge, 
				MiscSurcharge, PeakPeriodSurRate, Days, TotalToPay, TodayDate, CheckDateIn,
				CheckDateOut, ServiceName,Cost, PaymentID, otherChargesPaid, TaxPaid,
				TotalChargesPaid, ExtraServices, DayCareRateP, SubTotal, DiscountP, NetBookingCharges,
				PaymentDate, AmountReceived, PaymentType):

		#for booking object
		self.BookingID = BookingID
		self.AnimalID = AnimalID
		self.KennelID = KennelID
		self.DateIn = DateIn
		self.DateOut = DateOut
		self.Status = Status
		self.Shared = Shared
		self.NoDays = NoDays
		self.BoardingRate = BoardingRate
		self.PeakPeriodSurCharge = PeakPeriodSurCharge
		self.Notes = Notes
		self.CollectionDayDiscount = CollectionDayDiscount
		self.TaskCharges = TaskCharges
		self.DayCare = DayCare
		self.DayCareRate = DayCareRate
		self.HalfDayDiscount = HalfDayDiscount
		self.ExtendedStayPeriod = ExtendedStayPeriod
		self.ExtendedStayDiscount = ExtendedStayDiscount
		self.SharedKennelSlot = SharedKennelSlot
		self.BookingCharge = BookingCharge
		self.Discount = Discount
		self.Linked = Linked
		self.LinkedBookingAccount = LinkedBookingAccount
		self.EmergencyContactNo = EmergencyContactNo
		self.StaffCode = StaffCode
		self.EditDate = EditDate
		self.UnitTypeSurcharge = UnitTypeSurcharge
		self.MiscSurcharge = MiscSurcharge
		self.PeakPeriodSurRate = PeakPeriodSurRate
		self.Days = Days
		self.TotalToPay = TotalToPay
		self.TodayDate = TodayDate
		self.CheckDateIn = CheckDateIn
		self.CheckDateOut = CheckDateOut

		#for extra services
		self.ServiceName = ServiceName
		self.Cost = Cost

		#for payment
		self.PaymentID = PaymentID
		self.otherChargesPaid = otherChargesPaid
		self.TaxPaid = TaxPaid
		self.TotalChargesPaid = TotalChargesPaid
		self.ExtraServices = ExtraServices
		self.DayCareRateP = DayCareRateP
		self.SubTotal = SubTotal
		self.DiscountP = DiscountP
		self.NetBookingCharges = NetBookingCharges
		self.PaymentDate = PaymentDate
		self.AmountReceived = AmountReceived
		self.PaymentType = PaymentType
		self.TotalToPay = TotalToPay



