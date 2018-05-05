
from flask import Flask, redirect, url_for, request, render_template, make_response, session, escape, abort

from multiprocessing import cpu_count

import subprocess
import sqlite3
import time
import os, webbrowser
import ipcontrol
import htmlmodule

screenposdisplay = htmlmodule.poscreen

myipaddress = ipcontrol.myipaddress

localtime = time.asctime(time.localtime(time.time()))

ipcontrol.GET_IP_CMD

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

ip = run_cmd(ipcontrol.GET_IP_CMD)

albiemerapp = Flask(__name__)

albiemerapp.secret_key = 'any random string'

@albiemerapp.route('/deldatabase', methods = ['POST', 'GET'])  ##check
def deldatabasefunc():
    if request.method == 'POST':
        myidelete = request.form['id_bar_code']
        ##myid = request['id']
        
        conn = sqlite3.connect('mydb.db')
        c = conn.cursor()
        
        try:
            c.execute("DELETE FROM products WHERE Barcode=?", (myidelete,))
            conn.commit()
            return redirect(url_for('opendatabasefunc'))
            
        except:
            conn.rollback()
        
        conn.close()

@albiemerapp.route('/opendatabase')  ## check
def opendatabasefunc():
    
    conn = sqlite3.connect('mydb.db')
    c = conn.cursor()
    
    try:
        c.execute("SELECT * FROM POS_Products")
        result1 = c.fetchall()
        
        try:
            result = c.fetchone()
            result2 = c.fetchone()
            
            placeholder = "SEARCH PRODUCT..."
            
            c.execute("select * from user")
            result3 = c.fetchall()
            
            if 'sesuserbase' in session:
                userbase = session['sesuserbase']
                session.pop('sesuserbase', None)
                
                return render_template("product_entry.html", userbase = userbase, placeholder = placeholder, data = result, data1 = result1, data2 = result2, data3 = result3, myipaddress = myipaddress)
                
            
            database = "defaultOpen"
            return render_template("product_entry.html", database = database, placeholder = placeholder, data = result, data1 = result1, data2 = result2, data3 = result3, myipaddress = myipaddress)
        
            
        
        except:
            
            conn.rollback()
    
    except:
        
        conn.rollback()
        
    conn.close()

@albiemerapp.route('/tosearch', methods = ['POST', 'GET'])  ##check
def tosearchfunc():
    
    if request.method == 'POST': 
        
        myproductcode = request.form['productcode']
        
        conn = sqlite3.connect('mydb.db')
    
        c = conn.cursor()
        
        c.execute("SELECT * FROM POS_Products WHERE Product=?", (myproductcode,))
        
        result1 = c.fetchall()
        
        try:
            
            c.execute("SELECT * FROM POS_Products WHERE Product=?", (myproductcode,))
            
            result = c.fetchone()
            
            c.execute("select * from products where Product=?", (myproductcode,))
            
            result2 = c.fetchone()
            
            c.execute("select * from user")
            
            result3 = c.fetchall()
            
            dis = 'disabled'
            
            database = "defaultOpen"
                
            placeholder = "SEARCH PRODUCT..."
            
            return render_template("product_entry.html", data3 = result3, database = database, placeholder = placeholder, dis = dis, data = result, data1 = result1, data2 = result2, myipaddress = myipaddress)
        
        except:
            
            conn.rollback()
        
        conn.close()    
        
@albiemerapp.route('/todatabase')
def databasefunc():
    
    if 'result' in session:
        
        sresult = session['result']
        
        session.pop('result', None)
    
    conn = sqlite3.connect('mydb.db')
    
    
    c = conn.cursor()
    
    try:
        
        c.execute("SELECT * FROM products")
        
        resultall = c.fetchall()
        
        return render_template("product_entry.html", data = resultall, data1 = sresult, myipaddress = myipaddress)
        
    except:
        
        conn.rollback()
        
    conn.close()

