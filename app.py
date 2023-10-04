from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


#http://127.0.0.1:5000/

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)

@app.route('/my-link/')
def my_link():
    import cv2 as cv
    import numpy as np
    import time
    import serial
    
    ser = serial.Serial('COM6 ', 9600)

    
    cap0 = cv.VideoCapture(0)
    cap1 = cv.VideoCapture(1)
    cap2 = cv.VideoCapture(2)
    cams=[cap0,cap1,cap2]
    
    time.sleep(2)   
    ser.write(b'1') 
    ser.write(b'1')
    ser.write(b'1') 
    
    for i in cams:
        i.set(cv.CAP_PROP_FRAME_WIDTH, 100)
        i.set(cv.CAP_PROP_FRAME_HEIGHT, 100)
        width = i.get(cv.CAP_PROP_FRAME_WIDTH)
        height = i.get(cv.CAP_PROP_FRAME_HEIGHT)
    suneliveri=0
    bugdayveri=0
    time.sleep(0.1)
    
    while cap0.isOpened():
        ret0, frame01 = cap0.read() 
        ret0, frame02 = cap0.read()
        a=0
        for i in cams:
            diff = cv.absdiff(frame01, frame02)
            diff_gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(diff_gray, (5, 5), 0)
            _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
            dilated = cv.dilate(thresh, None, iterations=3)
            contours, _ = cv.findContours(
                dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            #********** hareket algılama ile bugday sayimi********
            for contour in contours:
                (x, y, w, h) = cv.boundingRect(contour)
                if cv.contourArea(contour) < 2200:#-------------değişken
                    continue
                cv.rectangle(frame01, (x, y), (x+w, y+h), (0, 255, 0), 2)
                #cv.drawContours(frame1, contours, -1, (0, 255, 0), 2)
                cv.putText(frame01, "durum: {}".format('hareket'), (10, 20), 
                           cv.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 3)
                bugdayveri += 1
            ret, img = i.read()
            cv.imshow('Bugday Ayirici-'+str(a),img)
            cam = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
            scale=20
            height, width = cam.shape
            centerX,centerY=int(height/2),int(width/2)
            radiusX,radiusY= int(scale*height/100),int(scale*width/100)
            minX,maxX=centerX-radiusX,centerX+radiusX
            minY,maxY=centerY-radiusY,centerY+radiusY
            cropped = cam[minX:maxX, minY:maxY]
            resized_cropped = cv.resize(cropped, (width, height)) 
            cam = resized_cropped
            cv.imshow('Bugday Ayirici filtreli-'+str(a),cam)
            ret,cam = cv.threshold(cam,123,255,0)#-------------değişken
            cam2 = cam.copy()
            #****************************analiz***********************
            contours, hier = cv.findContours(cam,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                if 20<cv.contourArea(cnt)<200:#-------------değişken
                    (x,y,w,h) = cv.boundingRect(cnt)
                    cv.rectangle(cam2,(x,y),(x+w,y+h),0,-1)
            #****************************tespit***********************
            print("\nsayilan bugday miktari= ",  bugdayveri)
            beyazpx = np.sum(cam2 == 255)
            siyahpx = np.sum(cam2 == 0)
            print('beyaz pixel sayisi:', beyazpx)
            print('siyah pixel sayisi:', siyahpx)
            if beyazpx>2000:#--------------------------------değişken
                suneliveri += 1
                print("suneli bugday miktari = ",suneliveri)
            cv.imshow('Bugday Ayirici sonuc-'+str(a),cam2)
            a=a+1
            print(a)
        if cv.waitKey(50) == 27:
            break
        if bugdayveri>50:
            break
    if bugdayveri>0:
        kalite=suneliveri/bugdayveri
        print("\ntoplam bugday= ",bugdayveri,"  suneli bugday= ",suneliveri,
              "\nbugday kalitesi (sune orani)= %",kalite)
    else:
        print("bugday verisi okunmadı")
        kalite=0
    cv.destroyAllWindows()
    
    time.sleep(3) 
    ser.write(b'0') 
    ser.write(b'0') 
    ser.write(b'0') 
    
    kalite= "{:.2f}".format(kalite*10)
    print ("xxx: ",kalite)		
    return render_template('index.html', oran=kalite)

if __name__ == "__main__":
    app.run(debug=True)
