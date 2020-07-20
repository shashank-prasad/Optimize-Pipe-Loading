import Optimizing as op
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/result',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        data= op.Optimize_loading(path= result['path'],
                         height_limit=result['ht_limit'], 
                         weight_limit=result['wt_limit'],
                         width_limit=result['wd_limit'] )

        
        return render_template("result.html", data=data)
    else:
        return "GET RESULT"
    

@app.errorhandler(500)
def page_not_found(e):
    err="""
    <style type="text/css">
    body{
      background: #ff3333;
    }
  </style>
</head>
<body>
<h1>Something went Wrong!</h1>
<h3>Possible errors:</h3>
<p>1) Incorrect Path or File not found , check path again. </p>
<p>2) Non-numeric Inputs given to height,width and weight limits. Check for special characters too.</p>
<p>3) Check the CSV file,if it is in the proper format.</p>
<p>4) If still doesn't work. Contact developer!  </p>
 </body>   
    """
    return err


if __name__ == '__main__':
    app.run()
