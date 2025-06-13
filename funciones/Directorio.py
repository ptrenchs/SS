import os

class  Directorio:

    def __init__(self, rutas):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas

    def informacion_ruta(ruta):
        while True:
            ruta = ruta.replace('//','/')
            if '//' not in ruta:
                break
        if ruta[-1] == '/':
            ruta = ruta[:-1]
        ruta_split = ruta.split('/')
        nombre = ruta_split[-1]
        nombre_split = nombre.split('.')
        if 1 < len(nombre_split):
            nombre = '.'.join(nombre_split[:-1])
            extension = nombre_split[-1]
        else:
            extension = ''

        if len(ruta_split) == 1:
            carpeta =''
        else:
            carpeta = '/'.join(ruta_split[:-1])

        return carpeta,nombre,extension.lower()

    def ordenar_lista_num(lista):

        def num_inicio(nombre, fin = False):
            if fin:
                nombre = ''.join([i for i in nombre][::-1])
                for i,rt in enumerate(nombre):
                    if not rt.isnumeric():
                        if nombre[:i] == '':
                            return ''
                        return int(''.join([j for j in nombre[:i]][::-1]))
                        break

            else:
                for i,rt in enumerate(nombre):
                    if not rt.isnumeric():
                        if nombre[:i] == '':
                            return ''
                        return int(nombre[:i])
                        break
        
        # def Directorio.informacion_ruta(ruta):
        #     while True:
        #         ruta = ruta.replace('//','/')
        #         if '//' not in ruta:
        #             break
        #     if ruta[-1] == '/':
        #         ruta = ruta[:-1]
        #     ruta_split = ruta.split('/')
        #     nombre = ruta_split[-1]
        #     nombre_split = nombre.split('.')
        #     if 1 < len(nombre_split):
        #         nombre = '.'.join(nombre_split[:-1])
        #         extension = nombre_split[-1]
        #     else:
        #         extension = ''

        #     if len(ruta_split) == 1:
        #         carpeta =''
        #     else:
        #         carpeta = '/'.join(ruta_split[:-1])

        #     return carpeta,nombre,extension.lower()

        lista_ordenada = []
        lista_no_ordenada = [i for i in lista]
        num = []
        for lno in lista_no_ordenada:
            _,nombre,_ = Directorio.informacion_ruta(lno)
            nu = num_inicio(nombre = nombre, fin = False)
            if type(nu) == int:
                num.append(nu)

        num = sorted(num)
        for n in num:
            for lno in lista_no_ordenada:
                _,nombre,_ = Directorio.informacion_ruta(lno)
                if n == num_inicio(nombre = nombre, fin = False):
                    lista_ordenada.append(lno)
                    lista_no_ordenada.remove(lno)
                    # num.remove(n)
                    # break
            # num.append(num_inicio(nombre = nombre, fin = False))

        num = []
        for lno in lista_no_ordenada:
            _,nombre,_ = Directorio.informacion_ruta(lno)
            nu = num_inicio(nombre = nombre, fin = True)
            if type(nu) == int:
                num.append(nu)

        num = sorted(num)
        for n in num:
            for lno in lista_no_ordenada:
                _,nombre,_ = Directorio.informacion_ruta(lno)
                if n == num_inicio(nombre = nombre, fin = True):
                    lista_ordenada.append(lno)
                    lista_no_ordenada.remove(lno)
                    # num.remove(n)
                    # break
            # num.append(num_inicio(nombre = nombre, fin = False))
        return lista_ordenada + lista_no_ordenada

    def archivos(ruta):
        if os.path.isdir(ruta):
            return Directorio.ordenar_lista_num([os.path.join(ruta, item) for item in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, item))])
        else:
            return []
    
    def carpetas(ruta):
        if os.path.isdir(ruta):
            return Directorio.ordenar_lista_num([os.path.join(ruta, item) for item in os.listdir(ruta) if os.path.isdir(os.path.join(ruta, item))])
        else:
            return []
    
    def all_archivos(self):
        archivos_all = []
        lista = []
        rutas = [i for i in self.rutas]
        while rutas != []:
            for ruta in rutas:
                archivos_all += Directorio.archivos(ruta=ruta)
                lista += Directorio.carpetas(ruta=ruta)
            rutas = lista
            lista = []
        return archivos_all
    
    def all_carpetas(self):
        carpetas_all = []
        lista = []
        rutas = [i for i in self.rutas]
        while rutas != []:
            for ruta in rutas:
                lista += Directorio.carpetas(ruta=ruta)
            rutas = lista
            carpetas_all += lista
            lista = []
        return carpetas_all
    def crear_carpeta(ruta):
        if not os.path.exists(ruta):
            os.makedirs(ruta)
        return ruta
    
class Filtros_formato:
    def __init__(self, rutas, formatos= ''):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas
        if type(formatos)==str:
             formatos = (formatos.replace(' ','').replace('\t','').replace('.','')).split(',')
        self.formatos = formatos
    

    def elejir(self):
        new_lista = []
        if self.formatos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for formato in self.formatos:
                    formato_ruta = ruta.split('.')[-1]
                    if formato_ruta.lower() == formato.lower():
                        new_lista.append(ruta)
                        break
            return new_lista
    
    def eliminar(self):
        new_lista = []
        if self.formatos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for formato in self.formatos:
                    formato_ruta = ruta.split('.')[-1]
                    if formato_ruta.lower() == formato.lower():
                        break
                if not (formato_ruta.lower() == formato.lower()):
                    new_lista.append(ruta)
            return new_lista


class Filtros_carpetas:

    def __init__(self, rutas, carpetas = ''):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas
        if type(carpetas)==str:
             carpetas = (carpetas.replace(' ','').replace('\t','')).split(',')
        self.carpetas = carpetas


    def elejir(self):
        new_lista = []
        if self.carpetas == '':
            return self.rutas
        else:
            for ruta in self.rutas:
                for carpeta in self.carpetas:
                    if '/' + carpeta +'/' in ruta:
                        new_lista.append(ruta)
                        break
            return new_lista
        
    def eliminar(self):
        new_lista = []
        if self.carpetas == '':
            return self.rutas
        else:
            for ruta in self.rutas:
                for carpeta in self.carpetas:
                    if '/' + carpeta +'/' in ruta:
                        break

                if '/' + carpeta +'/' not in ruta:
                    new_lista.append(ruta)
            return new_lista
        
    
        
class Filtros_archivos:

    def __init__(self, rutas, archivos = ''):
        if type(rutas)==str:
             rutas = (rutas.replace(' ','').replace('\t','')).split(',')
        self.rutas = rutas
        if type(archivos)==str:
             archivos = (archivos.replace(' ','').replace('\t','')).split(',')
        self.archivos = archivos

    def elejir(self):
        new_lista = []
        if self.archivos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for arch in self.archivos:
                    nombre_archivo = '.'.join(os.path.basename(ruta).split('.')[:-1])
                    if nombre_archivo == arch:
                        new_lista.append(ruta)
                        break
            return new_lista
    
    def eliminar(self):
        new_lista = []
        if self.archivos == '':
            return new_lista
        else:
            for ruta in self.rutas:
                for arch in self.archivos:
                    nombre_archivo = '.'.join(os.path.basename(ruta).split('.')[:-1])
                    if nombre_archivo == arch:
                        break
                if not (nombre_archivo == arch):
                    new_lista.append(ruta)
            return new_lista