@albiemerapp.route('/addnewdata', methods = ['POST', 'GET']) ##check
def addnewrecordfunc():
    
    if request.method == 'POST':
        
        mybarcode = request.form['bar_code']
        
        conn = sqlite3.connect('mydb.db')
        
        c = conn.cursor()
        
        c.execute("delete from products where Barcode=?",(mybarcode,))
           
        conn.commit()
        
        try:
            
            myproduct = request.form['pro_duct']
            mybarcode = request.form['bar_code']
            myquantity = request.form['quan_tity']
            mytax = request.form['ta_x']
            mydiscount = request.form['dis_count']
            mynetcost = request.form['net_cost']
            myprice = request.form['pr_ice']
            mystockpc = request.form['stock_pc']
            mystockcs = request.form['stock_cs']
            mycompany = request.form['com_pany']
            myimage = request.form['i_mage']
            
            c.execute("insert into products (Product, Barcode, Quantity, Tax, Discount, Net_Cost, Price, Stockpc, Stockcs, Datetime, Company, Image) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                      ( myproduct, mybarcode, myquantity, mytax, mydiscount, mynetcost, myprice, mystockpc, mystockcs, localtime, mycompany, myimage,))
        
            conn.commit()
    
            return redirect(url_for('opendatabasefunc'))

        except:
            
            conn.rollback()
            
        conn.close()

@albiemerapp.route('/page')
def get_screen_resolution():
    output = subprocess.Popen('xrandr | grep "\*" | cut -d" " -f4',shell=True, stdout=subprocess.PIPE).communicate()[0]
    resolution = output.split()[0].split(b'x')
    session['info_resolution'] = {'width': resolution[0], 'height': resolution[1]}

    return redirect(url_for('confirm_screen_size'))

@albiemerapp.route('/toconfirmscreensize')
def confirm_screen_size():
    
    resultsize = session['info_resolution']
    
    if resultsize.items():
        
        height = resultsize['height']
        width = resultsize['width']
        
        if height == b'768' and width == b'1024':
            
            session.pop('info_resolution', None)
            
            print(height)
            print(width)
            
            return redirect(url_for('readpunchfunc'))
        
        elif height == b'768' and width ==b'1366':
            
            print(height)
            print(width)
            
        else:
            
            print("press enter to go to default size:")
            

@albiemerapp.route('/userbox', methods = ['POST', 'GET'])
def userboxfunc():
    
    if request.method == 'POST':
        
        try:
            
            my_fname = request.form['first_name']
            my_lname = request.form['last_name']
            my_user = request.form['user_name']
            my_position = request.form['po_sition']
            my_pass = request.form['p_sw']
            
            conn = sqlite3.connect('mydb.db')
        
            c = conn.cursor()
            
            c.execute("insert into user (Firstname, Lastname, Username, Position, Password, Terminal) values (?,?,?,?,?,?)",\
                  (my_fname, my_lname, my_user,my_position, my_pass, 'Terminal 1'))

            conn.commit()
        
            session['sesuserbase'] = "defaultOpen"
        
            return redirect(url_for('opendatabasefunc'))
            
        except:
            
            conn.rollback()
        
        conn.close()
        


@albiemerapp.route('/deluser')
def deluserfunc():
    
    conn = sqlite3.connect('mydb.db')
    
    c = conn.cursor()
    
    c.execute("delete from user")
    
    conn.commit()
    
    conn.close()
    
    return redirect(url_for('opendatabasefunc'))
        
@albiemerapp.route('/myposuser', methods = ['POST', 'GET'])
def myposuserfunc():
    
    if request.method == 'POST':
        
        my_user = request.form['u_ser']
        my_pass = request.form['p_ass']
        
        if my_user == 'albiemer' and my_pass == 'dbase':
            
            return redirect(url_for('opendatabasefunc'))
        
        conn = sqlite3.connect('mydb.db')
        
        c = conn.cursor()
        
        c.execute("select * from user where Username=(?) and Password=(?)", (my_user, my_pass))
        
        result = c.fetchone()
        
        try:
            
            if result[3] == my_user and result[5] == my_pass:
                
                userin = result[1] + " " + result[2]
            
                session['c1user'] = userin
            
                c.execute("insert into log (User, Terminal, Position) values (?,?,?)", (userin, 'Terminal 1', result[4]))
            
                conn.commit()
            
                return redirect(url_for('readpunchfunc'))
            
        except:
            
            note = "USER ACCOUNT NOT FOUND, PLEASE REGISTER"
            
            return render_template("Logintopos.html", note = note, myipaddress = myipaddress)

        conn.close()
        

@albiemerapp.route('/mypos')
def myposfunc():
    
    if 'c1user' in session:
        
        return redirect(url_for('readpunchfunc'))
        
        
    else:
        
        return render_template("Logintopos.html", myipaddress = myipaddress)


@albiemerapp.route('/logout')
def lofoutfunc():
    
    session.pop('c1user', None)
    
    conn = sqlite3.connect('mydb.db')
    
    c = conn.cursor()
    
    c.execute("delete from log")
    
    conn.commit()
    
    conn.close()
    
    return render_template("Logintopos.html", myipaddress = myipaddress)

@albiemerapp.route('/delog')
def delogfunc():
    
    conn = sqlite3.connect('mydb.db')
    
    c = conn.cursor()
    
    c.execute("delete from log")
    
    conn.commit()
    
    conn.close()
    
    return redirect(url_for('myposfunc'))

#################################################POS#################################################






#####################################################################################################

@albiemerapp.route('/writepunch', methods = ['POST', 'GET'])
def writepunchfunc():
    
    if request.method == 'POST':
        
        bar_code = request.form['product_code']
        
        session['sesproduct'] = bar_code
        
        try:
            
            conn = sqlite3.connect('mydb.db')
        
            c = conn.cursor()
        
            c.execute("select Barcode from scanned where Barcode=?", (bar_code,))
            
            if c.fetchone() == None:
                
                c.execute("select * from products where Barcode=?", (bar_code,))
                
                result = c.fetchone()
                
                netotal = result[3] * result[6]
                
                qptotal = result[7] - result[5]
                
                myproduct = result[1]
                mybarcode = result[2]
                myquantity = result[3]
                mytax = result[4]
                mydiscount = result[5]
                mynetcost = result[6]
                myprice = result[7]
                mystockpc = result[8]
                mystockcs = result[9]
                mycompany = result[11]
                myimage = result[12]
                
                
                c.execute("insert into scanned ( Product, Barcode, Quantity, Tax, Discount, Net_Cost, Price, Stockpc, Stockcs, Datetime, Company, Image, Net_Total, Total) values ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                      ( myproduct, mybarcode, myquantity, mytax, mydiscount, mynetcost, myprice, mystockpc, mystockcs, localtime, mycompany, myimage, netotal, qptotal))
                
                conn.commit()
                
                return redirect(url_for('readpunchfunc'))
                
            else:
                
                try:
                    
                    c.execute("select * from scanned where Barcode=?", (bar_code,)) ##prevrec
                    result1 = c.fetchone()
                    
                    c.execute("select * from products where Barcode=?", (bar_code,))  ##baserec
                    result2 = c.fetchone()
                    
                    tquantity = result1[3] + result2[3]
                    
                    #nottotalatall = result1[3] * result2[7]
                    
                    ttotal = result1[4] + result2[4]
                
                    nettotal = result1[13] + result2[6]
                    
                    dtotal = result1[5] + result2[5]
                
                    suballtotal = nettotal + ttotal
                    
                    alltotal = suballtotal - dtotal
                    
                    c.execute("delete from scanned where Barcode=?", (bar_code,))
                
                    c.execute("insert into scanned (Product, Barcode, Quantity, Tax, Discount, Net_Cost, Price, Stockpc, Stockcs, Datetime, Company, Image, Net_Total, Total) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                          (result2[1], result2[2], tquantity, ttotal, dtotal, result2[6], result2[7], result2[8], result2[9], result2[10], result2[11], result2[12], nettotal, alltotal))

                    conn.commit()
                    
                    return redirect(url_for('readpunchfunc'))
                
                except:
                    
                    print("Error")
            
            
        except:
            
            if c.fetchone() == None:
                
                return redirect(url_for('punchnotfoundfunc'))
            
        conn.close()
    

    
@albiemerapp.route('/addquantity')
def addquantityfunc():
    
    if 'sesproduct' in session:
        
        pymyproduct = session['sesproduct']
    
        conn = sqlite.connect('mydb.db')
    
        c = conn.cursor()
    
        c.execute("select Quantity, Price, Quantity*price as total from scanned where Barcode=?", (pymyproduct,))
        
        qptotal = c.fetchone()
    
        c.execute("insert into scanned (Total) values (?) where Barcode=?", (pymyproduct,))
        
        conn.commit()
        
        conn.close()
        
        return redirect(url_for('readpunchfunc'))



@albiemerapp.route('/punchnotfound')
def punchnotfoundfunc():
    
    conn = sqlite3.connect('mydb.db')
    
    c = conn.cursor()
    
    c.execute("select * from scanned")
    
    result = c.fetchall()
    
    result1 = c.fetchone()
    
    c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Price), sum(Net_Total), sum(Total) from scanned")
            
    result2 = c.fetchone()
    
    c.execute("select * from log")
    
    result3 = c.fetchone()
    
    note = 'NOT FOUND PRODUCT... REPUNCH AGAIN.'
    
    return render_template(screenposdisplay, data = result, data1 = result1, note = note, total = result2, log = result3, myipaddress = myipaddress)
        
    conn.close()


@albiemerapp.route('/readpunch')
def readpunchfunc():
    
    try:
        
        if 'sesproduct' in session or 'c1user' in session:
            
            smyproduct = session['sesproduct']
        
            sesciuser = session['c1user']
            
            conn = sqlite3.connect('mydb.db')
        
            c = conn.cursor()
        
            c.execute("select * from scanned")
        
            result = c.fetchall()
        
        
            c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Price), sum(Net_Total), sum(Total) from scanned")
            
            result2 = c.fetchone()
            
            c.execute("select * from scanned where Barcode=?", (smyproduct,))
        
            result1= c.fetchone()
        
            c.execute("select * from log where User=?", (sesciuser,))
        
            result3 = c.fetchone()
        
            return render_template(screenposdisplay, data = result, data1 = result1, total = result2, log = result3, myipaddress = myipaddress)
            
            session.pop('sesproduct', None)    
        
            conn.close()
          
    except:
        
        conn = sqlite3.connect('mydb.db')
        
        c = conn.cursor()
        
        c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Price), sum(Net_Total), sum(Total) from scanned")
            
        result2 = c.fetchone()
        
        c.execute("select * from scanned")
        
        result = c.fetchall()
        
        result1 = c.fetchone()
        
        c.execute("select * from log")
        
        result3 = c.fetchone()
        
        return render_template(screenposdisplay, data = result, data1 = result1, total = result2, log = result3, myipaddress = myipaddress)
        
        conn.close()
        

