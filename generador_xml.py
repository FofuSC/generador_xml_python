from xml.dom.minidom import parse
import xml.dom.minidom
import base64
from M2Crypto import RSA
from time import strftime
from lxml import etree as ET
import hashlib
from datetime import datetime
import subprocess
import commands

ruta_cer = '/home/fofu/Documentos/Informacion_FINKOK/practicas_amexiproc/informacion_cliente/IIA040805DZ4.cer'
certificado = subprocess.check_output('openssl x509 -inform DER -in ' + str(ruta_cer), shell=True).replace("\n", "")
serial = subprocess.check_output('openssl x509 -inform DER -in ' + str(ruta_cer) + ' -noout -serial', shell=True)
get_serial = ""
get_certificado = ""

indice = 7
while indice < len(serial):
	if indice % 2 == 0:
		get_serial += serial[indice]
	indice += 1

indice = 27
while indice < len(certificado) - 25:
	get_certificado += certificado[indice]
	indice += 1

sello = ""

tiempo = datetime.now()
fecha = tiempo.strftime("%Y-%m-%d")+"T"+tiempo.strftime("%H:%M:%S")
sello = " "
noCertificado = " "
certificado = " "

totalDeTotales = 0.00
subTotal = 0.00

ret = 0
retenc = []
clavesProdServ = []
clavesUnidad = []
noIdentificacion = []
cantidadProdServ = []
unidadesProdServ = []
descProdServ = []
valorUnitario = []
descuentosProdServ = []
tasasCuotasRetenciones = []
impuestosRetenciones = [],[]

importesProdServ = []
importesPartes = []
bases = []
cfdiRelacionados = []
importesRetenciones = []
totalImpuestosRetenidos = 0.00
totalImpuestosTrasladados = 0.00
impuestosTraslados = []
tasasCuotas = []
numerosPedimento = []
cuentasPrediales = []
importados = 0

partes_claves = []
partes_cantidades = []
partes_descripciones = []
partes_no_identificaciones = []
partes_unidades = []
partes_valores_unitarios = []
tiposFactores = []
importesTraslados = [],[]
cantidad_partes = 0
cant_retenciones = 0
cant_traslados = 0

print "--------------------DATOS DEL EMISOR--------------------"
rfc_emisor = raw_input("RFC: ")
nombre_emisor = raw_input("Nombre: ")
regimen_fiscal = raw_input("Regimen Fiscal: ")

print "-------------------DATOS DEL RECEPTOR-------------------"
rfc_receptor = raw_input("RFC: ")
nombre_receptor = raw_input("Nombre: ")
usoCFDI = raw_input("Uso de CFDI: ")

print "-------------------DATOS COMPROBANTE--------------------"
formaPago = raw_input("Forma de pago: ")
condicionesDePago = raw_input("Condicion de Pago: ")
tipoMoneda = raw_input("Moneda: ")
metodoPago = raw_input("Metodo de pago: ")
tipoComprobante = raw_input("Tipo de comprobante (I/E): ")
codigoPostal = raw_input("Codigo postal de expedicion: ")

print "--------------------CFDI RELACIONADOS--------------------"
cfdi_relacionados = input("Cantidad de CFDI relacionados: ")
i = 0
while i < cfdi_relacionados:
	cfdi = raw_input("UUID: ")
	cfdiRelacionados.append(cfdi)
	i+=1

cantConceptos = input("Cantidad de conceptos: ")

