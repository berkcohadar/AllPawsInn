################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################

import sys
import platform


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel,QWidget, QVBoxLayout, QGraphicsDropShadowEffect, QSizeGrip, QPushButton, QSizePolicy,QDateEdit,QSplashScreen,QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QSize, Qt,QDateTime,QDate,QTimer
from PyQt5.QtGui import QColor, QFont,QPixmap,QIntValidator
from ui_styles import Style
import pyodbc
# GUI FILE
from ClientDetails import Client
from DatabaseClass import Database_Class
from decimal import Decimal
from ui_main import Ui_MainWindow
import datetime

global d
# IMPORT FUNCTIONS

from Back_end_functions import *
#from Reservation_Functions import*
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        _translate = QtCore.QCoreApplication.translate
        
#        self.splash = Ui_Dialog()
#        self.splash.setupUi(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.paws= []
        #self.BackEndFunctions = BackEndFunctions()
        #self.BackEndFunctions.update_display(self)
        todaydate = QtCore.QDate.currentDate()
        self.ui.home_date.setDate(todaydate)
        todayfuncdate = todaydate.toString("yyyy-MM-dd")
        tommorrowdate = QtCore.QDate.currentDate().addDays(1)
        tommrwfuncdate = tommorrowdate.toString("yyyy-MM-dd")
        WeeklyScheduleFunctions.DisplayWeeklyList(self)
        #self.ui.treeWidget.setColumnWidth(0,200)
        #self.ui.treeWidget.setColumnWidth(1,100)
        #self.ui.treeWidget.setColumnWidth(2,100)
        #self.ui.treeWidget.setColumnWidth(3,200)
        self.ui.menu_btn_settings.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_admin))
        self.ui.menu_btn_settings.clicked.connect(lambda: AdminFunctions.DisplayAdminList(self))
        HomeFunctions.DisplayReservations(self,todayfuncdate,tommrwfuncdate)
        HomeFunctions.DisplayCheckedIn(self,todayfuncdate,tommrwfuncdate)
        HomeFunctions.DisplayCheckedOut(self,todayfuncdate,tommrwfuncdate)
        self.ui.menu_btn_daily.clicked.connect(lambda: HomeFunctions.DisplayReservations(self,todayfuncdate,tommrwfuncdate))
        # BackEndFunctions.GenerateDaylyView(self,('2020-04-24 08:00:00.000' , '2017-04-25 08:00:00.000')) # Generates error
       
        #self.ui.search_bar.textChanged.connect(lambda :BackEndFunctions.update_list(self))
        
        self.ui.res_search_bar.textChanged.connect(lambda :ReservationFunctions.updateReservationList(self))
       # UIFunctions.CREATE_CLIENT(self)

       # self.ui.home_checkin_btn.clicked.connect(lambda: BackEndFunctions.DirectCheckIn(self) )

        self.ui.res_remove.clicked.connect(lambda :ReservationFunctions.RemoveDay(self))
        self.ui.res_submit.clicked.connect(lambda: ReservationFunctions.SubmitReservation(self))
        self.ui.res_submit.clicked.connect(lambda: HomeFunctions.UpdateDisplay(self))
       # self.ui.res_submit.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home))



       ###################################################### Weekly Schedule ######################################
        self.ui.menu_btn_weekly.clicked.connect(lambda: WeeklyScheduleFunctions.DisplayWeeklySchedule(self,0))
        self.ui.weekly_date_next.clicked.connect(lambda: WeeklyScheduleFunctions.NextWeek(self))
        self.ui.weekly_date_prev.clicked.connect(lambda: WeeklyScheduleFunctions.PreviousWeek(self))

        self.ui.weekly_date_thisweek.clicked.connect(lambda: WeeklyScheduleFunctions.ThisWeek(self))

       
       #################################################################################################################
       # self.ui.home_checkin_btn.clicked.connect(lambda:BackEndFunctions.update_list(self))
   
        self.ui.home_date_next.clicked.connect(lambda: HomeFunctions.NextDay(self))
        self.ui.home_date_prev.clicked.connect(lambda: HomeFunctions.PreviosDay(self))

        #Date Implementation and set dates buttons--------------- Start-----
        d = QtCore.QDate.currentDate()


        ## ADditional Pet Page
        self.onlyInt = QIntValidator()
        self.ui.addpet_foodtype_input.setValidator(self.onlyInt)
        self.ui.addpet_age_input.setValidator(self.onlyInt)
        self.ui.addpet_foodamount_input.setValidator(self.onlyInt)
        self.ui.addpet_search_bar.textChanged.connect(lambda: AddPetFunctions.updateSearchList(self))
        self.ui.addpet_search_list.itemClicked.connect(lambda: AddPetFunctions.DisplayDetail(self))
        self.ui.addpet_delete_btn.clicked.connect(lambda: AddPetFunctions.Delete_pet(self))
        self.ui.edit_client_submit_btn_2.clicked.connect(lambda: AddPetFunctions.Set_newPet(self))
        ## Payment Page Connections
        ########################################################################

        self.ui.pay_search_bar.textChanged.connect(lambda: PaymentFunctions.updatePaymentList(self))
        self.ui.pay_take_payment_btn.clicked.connect(lambda: PaymentFunctions.SubmitPayments(self))
        #self.ui.res_list.setCurrentItem(self.ui.res_list.topLevelItem(0))
        self.ui.pay_search_list.itemClicked.connect(lambda: PaymentFunctions.DisplayDetail(self))
   
        self.ui.pay_add_list_btn_2.clicked.connect(lambda: PaymentFunctions.AddToList(self))
        self.ui.deleteRow_button.clicked.connect(lambda: PaymentFunctions.removeFromList(self))

        ########################################################################   
        ## End Payment Page Connections

        ## SERVICES
        ########################################################################
        self.ui.menu_btn_settings.clicked.connect(lambda: AdminFunctions.GetServices(self))
        self.ui.pay_services_discount.textChanged.connect(lambda : PaymentFunctions.AddServices(self))
        self.ui.pay_services_food.clicked.connect(lambda : PaymentFunctions.AddServices(self))
        self.ui.pay_services_hair.clicked.connect(lambda : PaymentFunctions.AddServices(self))
        self.ui.pay_services_nails.clicked.connect(lambda : PaymentFunctions.AddServices(self))
        self.ui.pay_services_other_goods.textChanged.connect(lambda : PaymentFunctions.AddServices(self))
        self.ui.admin_service_change_cost_btn.clicked.connect(lambda: AdminFunctions.ChangeServiceCost(self))
        self.ui.admin_service_list.itemClicked.connect(lambda: AdminFunctions.ChangeCurrentService(self))
        ########################################################################
        d.toString(QtCore.Qt.ISODate)

      ## HOME PAGE
        ########################################################################
        self.ui.home_checkin_btn.clicked.connect(lambda: HomeFunctions.CheckedIn(self))
        self.ui.home_checkin_btn.clicked.connect(lambda: HomeFunctions.UpdateDisplay(self))
        
        self.ui.home_checkout_btn.clicked.connect(lambda: HomeFunctions.CheckedOutWithoutPayment(self))
        
        self.ui.mpayment_submt_services_btn.clicked.connect(lambda: HomeFunctions.CheckoutWithoutPaymentServices(self))
        self.ui.mpayment_submt_services_btn.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home))
        
        
        
        self.ui.home_checkout_w_btn.clicked.connect(lambda: HomeFunctions.CheckedOutWithPayment(self))
        

        self.ui.mpayment_make_payment_btn.clicked.connect(lambda : HomeFunctions.CheckOutWithPaymentMakePayment(self))

        self.ui.res_calendar.clicked.connect(lambda: ReservationFunctions.AddDaysToSelectedDayList(self))
        self.ui.mpayment_nails.clicked.connect(lambda : HomeFunctions.CheckoutWithPaymentServices(self))
        self.ui.mpayment_hair.clicked.connect(lambda : HomeFunctions.CheckoutWithPaymentServices(self))
        self.ui.mpayment_other_goods.textChanged.connect(lambda : HomeFunctions.CheckoutWithPaymentServices(self))
        self.ui.mpayment_food.clicked.connect(lambda : HomeFunctions.CheckoutWithPaymentServices(self))
        self.ui.mpayment_discount.textChanged.connect(lambda : HomeFunctions.CheckoutWithPaymentServices(self))

        self.ui.home_show_today.clicked.connect(lambda: HomeFunctions.ShowToday(self))
          ## Admin PAGE 
        ########################################################################
        self.ui.admin_delete_profile_btn.clicked.connect(lambda: AdminFunctions.DeleteProfile(self))
        self.ui.admin_add_profile_btn.clicked.connect(lambda : AdminFunctions.AddAdminSetting(self))
        self.ui.admin_activate_profile_btn.clicked.connect(lambda : AdminFunctions.ActivateProfile(self))
         ########################################################################
        ## Toogle Bottons to PAGES
        ########################################################################

      
        self.ui.menu_btn_newclient.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_client))
        self.ui.menu_btn_daily.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home))
        #self.ui.menu_btn_daily.clicked.connect(lambda:HomeFunctions.ChangeColor(self) )
        self.ui.menu_btn_weekly.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_weekly))
        self.ui.menu_btn_payment.clicked.connect(lambda : self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_payment))
        self.ui.menu_btn_reports.clicked.connect(lambda : self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_reports))
     #   self.ui.check_button.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.daycare_page))
        self.ui.menu_btn_reservation.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_reservation) )
        self.ui.menu_btn_editclient.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_editclient) )
        self.ui.menu_btn_addanimal.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_addpet) )
         ########################################################################

         
        ############################################# EDIT CLIENT ############################################

        self.ui.editclient_search_bar.textChanged.connect(lambda :EditClientFunctions.updateSearchList(self))
        self.ui.editclient_search_list.itemClicked.connect(lambda: EditClientFunctions.DisplayDetail(self))
        self.ui.edit_client_submit_btn.clicked.connect(lambda: EditClientFunctions.editClient(self))
        ##############################################################################################




         ## REMOVE ==> STANDARD TITLE BAR
        UIFunctions.removeTitleBar(True)
        ## ==> END ##

        ## SET ==> WINDOW TITLE
        self.setWindowTitle('Allpawsinn')
        UIFunctions.labelTitle(self, 'Allpawsinn Dashboard')
        UIFunctions.labelDescription(self, 'Search Bar')
        ## ==> END ##

        ## WINDOW SIZE ==> DEFAULT SIZE
        startSize = QSize(1400, 900)
        minSize = QSize(1240, 820)
        self.setMinimumSize(minSize)
        self.resize(startSize)

        #UIFunctions.enableMaximumSize(self, 500, 720)
        ## ==> END ##

        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 190, True))
        ## End

         ## ==> LOAD DEFINITIONS
        ########################################################################
        UIFunctions.uiDefinitions(self)
        ## ==> END ##



        self.ui.mpayment_cancel_services_btn.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home))
        self.ui.mpayment_cancel_payment_btn.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home))
        self.ui.res_cancel.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home))


        #self.ui.btn_Menu1_3.clicked.connect(lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.page_5))
       # self.ui.btn_vet_detail_3.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_vet))
       # self.ui.btn_vet_detail_4.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_vet))
       # self.ui.btn_vet_detail_2.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_vet))

        
        self.ui.client_pet_btn.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_animal))
        self.ui.pet_vet_btn.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_vet))
        self.ui.vet_submit_btn.clicked.connect(lambda: BackEndFunctions.CREATE_CLIENT(self))
        self.ui.vet_submit_btn.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home))
      #  self.ui.btn_client_info_3.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_client))
      #  self.ui.btn_client_info_4.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_client))


     #   self.ui.btn_animal_info_4.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_animal))
     #   self.ui.btn_animal_info_3.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_animal))
     #   self.ui.btn_animal_info_2.clicked.connect(lambda: self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_animal))
     ## ==> START PAGE
        self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home)
        ## ==> END ##
        
       ## ==> MOVE WINDOW / MAXIMIZE / RESTORE
        ########################################################################
        def moveWindow(event):
            # IF MAXIMIZED CHANGE TO NORMAL
            if UIFunctions.returStatus() == 1:
                UIFunctions.maximize_restore(self)

            # MOVE WINDOW
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos() 
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_label_top_btns.mouseMoveEvent = moveWindow
        ## ==> END ##
        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##
  ########################################################################
    ## MENUS ==> DYNAMIC MENUS FUNCTIONS
    ########################################################################
    def show_popup(self,title,text):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)

        x= msg.exec_()
    def Button(self):
        # GET BT CLICKED
        btnWidget = self.sender()

        # PAGE HOME
        if btnWidget.objectName() == "btn_new_user":
            self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_new_user")
            UIFunctions.labelPage(self, "Home")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE NEW USER
        if btnWidget.objectName() == "btn_new_user":
            self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_home)
            UIFunctions.resetStyle(self, "btn_new_user")
            UIFunctions.labelPage(self, "New User")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

        # PAGE WIDGETS
        if btnWidget.objectName() == "btn_widgets":
            self.ui.Content_stacked_Widget.setCurrentWidget(self.ui.page_widgets)
            UIFunctions.resetStyle(self, "btn_widgets")
            UIFunctions.labelPage(self, "Custom Widgets")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(btnWidget.styleSheet()))

    ## ==> END ##

    ########################################################################
    ## START ==> APP EVENTS
    ########################################################################

    ## EVENT ==> MOUSE DOUBLE CLICK
    ########################################################################
    def eventFilter(self, watched, event):
        if watched == self.le and event.type() == QtCore.QEvent.MouseButtonDblClick:
            print("pos: ", event.pos())
    ## ==> END ##

    ## EVENT ==> MOUSE CLICK
    ########################################################################
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')
        if event.buttons() == Qt.MidButton:
            print('Mouse click: MIDDLE BUTTON')
    ## ==> END ##

    ## EVENT ==> KEY PRESSED
    ########################################################################
    def keyPressEvent(self, event):
        print('Key: ' + str(event.key()) + ' | Text Press: ' + str(event.text()))
    ## ==> END ##

    ## EVENT ==> RESIZE EVENT
    ########################################################################
    def resizeEvent(self, event):
        self.resizeFunction()
        return super(MainWindow, self).resizeEvent(event)

    def resizeFunction(self):
        print('Height: ' + str(self.height()) + ' | Width: ' + str(self.width()))
    ## ==> END ##
  

    ########################################################################
    ## END ==> APP EVENTS
    ############################## ---/--/--- ##############################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    timer = QTimer()
    pixmap = QPixmap('C:\\Users\\Berk\\Desktop\\AllPawsInn\\codes\\icon.png')
    splash = QSplashScreen(pixmap)
    splash.show()
    splash.showMessage("Loading...")    
    
    timer.singleShot(10000, window.show )

    
    app.processEvents()
    splash.showMessage("Loading is completed")
    
    
     
    splash.finish(window)
    
   
    sys.exit(app.exec_())