@albiemerapp.route('/deleteallscanned')
def deleteallscanned():
    
    conn = sqlite3.connect('mydb.db')
    
    c = conn.cursor()
    
    try:
        
        c.execute("delete from scanned")
    
        conn.commit()
    
        return redirect(url_for('readpunchfunc'))

    except:
        
        conn.rollback()
        
    conn.close()

@albiemerapp.route('/logintodelete', methods = ['POST', 'GET'])
def logintodeletedef():
    
    if request.method == 'POST':
        
        todelproduct = request.form['product_code']
        
        if 'c1user' in session:
            
            suser = session['c1user']
            
            conn = sqlite3.connect('mydb.db')
            
            c = conn.cursor()
                
            c.execute("select * from log where User=?", (suser,))
                
            result = c.fetchone()
            
            c.execute("select * from scanned where Product=?",(todelproduct,))
                
            if c.fetchone() == None:
                
                return redirect(url_for('notfoundtodelete'))
            
            else:
                
                try:
                    
                    if result[3] == 'Admin' or result[3] == 'Supervisor' or result[3] == 'I.T. Staff':
                        
                        c.execute("delete from scanned where Product=?",(todelproduct,))
                    
                        conn.commit()
                    
                        return redirect(url_for('get_screen_resolution')) 
                
                    
                    else:
                        
                        return render_template("logintodelete.html", dataproduct = todelproduct, myipaddress = myipaddress)
                
                except:
                    
                    note = "PLEASE LOGIN FIRST, THE LOG HAS NO RECORD."
                    
                    return render_template("Logintopos.html", note = note, myipaddress = myipaddress)
                    
                conn.close()
                    
            
           
