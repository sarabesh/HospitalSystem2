

from flask import Flask, flash, redirect, render_template, request, session, abort

from  flaskext.mysql import   MySQL
from  flask_uploads   import  UploadSet, configure_uploads, IMAGES
from  random import randint


app=Flask(__name__,static_url_path="/static")
app.secret_key='ironman'
#api=Api(app)
mysql=MySQL()


app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='HosInfSys'
app.config['MYSQL_DATABASE_HOST']='localhost'
mysql.init_app(app)




@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return render_template('upload.html')



@app.route('/')
def home():
    return render_template("home.html")

def idgen():
    try:
            conn=mysql.connect()
            cursor=conn.cursor()
    except Exception as e:
            return{'error':str(e)} 

    id=randint(0, 1000)
    select_stmt=("SELECT * FROM patient WHERE id=%s")
    select_data=(id)
            #cursor.callproc('spCreatePatient',(_userName,_userPassword,111,_userSex,_userAge,_userAddress,_userPhone,_userWard,_userDate))
            #cursor.execute(    "INSERT INTO patient VALUES ('"+'1'+"','"+_user))   
    cursor.execute(select_stmt,select_data)
            #data=cursor.fetchone()
    data=cursor.fetchall()
    if len(data) is 0:
            return id
    else:
            return idgen()






@app.route('/admin')
def admin():   
    conn=mysql.connect()
    cursor=conn.cursor()
    patstmt=("SELECT * FROM patient")
    cursor.execute(patstmt)
    pats=cursor.fetchall()
    patlist=list(pats)
    pno=len(patlist)

    stafstmt=("SELECT * FROM staff")
    cursor.execute(stafstmt)
    stafs=cursor.fetchall()
    staflist=list(stafs)
    sno=len(staflist)

    ICUstafstmt=("SELECT * FROM staff WHERE profession=%s")
    stad=('doctorICU')
    cursor.execute(ICUstafstmt,stad)
    stafs=cursor.fetchall()
    ICUstaflist=list(stafs)

    norstafstmt=("SELECT * FROM staff WHERE profession=%s")
    stad=('doctornor')
    cursor.execute(norstafstmt,stad)
    stafs=cursor.fetchall()
    norstaflist=list(stafs)

    outstafstmt=("SELECT * FROM staff WHERE profession=%s")
    stad=('doctorout')
    cursor.execute(outstafstmt,stad)
    stafs=cursor.fetchall()
    outstaflist=list(stafs)

    labstafstmt=("SELECT * FROM staff WHERE profession=%s")
    stad=('lab')
    cursor.execute(labstafstmt,stad)
    stafs=cursor.fetchall()
    labstaflist=list(stafs)

    manstafstmt=("SELECT * FROM staff WHERE profession=%s")
    stad=('manager')
    cursor.execute(manstafstmt,stad)
    stafs=cursor.fetchall()
    manstaflist=list(stafs)
  
  


    surgstmt=("SELECT * FROM operation")
    cursor.execute(surgstmt)
    surts=cursor.fetchall()
    surtlist=list(surts)
    suno=len(surtlist)


    intstmt=("SELECT DISTINCT * FROM invoice")
    cursor.execute(intstmt)
    ints=cursor.fetchall()
    intlist=list(ints)
    int_cost=0
    for i in intlist:
        int_cost+=int(i[3])

    Lab_cost=("SELECT DISTINCT * FROM invoice WHERE type='Lab_Test'")
    cursor.execute(Lab_cost)
    labs=cursor.fetchall()
    labclist=list(labs)
    lab_cos=0
    for i in labclist:
        lab_cos+=int(i[3])

    surg_cost=("SELECT DISTINCT * FROM invoice WHERE type='Surgery/operation'")
    cursor.execute(surg_cost)
    labs=cursor.fetchall()
    labclist=list(labs)
    surg_cos=0
    for i in labclist:
        surg_cos+=int(i[3])
        
    room_cost=("SELECT DISTINCT * FROM invoice WHERE type='room'")
    cursor.execute(room_cost)
    labs=cursor.fetchall()
    labclist=list(labs)
    room_cos=0
    for i in labclist:
        room_cos+=int(i[3])        


    return render_template("/admin.html",**locals())    

