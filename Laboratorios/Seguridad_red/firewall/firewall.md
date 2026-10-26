# Laboratorio: Firewall

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar lsi si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.
- Cuenta Google Cloud.

## Firewall Google Cloud

En este laboratorio desplegaréis vuestro sistema web en el servidor remoto de Google Cloud para aprender a configurar el acceso al mismo a través del firewall que provee Google Cloud por defecto. Para desplegar el proyecto web en el servidor remoto hay que instalar Docker y Docker Compose. Clonad el proyecto web en el servidor de Google Cloud (una vez establecida la conexión SSH): 

```bash
git clone https://github.com/mikel-egana-aranguren/docker-lamp.git
```

Construid la imagen web:

```bash
docker build -t="web" .
```

Desplegad la aplicación mediante Docker Compose:

```bash
docker-compose up
```

Para poder acceder a nuestro proyecto, cargar los datos mediante phpMyAdmin y ver la página web, tenemos que abrir ciertos puertos.

> ¿En qué puertos escucha nuestro proyecto? (Pista: `netstat`).  
> *Con el comando ss -tlp | grep 'docker' podemos ver esta información. Concretamente esucha en 8890 y 8889*

Una vez hayamos comprobado los puertos en los que nuestro proyecto está escuchando, tenemos que abrirlos para poder acceder desde el exterior.

> ¿Cómo se pueden abrir esos puertos en Google Cloud? (Pistas: red de VPC, etiqueta `http-server`, `0.0.0.0/0`).  
>*Configurándolos como puertos habilitados en una regla del firewall.*

En un firewall también es posible impedir el tráfico entrante, no solo permitirlo.

> ¿Cómo cerrarías los puertos 80 y 443 al tráfico entrante?  
> *Se podría o bien borrar la regla del firewall que permite el tráfico por estos 2 puertos o bien crear una nueva de mayor prioridad que los denegase.*

Además del tráfico entrante, en un firewall se puede bloquear el tráfico saliente.

> ¿Cómo impedirías el tráfico saliente a la página [https://en.wikipedia.org](https://en.wikipedia.org/) desde tu servidor de Google Cloud? (Pistas: `wget`, `ping`).  
> *Sí se puede, con otra regla del firewall que bloquee el tráfico que llegue desde la IP que tiene el servidor de la página web. Podemos conocer la IP de la web en cuestión por medio de herrmaientas de red, por ejemplo haciendo un `ping` al dominio de Wikipedia nos devuelva la siguiente IP`185.15.58.224`.*

Por último, se puede bloquear el tráfico desde una dirección concreta.

> ¿Cómo impedirías el tráfico entrante en el puerto 8890 desde tu IP actual? (Pista: «What is my IP?»).  
> *Creando otra regla del firewall que bloquease el tráfico por dicho puerto solamente para la IP del host en cuestión. Para ello necesitaré conocer la IP pública que dicho host está empleando. Hay páginas web que te la indican

## IPTables

**IPTables** es un módulo perteneciente al kernel de Linux que permite actuar como firewall, ya que se encarga de filtrar los paquetes de datos que entran y salen de la máquina. IPTables funciona mediante reglas que tendremos que definir en función de lo que queramos hacer. Por defecto, las reglas definidas no son persistentes; esto es, al reiniciar el sistema se borran.

Para evitar tener que introducir una y otra vez las mismas reglas, se pueden guardar en un fichero mediante el siguiente comando:

```bash
sudo iptables-save > /home/user/fichero
```

Tras reiniciar la máquina, se pueden recuperar mediante:

```bash
sudo iptables-restore < /home/user/fichero
```

Si quisiéramos que la restauración de reglas se hiciera de manera automática cada vez que se reiniciara el sistema, podríamos crear un script que se ejecutara al iniciar la máquina o modificar la configuración de red para que, al configurar las conexiones, se restauraran automáticamente las reglas de IPTables.

Definid las reglas necesarias para conseguir lo siguiente:

> Que vuestro servidor de Google Cloud solo acepte conexiones SSH desde el servidor de Google Cloud de otro alumno y desde vuestra máquina local.

> Instalad un servicio FTP en vuestro servidor de Google Cloud y configuradlo para que solo acepte conexiones FTP desde máquinas de la red de `ehu.eus`.

> Que vuestro servidor de Google Cloud no acepte conexiones HTTP (solo HTTPS).

> Que en vuestra máquina local no se puedan hacer conexiones salientes a Twitter, Facebook ni YouTube.