@albiemerapp.route('/deletescanned', methods = ['POST', 'GET'])
def deletescannedfunc():
   
   if request.method == 'POST':
        
        todelproduct = request.form['product_code']
        myuser = request.form['u_ser']
        mypass = request.form['p_ass']
                
        conn = sqlite3.connect('mydb.db')
        c = conn.cursor()
            
        c.execute("select * from user where Username=(?) and Password=(?)", (myuser, mypass))
            
        result = c.fetchone()
            
        try:
            
            if result[4] == 'Admin' or result[4] == 'Supervisor' or result[4] == 'I.T. Staff':
                
                c.execute("delete from scanned where Product=?", (todelproduct,))
            
                conn.commit()
            
                return redirect(url_for('get_screen_resolution'))
        
                conn.close()
            
            else:
                
                note = "USER ARE NOT AUTORIZED TO DELETE. PLEASE SPECIFIED ACCOUNT"
                
                return render_template("logintodelete.html", note = note, dataproduct = todelproduct, myipaddress = myipaddress)
            
        except:
            
            note = "USER ACCOUNT NOT FOUND, PLEASE REGISTER"
            
            
            return render_template("logintodelete.html", note = note, dataproduct = todelproduct, myipaddress = myipaddress)

        conn.close()


@albiemerapp.route('/notfoundtodelete')
def notfoundtodelete():
    
    conn = sqlite3.connect('mydb.db')
    
    c = conn.cursor()
    
    c.execute("select * from scanned")
    
    result = c.fetchall()
    
    result1 = c.fetchone()
    
    c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Price), sum(Net_Total), sum(Total) from scanned")
            
    result2 = c.fetchone()
    
    c.execute("select * from log")
    
    result3 = c.fetchone()
    
    note = 'NO FOUND PRODUCT TO DELETE... TRY TO CORRECT INPUT.'
    
    return render_template("logintodelete.html", data = result, data1 = result1, note = note, total = result2, log = result3, myipaddress = myipaddress)
        
    conn.close()
    


