from flask import Flask, request, render_template
from confiDB import * #Importando conexion BD
from flask_cors import CORS  # Importa Flask-CORS

app = Flask(__name__) 
CORS(app) 

@app.route('/') 
def inicio(): 
     return render_template('public/index.html')


@app.route('/form', methods=['GET', 'POST'])
def registrarForm():
    if request.method == 'POST':
        nombreJ         = request.form['nombre']
        posicionJ       = request.form['posicion']
        nacimientoJ     = request.form['nacimiento']
        biografiaJ      = request.form['biografia']
        
        conexion_MySQLdb = connectionBD()
        cursor           = conexion_MySQLdb.cursor(dictionary=True)
        
            
        sql         = ("INSERT INTO jugadoras(nombre, posicion, nacimiento, biografia) VALUES (%s, %s, %s, %s)")
        valores     = (nombreJ, posicionJ, nacimientoJ, biografiaJ)
        cursor.execute(sql, valores)
        conexion_MySQLdb.commit()
        
        cursor.close() #Cerrando conexion SQL
        conexion_MySQLdb.close() #cerrando conexion de la BD
        msg = 'Registro con exito'
        
        print(cursor.rowcount, "registro insertado")
        print("1 registro insertado, id", cursor.lastrowid)
  
        return render_template('public/index.html', msg='Formulario enviado')
    else:
        return render_template('public/index.html', msg = 'Metodo HTTP incorrecto')


if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000, debug=True)