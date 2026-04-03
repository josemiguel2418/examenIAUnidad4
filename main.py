import csv
import os

def get_precios_colmados():
    datos = []
    nombre_archivo = 'lista_compras.csv'
    with open(nombre_archivo, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for fila in csv_reader:
            fila['precio'] = float(fila['precio'])
            datos.append(fila)
    return datos

def get_lista_compras():
    datos = []
    nombre_archivo = 'precios_colmados.csv'
    with open(nombre_archivo, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for fila in csv_reader:
            fila['cantidad'] = float(fila['cantidad'])
            datos.append(fila)
    return datos

def escribir_archivo_salida(nombre_archivo,datos):

    if not os.path.exists('salida'):
        os.makedirs('salida')

    archivo_salida = f"salida/{nombre_archivo}"
    with open(archivo_salida, mode='w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=datos[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(datos)
    

def recomendar_ahorro(barrio_seleccionado):
    
    
    precios_colmados = get_precios_colmados()
    lista_compras = get_lista_compras()

    precios_barrio = [fila for fila in precios_colmados if fila['barrio'].lower() == barrio_seleccionado.lower()]

    resultados = []
    total_compra = 0
    ahorro_total = 0

    print(f"******** Recomendación para {barrio_seleccionado} ********")

    for item in lista_compras:
        producto_buscado = item['producto'].lower()
        categoria_buscada = item['categoria'].lower()
        cantidad = item['cantidad']

        
        productos_seleccionados = [fila for fila in precios_barrio if fila['producto'].lower() == producto_buscado]

        if productos_seleccionados:
            
            producto_mas_barato = min(productos_seleccionados, key=lambda producto: producto['precio'])
                      
            precios_productos = [producto['precio'] for producto in productos_seleccionados]
            promedio = sum(precios_productos) / len(precios_productos)
            
            ahorro_total_producto = (promedio - producto_mas_barato['precio']) * cantidad
            costo_total_producto = producto_mas_barato['precio'] * cantidad
            
            resultados.append({
                'producto': producto_mas_barato['producto'],
                'marca': producto_mas_barato['marca'],
                'colmado': producto_mas_barato['colmado'],
                'precio': producto_mas_barato['precio'],
                'costo_total': costo_total_producto,
                'sugerencia': "Producto exacto encontrado"
            })
            total_compra += costo_total_producto
            ahorro_total += ahorro_total_producto

        else:
            
            productos_seleccionados_alternativos = [fila for fila in precios_barrio if fila['categoria'].lower() == categoria_buscada]
            
            if productos_seleccionados_alternativos:
                producto_mas_barato_alternativo = min(productos_seleccionados_alternativos, key=lambda x: x['precio'])
                costo_total_producto = producto_mas_barato_alternativo['precio'] * cantidad
                
                explicacion = f"Se recomienda {producto_mas_barato_alternativo['producto']} marca {producto_mas_barato_alternativo['marca']}, ya que es la alternativa más barata al producto original que ingresaste({producto_buscado})"
                               
                
                resultados.append({
                    'producto': producto_mas_barato_alternativo['producto'],
                    'marca': producto_mas_barato_alternativo['marca'],
                    'colmado': producto_mas_barato_alternativo['colmado'],
                    'precio': producto_mas_barato_alternativo['precio'],
                    'costo_total': costo_total_producto,
                    'sugerencia': explicacion
                })
                total_compra += costo_total_producto
                print(f"{producto_buscado} no disponible. {explicacion}")

   
    print("-" * 50)
    for resultado in resultados:
        print(f"{resultado['producto']} | {resultado['colmado']} | RD${resultado['costo_total']}")
    
    print("-" * 50)
    print(f"Gasto Total: RD$ {total_compra}")
    print(f"Ahorro Estimado: RD$ {ahorro_total}")

    nombre_archivo = f"recomendacion_{barrio_seleccionado.replace(' ', '_')}.csv"
    escribir_archivo_salida(nombre_archivo,resultados)

print("******** Sistema AhorraRD ********")


barrio = input("Escribe el nombre del barrio: ")
recomendar_ahorro(barrio)