########################################################################################################
#payment
    
#######################################################################################################    

@albiemerapp.route('/cashpayment')
def cashpaymentdef():
    
    conn = sqlite3.connect('mydb.db')
    
    c = conn.cursor()
    
    c.execute("select * from scanned")
    
    if c.fetchone() == None:
        
        return redirect(url_for('get_screen_resolution'))
    
    c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Net_Total), sum(Tax)-sum(Discount)+sum(Net_Total) as Total_Payment from scanned")
    
    result_total = c.fetchone()
    
    receipt = "READY TO PRINT RECEIPT"
    
    altc = "disabled hidden"
    
    return render_template("cash payment process.html", data = result_total, receipt = receipt, altc = altc, myipaddress = myipaddress)
   

@albiemerapp.route('/checkpayment')
def checkpaymentdef():
    
    conn = sqlite3.connect('mydb.db')
    
    c = conn.cursor()
    
    c.execute("select * from scanned")
    
    if c.fetchone() == None:
        
        return redirect(url_for('get_screen_resolution'))
    
    c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Net_Total), sum(Tax)-sum(Discount)+sum(Net_Total) as Total_Payment from scanned")
    
    result_total = c.fetchone()
    
    receipt = "READY TO PRINT RECEIPT"
    
    altc = "disabled hidden"
    
    return render_template("check payment process.html", data = result_total, receipt = receipt, altc = altc, myipaddress = myipaddress)