print "---------------------DATOS CONCEPTOS---------------------"
iterador = 0
while iterador < cantConceptos:
	clave_prod_serv = raw_input("Clave del producto o servicio: ")
	clave_unidad = raw_input("Clave por unidad: ")
	no_identificacion = raw_input("Numero de identificacion: ")
	cantidad_prod_serv = float(input("Cantidad: "))
	unidad_prod_serv = raw_input("Unidad: ")
	desc_prod_serv = raw_input("Descripcion: ")
	valor_unit = float(input("Valor por unidad: "))
	descuento_prod_serv = float(input("Descuento: "))

	clavesProdServ.append(clave_prod_serv)
	clavesUnidad.append(clave_unidad)
	noIdentificacion.append(no_identificacion)
	cantidadProdServ.append(cantidad_prod_serv)
	unidadesProdServ.append(unidad_prod_serv)
	descProdServ.append(desc_prod_serv)
	valorUnitario.append(valor_unit)
	descuentosProdServ.append(descuento_prod_serv)
	tipoFactor = raw_input("Tipo de factor: ")
	tiposFactores.append(tipoFactor)

	importe = valor_unit * cantidad_prod_serv
	importesProdServ.append(importe)
	subTotal += importe

	base = importesProdServ[iterador] - descuentosProdServ[iterador]
	bases.append(base)

	importado = raw_input("Concepto importado? (y/n): ")
	if importado == "y" or importado == "Y" or importado == "s" or importado == "S":
		print "----------------------INFORMACION ADUANERA----------------------"
		numeroPedimento = raw_input("Numero pedimento: ")
		cuentaPredial = raw_input("Numero cuenta predial: ")
		numerosPedimento.append(numeroPedimento)
		cuentasPrediales.append(cuentaPredial)
		importados += 1


	partes = raw_input("Equipado por partes? (y/n): ")
	if partes == "y" or partes == "Y" or partes == "s" or partes == "S":
		iterador2 = 0
		cantidad_partes = input("Cantidad de partes: ")
		while iterador2 < cantidad_partes:
			print "--------------------DATOS POR PARTES--------------------"
			parte_clave = raw_input("Clave del producto o servicio: ")
			parte_cantidad = float(input("Cantidad: "))
			parte_descripcion = raw_input("Descripcion: ")
			parte_no_identificacion = raw_input("Numero de identificacion: ")
			parte_unidad = raw_input("Unidad: ")
			parte_valor_unitario = float(input("Valor por unidad: "))

			partes_claves.append(parte_clave)
			partes_cantidades.append(parte_cantidad)
			partes_descripciones.append(parte_descripcion)
			partes_no_identificaciones.append(parte_no_identificacion)
			partes_unidades.append(parte_unidad)
			partes_valores_unitarios.append(parte_valor_unitario)

			importe_parte = parte_valor_unitario * parte_cantidad
			importesPartes.append(importe_parte)
			iterador2+=1
	if tipoFactor != "Exento" or tipoFactor != "exento":
		traslado_pregunta = raw_input("Traslado? (y/n)")
		if traslado_pregunta == "S" or traslado_pregunta == "s" or traslado_pregunta == "y" or traslado_pregunta == "Y":
			importesTraslados[0].append(iterador)
			cant_traslados = input("Cantidad de traslados: ")
			i_tras = 0
			while i_tras < cant_traslados:
				print "-----------------------TRASLADOS-----------------------"
				impuestoTraslado = raw_input("Impuesto: ")
				tasaOcuotaTraslado = float(input("Tasa o cuota: "))
				importeTraslado = bases[iterador] * tasaOcuotaTraslado
				importesTraslados[1].append(importeTraslado)
				totalImpuestosTrasladados += importeTraslado
				impuestosTraslados.append(impuestoTraslado)
				tasasCuotas.append(tasaOcuotaTraslado)
				i_tras += 1

	retencion_pregunta = raw_input("Retencion? (y/n)")
	if retencion_pregunta == "S" or retencion_pregunta == "s" or retencion_pregunta == "y" or retencion_pregunta == "Y":
		cant_retenciones = input("Cantidad de reteciones: ")
		i_ret = 0
		retenc.append(cant_retenciones)
		while i_ret < cant_retenciones:
			print "----------------------RETENCIONES----------------------"
			impuestoRetencion = raw_input("Impuesto: ")
			tasaOcuotaRetencion = float(input("Tasa o cuota: "))
			importeRetencion = bases[iterador] * tasaOcuotaRetencion
			tasasCuotasRetenciones.append(tasaOcuotaRetencion)
			impuestosRetenciones[0].append(impuestoRetencion)
			impuestosRetenciones[1].append(importeRetencion)
			#importesRetenciones.append(importeRetencion)
			totalImpuestosRetenidos += importeRetencion
			i_ret += 1
	iterador+=1

totalDescuentos = 0.00
for d in descuentosProdServ:
	totalDescuentos += d

totalDeTotales = subTotal - totalImpuestosRetenidos + totalImpuestosTrasladados - totalDescuentos

xml = open('cfdi_generado.xml', "w")