@app.route('/GetCollege',methods=['POST'])
def GetCollege():
    gre=request.form['gre']
    gpa=request.form['gpa']
    lang=request.form['lang']
    def predict(X_train, y_train, x_test, k):
    # create list for distances and targets
        distances = []
        targets = []

        for i in range(len(X_train)):
        # first we compute the euclidean distance
            distance = np.sqrt(np.sum(np.square(x_test - X_train.values[i, :])))
        # add it to list of distances
            distances.append([distance, i])

    # sort the list
        distances = sorted(distances)
   
    # make a list of the k neighbors' targets
        i=0
        while len(list(set(targets)))<k:
            index=distances[i][1]
            val=y_train[index]
            i=i+1
            targets.append(val)
  
    return list(set(targets))

  
    df = pd.read_csv("gredataset.csv")
    X=df.iloc[:,[1,2,3]]
    labels=df.iloc[:,[0]]

    from sklearn.preprocessing import LabelEncoder
    le_X=LabelEncoder()
    labels.values[:,0]=le_X.fit_transform(labels.values[:,0])




    labelVal=labels.values.ravel()
    labelVal=labelVal.astype('int')


    Xt=([gre,lang,gpa])
    fin=predict(X,labelVal,Xt,8)
    for op in fin:
        i=labels.index[labels['name'] == op].tolist()
        i=i[0]
        print(df.iloc[i,0])