@albiemerapp.route('/checkinfoentry', methods =['POST', 'GET'])
def checkinfoentrydef():
    
    if request.method == 'POST':
        
        mycheckholder_name = request.form['checkholder_name']
        mycheckholder_address = request.form['checkholder_address']
        mycheckholder_zip = request.form['checkholder_zip']
        mycheckholder_accountnumber = request.form['checkholder_accountnumber']
        mycheckholder_checknumber = request.form['checkholder_checknumber']
        mycardholder_validdate = request.form['cardholder_validdate']
        
        if 'sestotalreceived' in session:
            
            mytotalreceived = session['sestotalreceived']
            
        try:
            
            conn = sqlite3.connect('mydb.db')
            
            c = conn.cursor()
            
            c.execute("insert into checkholder_info (Name, Address, Zip, Account_Number, Check_Number, Valid_Date) values (?,?,?,?,?,?)", \
                      (mycheckholder_name, mycheckholder_address, mycheckholder_zip, mycheckholder_accountnumber, mycheckholder_checknumber, mycardholder_validdate))
            
            conn.commit()
            
            c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Net_Total), sum(Tax)-sum(Discount)+sum(Net_Total) as Total_Payment from scanned")
        
            result = c.fetchone()
            
            changemoney = float(mytotalreceived) - float(result[4])
        
            c.execute("select * from log")
            result1 = c.fetchone()
        
            c.execute("insert into daytransaction (Total, Total_Received, Total_Changed, Total_Discount, Total_Tax, Net_Total, User, Terminal, Datetime) values (?,?,?,?,?,?,?,?,?)", \
                      (result[4], mytotalreceived, changemoney, result[2], result[1], result[3], result1[1], result1[2], localtime))
        
            conn.commit()
        
            c.execute("Delete from scanned")
        
            conn.commit()
        
            receipt = "PRINTING RECEIPT..."
        
            readonlyfunc = 'readonly = "readonly"'
        
            altcrev = "disabled hidden"
        
            altrev1 = "disabled"
        
            session.pop('sestotalreceived', None)
        
            return render_template("check payment process.html", data = result, datachange = changemoney, mytotalreceived = mytotalreceived, receipt = receipt, readonlyfunc = readonlyfunc, altcrev = altcrev, altrev1 = altrev1, myipaddress = myipaddress)
            
        except:
            
            return redirect(url_for('myposfunc'))
            
            session.pop('sestotalreceived', None)
        
        conn.close()
            

@albiemerapp.route('/checkpaidprocess', methods = ['POST', 'GET'])
def checkpaidprocessdef():
    
    if request.method == 'POST':
        
        mytotalreceived = request.form['input_total_received']
        
        session['sestotalreceived'] = mytotalreceived
        
        conn = sqlite3.connect('mydb.db')
        
        c = conn.cursor()
        
        c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Net_Total), sum(Tax)-sum(Discount)+sum(Net_Total) as Total_Payment from scanned")
        
        result = c.fetchone()
        
        return render_template("check info entry.html", data = result, mytotalreceived = mytotalreceived, myipaddress = myipaddress)
    

@albiemerapp.route('/cardpayment')
def cardpaymentdef():
    
    conn = sqlite3.connect('mydb.db')
    
    c = conn.cursor()
    
    c.execute("select * from scanned")
    
    if c.fetchone() == None:
        
        return redirect(url_for('get_screen_resolution'))
    
    c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Net_Total), sum(Tax)-sum(Discount)+sum(Net_Total) as Total_Payment from scanned")
    
    result_total = c.fetchone()
    
    receipt = "READY TO PRINT RECEIPT"
    
    altc = "disabled hidden"
    
    return render_template("card payment process.html", data = result_total, receipt = receipt, altc = altc, myipaddress = myipaddress)