xml.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
xml.write('<cfdi:Comprobante Version="3.3" Fecha="'+ str(fecha) +'" Sello="" FormaPago="' + str(formaPago) + '" NoCertificado="' + str(get_serial) + '" Certificado="' + str(get_certificado) + '" CondicionesDePago="' + str(condicionesDePago) + '" SubTotal="' + str("{0:.2f}".format(subTotal)) + '" Descuento="' + str("{0:.2f}".format(totalDescuentos)) + '" Moneda="' + str(tipoMoneda) + '" Total="' + str("{0:.2f}".format(totalDeTotales)) + '" TipoDeComprobante="' + str(tipoComprobante) + '" MetodoPago="' + str(metodoPago) + '" LugarExpedicion="' + str(codigoPostal) + '" xmlns:cfdi="http://www.sat.gob.mx/cfd/3" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n')
xml.write('\t<cfdi:CfdiRelacionados TipoRelacion="0' + str(cfdi_relacionados) + '">\n')
for cfdi in cfdiRelacionados:
	xml.write('\t\t<cfdi:CfdiRelacionado UUID="' + str(cfdi) + '"/>\n')
xml.write('\t</cfdi:CfdiRelacionados>\n')
xml.write('\t<cfdi:Emisor Rfc="' + str(rfc_emisor) + '" Nombre="' + str(nombre_emisor) + '" RegimenFiscal="' + str(regimen_fiscal) + '"/>\n')
xml.write('\t<cfdi:Receptor Rfc="' + str(rfc_receptor) + '" Nombre="' + str(nombre_receptor) + '" UsoCFDI="' + str(usoCFDI) + '"/>\n')
xml.write('\t<cfdi:Conceptos>\n')
c = 0
while c < cantConceptos:
	xml.write('\t\t<cfdi:Concepto ClaveProdServ="' + str(clavesProdServ[c]) + '" NoIdentificacion="' + str(noIdentificacion[c]) + '" Cantidad="' + str("{0:.2f}".format(cantidadProdServ[c])) + '" ClaveUnidad="' + str(clavesUnidad[c]) + '" Unidad="' + str(unidadesProdServ[c]) + '" Descripcion="' + str(descProdServ[c]) + '" ValorUnitario="' + str("{0:.2f}".format(valorUnitario[c])) + '" Importe="' + str("{0:.2f}".format(importesProdServ[c])) + '" Descuento="' + str("{0:.2f}".format(descuentosProdServ[c])) + '">\n')
	xml.write('\t\t\t<cfdi:Impuestos>\n')
	t = 0
	if c in importesTraslados[0]:
		xml.write('\t\t\t\t<cfdi:Traslados>\n')
		tras = 0
		while tras < cant_traslados:
			xml.write('\t\t\t\t\t<cfdi:Traslado Base="' + str("{0:.2f}".format(bases[c])) + '" Impuesto="' + str(impuestosTraslados[t]) + '" TipoFactor="' + str(tiposFactores[t]) + '" TasaOCuota="' + str("{0:.6f}".format(tasasCuotas[t])) + '" Importe="' + str("{0:.2f}".format(importesTraslados[1][t])) + '"/>\n')
			tras += 1
			t+=1
		xml.write('\t\t\t\t</cfdi:Traslados>\n')
	if len(retenc) > 0:
		#ret = 0
		xml.write('\t\t\t\t<cfdi:Retenciones>\n')
		while ret < retenc[c]:
			xml.write('\t\t\t\t\t<cfdi:Retencion Base="' + str("{0:.2f}".format(bases[c])) + '" Impuesto="' + str(impuestosRetenciones[0][ret]) + '" TipoFactor="' + str(tiposFactores[c]) + '" TasaOCuota="' + str("{0:.6f}".format(tasasCuotasRetenciones[ret])) + '" Importe="' + str("{0:.2f}".format(impuestosRetenciones[1][ret])) + '"/>\n')
			ret += 1
	xml.write('\t\t\t\t</cfdi:Retenciones>\n')
	xml.write('\t\t\t</cfdi:Impuestos>\n')
	i = 0
	while i < importados:
		xml.write('\t\t\t<cfdi:InformacionAduanera NumeroPedimento="' + str(numerosPedimento[i]) + '"/>\n')
		xml.write('\t\t\t<cfdi:CuentaPredial Numero="' + str(cuentasPrediales[i]) + '"/>\n')
		i+=1
		importados -= 1
	p = 0
	while p < cantidad_partes:
		xml.write('\t\t\t<cfdi:Parte ClaveProdServ="' + str(partes_claves[p]) + '" NoIdentificacion="' + str(partes_no_identificaciones[p]) + '" Cantidad="' + str("{0:.2f}".format(partes_cantidades[p])) + '" Unidad="' + str(partes_unidades[p]) + '" Descripcion="' + str(partes_descripciones[p]) + '" ValorUnitario="' + str("{0:.2f}".format(partes_valores_unitarios[p])) + '" Importe="' + str("{0:.2f}".format(importesPartes[p])) + '">\n')
		xml.write('\t\t\t\t<cfdi:InformacionAduanera NumeroPedimento="' + str(numerosPedimento[p]) + '"/>\n')
		xml.write('\t\t\t</cfdi:Parte>\n')
		p+=1
	xml.write('\t\t</cfdi:Concepto>\n')
	c+=1
