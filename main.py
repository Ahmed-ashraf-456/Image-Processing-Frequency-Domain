import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, render_template,request, jsonify, redirect, session
import os
from PreProcessing import preprocessingImages
from processing import Processing
from After_Processing import After_Processing
import functions as fn

app = Flask(__name__)
UPLOAD_FOLDER = "./static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = 'sdef2222ddfwr1rbd2w235Y51@56I7'
app.config['SESSION_TYPE'] = 'filesystem'

@app.route("/",methods=['GET','POST'])
def index():
    output = "static/images/imag_final.jpg"
    global_first_path="./static/images/uniform.jpeg"
    global_second_path = "./static/images/uniform.jpeg"    
    path = "./static/images/uniform.jpeg"
    path_2 = "./static/images/uniform.jpeg"
    if session.get('global_second_path') is not None:
        global_first_path = session['global_first_path']
        global_second_path = session['global_second_path']
    if session.get('path') is not None:
        path = session['path'] 
        path_2 = session['path_2'] 
    else:
        path = "./static/images/uniform.jpeg"
        path_2 = "./static/images/uniform.jpeg"
    if session.get('output') is not None:
        output = session['output']
    # print("hereee", session['first_image_is_phase'],session['hp_checked'])
    # print(path,path_2)
    return render_template('index.html',path_to_first_pic=global_first_path,path_to_second_pic=global_second_path, phase_image= path, magnitude_image= path_2,output_image= output)

@app.route("/post",methods=['GET', 'POST'])
def post():
    hp_checked  = 1
    first_image_is_phase = 1
    # session['hp_checked'] = 1
    # session['first_image_is_phase'] = 0
    global_first_path="./static/images/uniform.jpeg"
    global_second_path = "./static/images/uniform.jpeg"

    if request.method == 'POST':
        if 'file1' in request.files:
            file1 = request.files['file1']
            first_path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
            file1.save(first_path)
            global_first_path = first_path
            session['global_first_path'] = global_first_path
        else:
            first_path = global_first_path
        if 'file2' in request.files:
            file2 = request.files['file2']
            second_path = os.path.join(app.config['UPLOAD_FOLDER'], file2.filename)
            file2.save(second_path)
            global_second_path = second_path
            session['global_second_path'] = global_second_path
        else:
            second_path = global_second_path
        try:
            hpBool = request.get_json("hpBool")
            hp_checked = hpBool['hpBool']
            session['hp_checked'] = hp_checked
            hp_checked=session['hp_checked']

        except:
             hp_checked=session['hp_checked']
        try:
            phaseBool = request.get_json("phaseBool")
            first_image_is_phase= phaseBool['phaseBool']
            session['first_image_is_phase'] = first_image_is_phase
            first_image_is_phase = session['first_image_is_phase']
            print("phase try ")
            print(first_image_is_phase)


        except:

            first_image_is_phase = session['first_image_is_phase']
            print("phase except ")

            print(first_image_is_phase)

    
        try:
            firstData = request.get_json("firstData")
            first_crop_array = firstData['firstData']
            final_first_crop_array = [first_crop_array[0], first_crop_array[3]]
            session['final_first_crop_array'] = final_first_crop_array
           

        except:
            final_first_crop_array = [[0,0],[600,600]]
        try:
            secondData = request.get_json("secondData")
            second_crop_array = secondData['secondData']
            final_second_crop_array = [second_crop_array[0], second_crop_array[3]]
            session['final_second_crop_array'] = final_second_crop_array
        except:
            final_second_crop_array = [[0,0],[600,600]]


        if session.get('global_first_path') is not None:
            global_first_path = session['global_first_path']

        if session.get('global_second_path') is not None:    
            global_second_path = session['global_second_path']

        if session.get('hp_checked') is not None:
            hp_checked = session['hp_checked']

        if session.get('first_image_is_phase') is not None:
            first_image_is_phase = session['first_image_is_phase'] 

        if session.get('final_first_crop_array') is not None:
            final_first_crop_array = session['final_first_crop_array']
            final_second_crop_array = session['final_second_crop_array']

        print("GLOBALSSS", global_first_path,global_second_path)   
        images = preprocessingImages(global_first_path, global_second_path)
        images.resizedImage()
        image1 , image2 = images.get_resized_image()

        img1 = Processing(image1 , final_first_crop_array , first_image_is_phase , hp_checked)
        img2 = Processing(image2 , final_second_crop_array  , int(not first_image_is_phase) , hp_checked)
        # print("YARABBBBBB",session['first_image_is_phase'] )
        path , data1 = img1.Edit_Signal()
        path_2 , data2 = img2.Edit_Signal()
        session['path'] = path
        session['path_2'] = path_2
        print("phaseee", first_image_is_phase)   
        print(final_first_crop_array,final_second_crop_array)
        final =After_Processing(data1 , data2 , first_image_is_phase).Inverse_Fourier_Transform()
        plt.imsave("static/images/imag_final.jpg" , final , cmap = 'gray')
        session['output']= "static/images/imag_final.jpg"
        return redirect("/")

if __name__ == '__main__':        

    app.run(debug=True)