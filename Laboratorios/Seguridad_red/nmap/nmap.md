# Laboratorio: NMap

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar lsi si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.
- Cuenta Google Cloud (ver laboratorio [Servidor remoto Google Cloud](../../Servidor_remoto_Google_Cloud/Servidor_remoto_Google_Cloud.md)).

## NMap

[Nmap](https://nmap.org/) es un programa de código abierto que sirve para rastrear puertos y máquinas en una red (probablemente sea la herramienta de hacking que aparece en más películas: [https://nmap.org/movies/](https://nmap.org/movies/)). Con Nmap se pueden descubrir fácilmente muchas características de las máquinas que están visibles en la red: qué máquinas están encendidas, qué puertos tiene abiertos una máquina concreta, qué servicios está ejecutando y qué versiones de los mismos, qué sistema operativo y qué versión usa, etc.

Instala NMap:

```bash
sudo apt install nmap
```

Describe los comandos necesarios para descubrir lo siguiente:

> ¿Qué puertos están abiertos en `scanme.nmap.org` y en tu servidor de Google Cloud, qué servicios y qué versión de esos servicios?  
```bash
    nmap scanme.nmap.org -F -sV
    ...
    Not shown: 97 closed tcp ports (conn-refused)
    PORT   STATE    SERVICE VERSION
    22/tcp open     ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
    25/tcp filtered smtp
    80/tcp open     http    Apache httpd 2.4.7 ((Ubuntu))
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel



    nmap 34.175.117.80 -F -sV
    ...
    Not shown: 95 filtered tcp ports (no-response)
    PORT     STATE  SERVICE       VERSION
    22/tcp   open   ssh           OpenSSH 10.2p1 Ubuntu 2ubuntu3.8 (Ubuntu Linux; protocol 2.0)
    80/tcp   open   http          Apache httpd 2.4.66   
    443/tcp  open   ssl/http      Apache httpd 2.4.66 ((Ubuntu))
    3389/tcp closed ms-wbt-server
    5000/tcp closed upnp
    Service Info: Host: 34.175.117.80; OS: Linux; CPE: cpe:/o:linux:linux_kernel

```

> ¿Qué máquinas están activas en la red desde tu máquina hasta tu servidor remoto? (Pista: `traceroute`).
```bash
    sudo nmap 34.175.117.80 --traceroute
    ...
    TRACEROUTE (using port 3389/tcp)
    HOP RTT      ADDRESS
    1   3.82 ms  home (192.168.1.1)
    2   4.07 ms  10.0.20.159
    3   4.38 ms  172.16.32.193
    4   4.66 ms  10.221.231.61
    5   ... 6
    7   8.43 ms  86-120-71-209.rdsnet.ro (86.120.71.209)
    8   10.99 ms 80.117.175.34.bc.googleusercontent.com (34.175.117.80)
```

> ¿Qué puertos tiene abiertos una de las máquinas activas de la red?
> ¿Qué versiones de los servicios está usando una de las máquinas activas de la red?
> ¿Qué sistema operativo tiene una de las máquinas activas de la red?
```bash
    sudo nmap -F -sV -O 185.28.84.88
```
> ¿Qué sistema operativo tiene tu servidor en Google Cloud (según NMap)?
```bash
    sudo nmap 34.175.117.80 -O
    ...
    OS CPE: cpe:/o:linux:linux_kernel:2.6.11 cpe:/o:vmware:esx:3.0:2
    OS details: Linux 2.6.11, Linux 2.6.18, Linux 2.6.20.6, Linux 2.6.23, Linux 2.6.39, VMware ESX Server 3.0.2
```

> ¿Qué sistema operativo tiene `scanme.nmap.org`?
```bash
    sudo nmap scanme.nmap.org -O
    ...
    OS CPE: cpe:/o:linux:linux_kernel:5
    OS details: Linux 5.0 - 5.14

```

> Una vez determinado el sistema operativo, ¿qué vulnerabilidades tiene? (Pista: [https://cve.mitre.org](https://cve.mitre.org/)).  
> *Podemos buscar en repositorios públicos las vulenarabilidades reportadas para distintos sistemas operativos*

> ¿Cómo se puede usar NMap para detectar si una máquina tiene un firewall?  
> *Cuando hay puertos marcados como `filtered` por **nmap**, esto quiere decir que un firewall o cualquier otro sistema de red está controlando los intentos de conexión a dichos puertos*