xml.write('\t</cfdi:Conceptos>\n')
xml.write('\t<cfdi:Impuestos TotalImpuestosRetenidos="' + str("{0:.2f}".format(totalImpuestosRetenidos)) + '" TotalImpuestosTrasladados="' + str("{0:.2f}".format(totalImpuestosTrasladados)) + '">\n')
xml.write('\t\t<cfdi:Retenciones>\n')
repetidos = []
unicos = []
total = 0.00
if impuestosRetenciones > 0:
	i = 0
	j = 0
	while i < len(impuestosRetenciones):
		if len(impuestosRetenciones[0]) - 1 > 0:
			if impuestosRetenciones[0][0] == impuestosRetenciones[0][1]:
				repetidos.append(impuestosRetenciones[0][0])
				impuestosRetenciones[0].pop(1)
				impuestosRetenciones[1].pop(1)
		i+=1
	total += totalImpuestosRetenidos
	impuestosRetenciones[0].pop(0)
	impuestosRetenciones[1].pop(0)
	if len(repetidos) > 0:
		xml.write('\t\t\t<cfdi:Retencion Impuesto="' + str(repetidos[0]) + '" Importe="' + str("{0:.2f}".format(total)) + '"/>\n')
if len(impuestosRetenciones[0]) > 0:
	i = 0
	while i < len(impuestosRetenciones) - 1:
		total = 0.00
		total += impuestosRetenciones[1][i]
		xml.write('\t\t\t<cfdi:Retencion Impuesto="' + str(impuestosRetenciones[0][i]) + '" Importe="' + str("{0:.2f}".format(total)) + '"/>\n')
		i+=1
xml.write('\t\t</cfdi:Retenciones>\n')
xml.write('\t\t<cfdi:Traslados>\n')
i = 0
while i < len(impuestosTraslados):
	xml.write('\t\t\t<cfdi:Traslado Impuesto="' + str(impuestosTraslados[i]) + '" TipoFactor="' + str(tiposFactores[i]) + '" TasaOCuota="' + str("{0:.6f}".format(tasasCuotas[i])) + '" Importe="' + str("{0:.2f}".format(importesTraslados[1][i])) + '"/>\n')
	i+=1
xml.write('\t\t</cfdi:Traslados>\n')
xml.write('\t</cfdi:Impuestos>\n')
xml.write('</cfdi:Comprobante>\n')

xml.close()

def generar_sello( nombre_archivo, llave_pem ):
	file = open(nombre_archivo, 'r')
	comprobante = file.read()
	file.close()
	xdoc = ET.fromstring(comprobante)
	xsl_root = ET.parse('cadenaoriginal_3_3.xslt')
	xsl = ET.XSLT(xsl_root)
	cadena_original = xsl(xdoc)

	keys = RSA.load_key(llave_pem)
	digest = hashlib.new('sha256', str(cadena_original).encode()).digest()
	sello = base64.b64encode(keys.sign(digest, "sha256"))

	f1 = open("cfdi_generado.xml", "r")
	f2 = open("cfdi_modificado.xml", "w")
	for line in f1:
		f2.write(line.replace('Sello=""', 'Sello="' + str(sello) + '"'))
	f1.close()
	f2.close()
	
ruta_xml = "cfdi_generado.xml"
llave_pem = "../informacion_cliente/IIA040805DZ4.key.pem"


generar_sello(ruta_xml, llave_pem)