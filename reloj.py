from tkinter import Label, Tk
import time 


#Todas estas son las funciones que sirven para darle las "ordenes y configuraciones" a la ventana flotante 

ventana = Tk ()    #Esta cosa esa para darle la "accion " de que se genere una ventana 
ventana.config(bg='gray')  #Esta cosa es para darle la cofiguracion a la ventana 
ventana.geometry('500x200')  #Con esta cosa damos el tamaño que queremos que tenga la ventana 
ventana.wm_attributes('-transparentcolor','gray')   #Se supone que lo que hace es de que todos los colores que sean grises lo cambia...
#a transparente, entonces el gris no se vereia por que lo estariamos cambiando a "transparente"
ventana.overrideredirect(1)  #Esta cosa lo que hace es que elimina todas las barras de comando como maximizar, cerrar y minimizar 

#Acciones:
#DEF: Es para definir las funciones que queremos que se creen, es como el "public funcion() del PHP"

def salir(*args):
    ventana.destroy()
    ventana.quit()

def obtener_tiempo():
    #todas estas cosas son variables:
    hora = time.strftime('%H:%M:%S')    #Este es el metodo que obtiene la hora (hora, minutos y segundos)
    zona = time.strftime('%Z')      #Esta es la que optiene la zona horaira
    fecha_formato12 = time.strftime('%A %d %B %Y')    #Este es el metodo que obtiene el dia mes y año 

#todas estas cosas son "labels (etiquetas)"
    texto_hora['text'] = hora 
    texto_fecha12['text'] = fecha_formato12
    zona_horaria['text'] = zona 
    texto_hora.after(1000, obtener_tiempo)


#Estas son funciones que nois permiten mover la ventana para todos lados. 

def start(event):
    global x, y
    x = event.x
    y = event.y

def stop(event):
    x = None
    y = None

def mover(event):
    global x, y 
    deltax = event.x - x
    deltay = event.y - y
    ventana.geometry(f"+{ventana.winfo_x() + deltax}+{ventana.winfo_y() + deltay}")
    ventana.update()


#funcion que nos permite controlar los botones 
ventana.bind("<ButtonPress-1>",start) #Es la que se encarga de dar la respuesta para el boton izquiero 
ventana.bind("<ButtonRelease-1>",stop) #monitorea la funcion de respuesta de operacion de la liberacion del boton izquierdo
ventana.bind("<B1-Motion>",mover) #Funcion de respuesta de movimineto del mouse del al monitor 
ventana.bind("<KeyPress-Escape>", salir) 

texto_hora = Label(ventana, fg= 'white', bg='gray', font= ('Star Jedi Hollow',50, 'bold'), width=10) 
texto_hora.grid(column=0, row=0, ipadx=1, ipady=1)

texto_fecha12 = Label(ventana, fg = 'white', bg='gray', font = ('Vivaldi',20, 'bold'))
texto_fecha12.grid(column=0, row=1)

zona_horaria = Label(ventana, fg= 'white', bg='gray', font = ('Lucida Sans',12))
zona_horaria.grid(column = 0, row=2)

obtener_tiempo()
ventana.mainloop()