@app.route('/Insert_patient',methods=['POST'])
def Insert_patient():
    if request.method == 'POST' and 'photo' in request.files:
            filename = photos.save(request.files['photo'])

    else:
        pid=0
        message="image not uploaded"
        return render_template('/diag_res.html',**locals())        
    _userName=request.form['name']
    _userPassword=request.form['password']
    _userSex=request.form['sex']
    _userAge=request.form['age']
    _userPhone=request.form['phone']
    _userDate=request.form['date']
    _userWard=request.form['ward']
    _userAddress=request.form['address']
    i=idgen()
    conn=mysql.connect()
    cursor=conn.cursor()
    check_stmt=("SELECT * FROM patient WHERE Name=%s")
    check_data=(_userName)
    cursor.execute(check_stmt,check_data)
    checkd=cursor.fetchall()
    if len(checkd)>0:
        return render_template('login_fail.html',message='name already exists')
    else:    
            insert_stmt=("INSERT INTO patient VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            insert_data=(i,_userName,_userPassword,_userAge,_userSex,_userAddress,_userPhone,_userDate,_userWard)
            #cursor.callproc('spCreatePatient',(_userName,_userPassword,111,_userSex,_userAge,_userAddress,_userPhone,_userWard,_userDate))
            #cursor.execute(    "INSERT INTO patient VALUES ('"+'1'+"','"+_user))   
            cursor.execute(insert_stmt,insert_data)
            #data=cursor.fetchone()
            data=cursor.fetchall()

           
            #return{'name':args['name'],'password':args['password']}
            try:
                img_ins=("INSERT INTO imagetbl VALUES (%s,%s,%s)")
                img_data=(i,'/static/patients/',filename)
                cursor.execute(img_ins,img_data)

            except Exception as e:
                message=e
                return render_template('login_fail.html',**locals())      

            if len(data) is 0:
                conn.commit()
                imgpath='/static/patients/'+filename
                conn=mysql.connect()
                cursor=conn.cursor()
                view_stmt=("SELECT * FROM patient WHERE password=%s AND Name=%s")
                view_data=(_userPassword,_userName)
                cursor.execute(view_stmt,view_data)
                data=cursor.fetchall()
                pid=data[0][0]
                pname=data[0][1]
                ppswd=data[0][2]
                page=data[0][3]
                psex=data[0][4]
                paddr=data[0][5]
                pphn=data[0][6]
                pdate=data[0][7]
                pward=data[0][8]    
                return render_template('view.html',**locals())

            else:
                return{'status':'failure','msf':str(data[0])}







@app.route('/Show',methods=['POST'])
def Show():
    _userName=request.form['name']
    _userPassword=request.form['password']
    conn=mysql.connect()
    cursor=conn.cursor()
    view_stmt=("SELECT * FROM patient WHERE password=%s AND Name=%s")
    view_data=(_userPassword,_userName)
    cursor.execute(view_stmt,view_data)
    data=cursor.fetchall()
    if len(data) is 0:
        pid=0
        message="login failed! try again"
        return render_template('login_fail.html',**locals())
    else:    
        pid=data[0][0]
    

        view_img=("SELECT * FROM imagetbl WHERE pid=%s")
        view_idata=(pid)
        cursor.execute(view_img,view_idata)

        img=cursor.fetchall()

        diag_stmt=("SELECT * FROM diagnosis WHERE pid=%s")
        diag_data=(pid) 
        cursor.execute(diag_stmt,diag_data)

        diag_res=cursor.fetchall()

        room_stmt=("SELECT * FROM ward WHERE pid=%s")
        room_data=(pid)
        cursor.execute(room_stmt,room_data)
        room_res=cursor.fetchall()
  #  room_res=list(room_result)

        lab_stmt=("SELECT * FROM lab WHERE lid=%s")
        diag_data=(pid) 
        cursor.execute(lab_stmt,diag_data)
    
        lab_result=cursor.fetchall()
        lab_res=list(lab_result)

        if len(diag_res) is 0:
            pdiag="no diagnosis"
            pdiadate=" "
        else:            
            pdiag=diag_res[0][1]
            pdiadate=diag_res[0][2]    
        imgpath=(img[0][1]+img[0][2])
        pname=data[0][1]
        ppswd=data[0][2]
        page=data[0][3]
        psex=data[0][4]
        paddr=data[0][5]
        pphn=data[0][6]
        pdate=data[0][7]
        pward=data[0][8]
        pid=data[0][0]
    #roomno=room_res[0][1]+room_res[0][2]
        op_stmt=("SELECT * FROM operation WHERE pid=%s")
        op_data=(pid)
        cursor.execute(op_stmt,op_data)
        op_res=cursor.fetchall()
        op_result=list(op_res)
   

        inv_stmt=("SELECT DISTINCT * FROM invoice WHERE pid=%s")
        inv_data=(pid)
        cursor.execute(inv_stmt,inv_data)
        inv_res=cursor.fetchall()
        inv_result=list(inv_res)
        return render_template('view.html',**locals())








@app.route('/Stafflogin',methods=['POST'])
def stafflog():
    
    _userName=request.form['name']
    _userPassword=request.form['password']
    
    conn=mysql.connect()
    cursor=conn.cursor()
    view_stmt=("SELECT * FROM staff WHERE password=%s AND name=%s")
    view_data=(_userPassword,_userName)
    cursor.execute(view_stmt,view_data)
    data=cursor.fetchall()
    if len(data) is 0:
        pid=0
        message="login failed! try again"
        return render_template('login_fail.html',**locals())
    else:    
          sid=data[0][0]
          prof=data[0][3]
          session['prof']=prof
          if prof=='doctorICU':
                ward='ICU'
          elif prof=='doctornor':
                ward='normal'    
          elif prof=='doctorout':
                ward='out'
          elif prof=='lab':
                ward='all'
          elif prof=='admin':
                return redirect('/admin')     
          else :
               ward='room' 

          if ward=='all':
               view_stmt2=("SELECT * FROM patient")
               cursor.execute(view_stmt2)
               datatup=cursor.fetchall()
               datali=[]
               for i in datatup:
                    view_img=("SELECT imagename FROM imagetbl WHERE pid=%s")
                    id=i[0]
                    view_data2=(id)
                    cursor.execute(view_img,view_data2)
                    img=cursor.fetchone()
            #imgli=list(str(img))
            #imgpathtup=str(imgli)
            #imgpath=list(imgpathtup)
            #imgname=str(imgli[0][1])
                    pth="/static/patients/"
                    nm=str(img)
                    nm=nm[3:-3]
                    datadict={
                    'id':i[0],
                    'name':i[1],
                    'ward':i[8],
                    'phone':i[6],
                    'address':i[5],
                    'imagepath':pth,
                    'imagename':nm
                    }
                    datali.append(datadict)
               return render_template('patient_list.html',**locals())

          elif ward=='room':
               view_stmt3=("SELECT * FROM patient WHERE ward=%s OR ward=%s")
               view_data3=('ICU','normal')
               cursor.execute(view_stmt3,view_data3)
               datatup=cursor.fetchall()
               datali=[]
               for i in datatup:
                    view_img=("SELECT imagename FROM imagetbl WHERE pid=%s")
                    id=i[0]
                    view_data2=(id)
                    cursor.execute(view_img,view_data2)
                    img=cursor.fetchone()
            #imgli=list(str(img))
            #imgpathtup=str(imgli)
            #imgpath=list(imgpathtup)
            #imgname=str(imgli[0][1])
                    pth='/static/patients/'
                    nm=str(img)
                    nm=nm[3:-3]
                    datadict={
                    'id':i[0],
                    'name':i[1],
                    'ward':i[8],
                    'phone':i[6],
                    'address':i[5],
                    'imagepath':pth,
                    'imagename':nm
                    }
                    datali.append(datadict)
               return render_template('patient_list.html',**locals())
          
          else :
               view_stmt4=("SELECT * FROM patient WHERE ward=%s")
               view_data4=(ward)
               cursor.execute(view_stmt4,view_data4)
               datatup=cursor.fetchall()
               datali=[]
               for i in datatup:
                    view_img=("SELECT imagename FROM imagetbl WHERE pid=%s")
                    id=i[0]
                    view_data2=(id)
                    cursor.execute(view_img,view_data2)
                    img=cursor.fetchone()
            #imgli=list(str(img))
            #imgpathtup=str(imgli)
            #imgpath=list(imgpathtup)
            #imgname=str(imgli[0][1])
                    pth='/static/patients/'
                    nm=str(img)
                    nm=nm[3:-3]
                    datadict={
                    'id':i[0],
                    'name':i[1],
                    'ward':i[8],
                    'phone':i[6],
                    'address':i[5],
                    'imagepath':pth,
                    'imagename':nm
                    }
                    datali.append(datadict)
               return render_template('patient_list.html',**locals()) 


def checki(rm,bk):
    try :
        conn=mysql.connect()
        cursor=conn.cursor()
        check_stmt=("SELECT * FROM ward WHERE block=%s AND room=%s")
        check_data=(bk,rm)
        cursor.execute(check_stmt,check_data)
        data=cursor.fetchall()

        if len(data) is 0:
            return bk+rm
        
                    
    except Exception as e:
        return{'error':str(e)} 

    
@app.route('/room_set',methods=['POST'])
def room_set():
     pid=request.form['id']
     a=[]
     b=[]
     c=[]
     d=[]
     for i in range(1,11):
        a.append(checki(str(i),'a'))
     for i in range(1,21):
        b.append(checki(str(i),'b'))
     for i in range(1,41):
        c.append(checki(str(i),'c'))
     for i in range(1,100):
        d.append(checki(str(i),'d'))               
     return render_template('/room_view.html',**locals())
            
            
            
       





@app.route('/expand',methods=['POST'])
def expand():
    conn=mysql.connect()
    cursor=conn.cursor()
    sname=request.form['sname']
    spass=request.form['spass']
    pid=request.form['id']
    view_stmt=("SELECT * FROM patient WHERE id=%s")
    view_data=(pid)
    cursor.execute(view_stmt,view_data)
    data=cursor.fetchall()
    if len(data) is 0:
     return "<hr><br>no such patient, wrong pid</hr>"
    view_img=("SELECT * FROM imagetbl WHERE pid=%s")
    view_idata=(pid)
    cursor.execute(view_img,view_idata)

    img=cursor.fetchall()

    diag_stmt=("SELECT * FROM diagnosis WHERE pid=%s")
    diag_data=(pid) 
    cursor.execute(diag_stmt,diag_data)

    diag_res=cursor.fetchall()

    room_stmt=("SELECT * FROM ward WHERE pid=%s")
    room_data=(pid)
    cursor.execute(room_stmt,room_data)
    room_res=cursor.fetchall()

    
    a=[]
    b=[]
    c=[]
    d=[]
    for i in range(1,11):
        a.append(checki(str(i),'a'))
    for i in range(1,21):
        b.append(checki(str(i),'b'))
    for i in range(1,41):
        c.append(checki(str(i),'c'))
    for i in range(1,100):
        d.append(checki(str(i),'d'))    
  #  room_res=list(room_result)


    lab_stmt=("SELECT * FROM lab WHERE lid=%s")
    diag_data=(pid) 
    cursor.execute(lab_stmt,diag_data)
    
    lab_result=cursor.fetchall()
    lab_res=list(lab_result)

    if len(diag_res) is 0:
            pdiag="no diagnosis"
            pdiadate=" "
    else:            
            pdiag=diag_res[0][1]
            pdiadate=diag_res[0][2]    
    
    if len(img) is 0:
        img='no img'
    else:
        imgpath=(img[0][1]+img[0][2])
    pname=data[0][1]
    ppswd=data[0][2]
    page=data[0][3]
    psex=data[0][4]
    paddr=data[0][5]
    pphn=data[0][6]
    pdate=data[0][7]
    pward=data[0][8]
    pid=data[0][0]
    ppas=data[0][0]


    op_stmt=("SELECT * FROM operation WHERE pid=%s")
    op_data=(pid)
    cursor.execute(op_stmt,op_data)
    op_res=cursor.fetchall()
    op_result=list(op_res)
   

    inv_stmt=("SELECT DISTINCT * FROM invoice WHERE pid=%s")
    inv_data=(pid)
    cursor.execute(inv_stmt,inv_data)
    inv_res=cursor.fetchall()
    inv_result=list(inv_res)
    #roomno=room_res[0][1]+room_res[0][2]
    return render_template('expand.html',**locals())


@app.route('/new_diagnosis',methods=['POST'])
def diag(): 
    pid=request.form['id']
    diag=request.form['dia']  
    date=request.form['date']
    sname=request.form['sname']
    spass=request.form['spass']
    conn=mysql.connect()
    cursor=conn.cursor()
    check_stmt=("SELECT * FROM diagnosis WHERE pid=%s");
    check_data=(pid)
    cursor.execute(check_stmt,check_data)
    data=cursor.fetchall()

    if len(data) is 0:
        
        cursor2=conn.cursor()
        insert_stmt5=("INSERT INTO diagnosis VALUES (%s,%s,%s)")
        insert_data5=(pid,diag,date)
        cursor2.execute(insert_stmt5,insert_data5)
        data=cursor2.fetchall()
        conn.commit()
        message="diagnosis inserted"
        return render_template('diag_res.html',**locals())
    else:
        cursor3=conn.cursor()   
        update_stmt5=("UPDATE diagnosis SET diagnosis=%s WHERE pid=%s")
        update_data5=(diag,pid)
        cursor3.execute(update_stmt5,update_data5)
        update_stmt5=("UPDATE diagnosis SET Adate=%s WHERE pid=%s")
        update_data5=(date,pid)
        cursor3.execute(update_stmt5,update_data5)
        
        conn.commit()
        
        message="diagnosis updated"
        return render_template('diag_res.html',**locals())        


@app.route('/room_alloc',methods=['POST'])
def room():
    conn=mysql.connect()
    cursor=conn.cursor()
    sname=request.form['sname']
    spass=request.form['spass']
    pname=request.form['pname']
    ppass=request.form['ppass']
    pid=request.form['id']
    rm=request.form['room']
    bl=request.form['block']
    Ch_stmt=("SELECT * FROM ward WHERE room=%s AND block=%s")
    ch_data=(rm,bl)
    cursor.execute(Ch_stmt,ch_data)
    data=cursor.fetchall()
    if len(data) is 0:
        ins_stmt=("INSERT INTO ward VALUES (%s,%s,%s)")
        ins_data=(pid,bl,rm)
        cursor.execute(ins_stmt,ins_data)
        conn.commit()
        message="Room booked"
        return render_template('/diag_res.html',**locals())
    else:   
        message="Room already booked"
        return render_template('/diag_res.html',**locals())    

@app.route('/new_test',methods=['POST'])
def new_test():
    conn=mysql.connect()
    cursor=conn.cursor()
    spec=request.form['spec']
    test=request.form['test']
    res=request.form['res']
    ref=request.form['ref']
    date=request.form['date']
    pid=request.form['id']
    sname=request.form['sname']
    spass=request.form['spass']
    #return pid+spec+ref+date
    ins_stmtlab=("INSERT INTO lab VALUES (%s,%s,%s,%s,%s,%s)")
    ins_datalab=(pid,spec,test,res,ref,date)
    cursor.execute(ins_stmtlab,ins_datalab)
    conn.commit()
    message="Test inserted"
    return render_template('/diag_res.html',**locals())





def sgen():
    try:
            conn=mysql.connect()
            cursor=conn.cursor()
    except Exception as e:
            return{'error':str(e)} 

    id=randint(0, 1000)
    select_stmt=("SELECT * FROM operation WHERE sid=%s")
    select_data=(id)
            #cursor.callproc('spCreatePatient',(_userName,_userPassword,111,_userSex,_userAge,_userAddress,_userPhone,_userWard,_userDate))
            #cursor.execute(    "INSERT INTO patient VALUES ('"+'1'+"','"+_user))   
    cursor.execute(select_stmt,select_data)
            #data=cursor.fetchone()
    data=cursor.fetchall()
    if len(data) is 0:
            return id
    else:
            return sgen()


@app.route('/new_surgery',methods=['POST'])
def new_surg():
    conn=mysql.connect()
    cursor=conn.cursor()
    did=request.form['sid']
    name=request.form['name']
    cost=request.form['cost']
    sname=request.form['sname']
    spass=request.form['spass']
    date=request.form['date']
    pid=request.form['id']
    sid=sgen();
    #return pid+spec+ref+date
    ins_stmtlab=("INSERT INTO operation VALUES (%s,%s,%s,%s,%s,%s)")
    ins_datalab=(sid,pid,did,name,date,cost)
    cursor.execute(ins_stmtlab,ins_datalab)
    conn.commit()
    message="Test inserted"
    return render_template('/diag_res.html',**locals())


@app.route('/invoice',methods=['POST'])
def invoice():
    conn=mysql.connect()
    cursor=conn.cursor()
    pid=request.form['pid']
    sname=request.form['sname']
    spass=request.form['spass']
    search_lab=("SELECT * FROM lab WHERE lid=%s")
    search_labd=(pid)
    cursor.execute(search_lab,search_labd)
    lab_result=cursor.fetchall()
    lab_res=list(lab_result)
    
    for i in lab_res:
        name="Lab_Test"
        cost=500
        ins_stmt=("INSERT INTO invoice VALUES (%s,%s,%s,%s,%s)")
        ins_data=(i[0],name,i[2],cost,i[5])
        cursor.execute(ins_stmt,ins_data)
        conn.commit()
   
    search_room=("SELECT * FROM ward WHERE pid=%s")
    search_roomd=(pid)
    cursor.execute(search_room,search_roomd)
    ward_res=cursor.fetchall()
    room_cost=0
    if len(ward_res) is 0:
        room_cost=0
    elif ward_res[0][1]=="a":
        room_cost=80000
    elif ward_res[0][1]=="b":
        room_cost=50000
    elif ward_res[0][1]=="c":
        room_cost=10000
    else:
        room_cost=5000
    name="room_alloc"
    rtype="room"
    rdate="-"

    ins_stmtw=("INSERT INTO invoice VALUES (%s,%s,%s,%s,%s)")
    ins_dataw=(pid,rtype,name,room_cost,rdate)
    cursor.execute(ins_stmtw,ins_dataw)
    

    search_surg=("SELECT * FROM operation WHERE pid=%s")
    search_surgd=(pid)
    cursor.execute(search_surg,search_surgd)
    surg_res=cursor.fetchall()
    surg_result=list(surg_res)
    
    for i in surg_result:
        ins_stmts=("INSERT INTO invoice VALUES (%s,%s,%s,%s,%s)")
        ins_datas=(pid,"Surgery/operation",i[3],i[5],i[4])
        cursor.execute(ins_stmts,ins_datas)
        conn.commit()

   
    conn.commit()
    message="Invoice generated"
    return render_template('/diag_res.html',**locals())    





if __name__=='__main__':
    app.run(host='0.0.0.0',port=80,debug=True)
                
         