@albiemerapp.route('/cardinfoentry', methods = ['POST', 'GET'])
def cardinfoentrydef():
    
    if request.method == 'POST':
        
        mycardholder_name = request.form['cardholder_name']
        mycardholder_address = request.form['cardholder_address']
        mycardholder_zip = request.form['cardholder_zip']
        mycardholder_cardnumber = request.form['cardholder_cardnumber']
        mycardholder_expirationdate = request.form['cardholder_expirationdate']
        mycardholder_verificationcode = request.form['cardholder_verificationcode']
        
        if 'sestotalreceived' in session:
            
            mytotalreceived = session['sestotalreceived']
        
        try:
            
            conn = sqlite3.connect('mydb.db')
        
            c = conn.cursor()
        
            c.execute("insert into cardholder_info (Name, Address, Zip, Card_Number, Expiration_Date, Verification_Number) values (?,?,?,?,?,?)",\
                      (mycardholder_name, mycardholder_address, mycardholder_zip, mycardholder_cardnumber, mycardholder_expirationdate, mycardholder_verificationcode))
        
            conn.commit()
        
            c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Net_Total), sum(Tax)-sum(Discount)+sum(Net_Total) as Total_Payment from scanned")
        
            result = c.fetchone()
            
            changemoney = float(mytotalreceived) - float(result[4])
        
            c.execute("select * from log")
            result1 = c.fetchone()
        
            c.execute("insert into daytransaction (Total, Total_Received, Total_Changed, Total_Discount, Total_Tax, Net_Total, User, Terminal, Datetime) values (?,?,?,?,?,?,?,?,?)", \
                      (result[4], mytotalreceived, changemoney, result[2], result[1], result[3], result1[1], result1[2], localtime))
        
            conn.commit()
        
            c.execute("Delete from scanned")
        
            conn.commit()
        
            receipt = "PRINTING RECEIPT..."
        
            readonlyfunc = 'readonly = "readonly"'
        
            altcrev = "disabled hidden"
        
            altrev1 = "disabled"
        
            session.pop('sestotalreceived', None)
        
            return render_template("card payment process.html", data = result, datachange = changemoney, mytotalreceived = mytotalreceived, receipt = receipt, readonlyfunc = readonlyfunc, altcrev = altcrev, altrev1 = altrev1, myipaddress = myipaddress)
        
        except:
            
            return redirect(url_for('myposfunc'))
            
            session.pop('sestotalreceived', None)
        
        conn.close()

@albiemerapp.route('/cardpaidprocesss', methods = ['POST', 'GET'])
def cardpaidprocessdef():
    
    if request.method == 'POST':
        
        mytotalreceived = request.form['input_total_received']
        
        session['sestotalreceived'] = mytotalreceived
        
        conn = sqlite3.connect('mydb.db')
        
        c = conn.cursor()
        
        c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Net_Total), sum(Tax)-sum(Discount)+sum(Net_Total) as Total_Payment from scanned")
        
        result = c.fetchone()
        
        return render_template("card info entry.html", data = result, mytotalreceived = mytotalreceived, myipaddress = myipaddress)
        

@albiemerapp.route('/paidprocess', methods = ['POST', 'GET'])
def paidprocessdef():
    
    if request.method == 'POST':
        
        mytotalreceived = request.form['input_total_received']
        
        try:
            
            conn = sqlite3.connect('mydb.db')
        
            c = conn.cursor()
        
            c.execute("select sum(Quantity), sum(Tax), sum(Discount), sum(Net_Total), sum(Tax)-sum(Discount)+sum(Net_Total) as Total_Payment from scanned")
        
            result = c.fetchone()
            
            changemoney = float(mytotalreceived) - float(result[4])
        
            c.execute("select * from log")
            result1 = c.fetchone()
        
            c.execute("insert into daytransaction (Total, Total_Received, Total_Changed, Total_Discount, Total_Tax, Net_Total, User, Terminal, Datetime) values (?,?,?,?,?,?,?,?,?)", \
                      (result[4], mytotalreceived, changemoney, result[2], result[1], result[3], result1[1], result1[2], localtime))
        
            conn.commit()
        
            c.execute("Delete from scanned")
        
            conn.commit()
        
            receipt = "PRINTING RECEIPT..."
        
            readonlyfunc = 'readonly = "readonly"'
        
            altcrev = "disabled hidden"
        
            altrev1 = "disabled"
        
        except:
            
            return redirect(url_for('myposfunc'))
            
        conn.close()
        
        return render_template("cash payment process.html", data = result, datachange = changemoney, receipt = receipt, mytotalreceived = mytotalreceived, readonlyfunc = readonlyfunc, altcrev = altcrev, altrev1 = altrev1, myipaddress = myipaddress)

#------------------------------------------------------------------------------------------------------------

@albiemerapp.route('/startquantity')
def startquantitydef():
    
    disable2 = "readonly autofocus"
    
    disable1 = "autofocus"
    
    direction = "assignquantity"
    
    return render_template("quantitycontrol.html", direction = direction, disable1 = disable1, disable2 = disable2, myipaddress = myipaddress)

@albiemerapp.route('/assignquantity', methods = ['POST', 'GET'])
def assignquantitydef():
    
    if request.method == 'POST':
        
        quantity = request.form['quan_tity']
        
        session['sesquantity'] = quantity
        
        disable1 = "readonly"
        
        disable2 = "autofocus"
        
        direction = "processquantity"
        
        return render_template("quantitycontrol.html", quantity = quantity, direction = direction, disable1 = disable1, disable2 = disable2, myipaddress = myipaddress)

@albiemerapp.route('/processquantity', methods = ['POST', 'GET'])
def processquantitydef():
    
    if request.method == 'POST':
        
        bar_code = request.form['product_code']
        
        session['sesproduct'] = bar_code
        
        if 'sesquantity' in session:
            
            receivedquantity = session['sesquantity']
            
            conn = sqlite3.connect('mydb.db')
        
            c = conn.cursor()
        
            c.execute("select Barcode from scanned where Barcode=?", (bar_code,))
            
            if c.fetchone() == None:
                
                c.execute("select * from products where Barcode=?", (bar_code,))
                
                result = c.fetchone()
                
                myproduct = result[1]
                mybarcode = result[2]
                myquantity = float(receivedquantity) #result[3]
                mytax = result[4] * float(receivedquantity)
                mydiscount = result[5] * float(receivedquantity)
                mynetcost = result[6]
                myprice = result[7]
                mystockpc = result[8]
                mystockcs = result[9]
                mycompany = result[11]
                myimage = result[12]
                
                netotal = float(receivedquantity) * float(mynetcost)
                
                alltotal = float(netotal) + float(mytax)
                
                qptotal = float(alltotal) - float(mydiscount)
                
                c.execute("insert into scanned ( Product, Barcode, Quantity, Tax, Discount, Net_Cost, Price, Stockpc, Stockcs, Datetime, Company, Image, Net_Total, Total) values ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                          ( myproduct, mybarcode, myquantity, mytax, mydiscount, mynetcost, myprice, mystockpc, mystockcs, localtime, mycompany, myimage, netotal, qptotal))
                
                conn.commit()
                
                session.pop('sesquantity', None)
                
                print(receivedquantity, bar_code)
                
                return redirect(url_for('readpunchfunc'))
            
            else:
                
                disable2 = "readonly autofocus"
    
                disable1 = "autofocus"
    
                direction = "assignquantity"
                
                note = "THE PRODUCT ALREADY EXIST IN SCANNED RECORD, PLEASE DELETE THE EXISTING PRODUCT TO SPECIFY NEW QUANTITY"
    
                return render_template("quantitycontrol.html", note = note, direction = direction, disable1 = disable1, disable2 = disable2, myipaddress = myipaddress)

            
            conn.close()
    
    
if __name__ == '__main__':
    
    albiemerapp.run(myipaddress)
    
    albiemerapp.run(debug=True, processes=cpu_count())
    
    #albiemerapp.run(debug=True)