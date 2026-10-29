# Laboratorio: pen-testing 

## Requisitos previos

- Máquina GNU/Linux: portátil, máquina virtual, o PC laboratorio (Entrar con credencial LDAP, solo usar usuario `lsi` si es necesario, mediante el comando `su - lsi`).
- Editor de código. En Visual Studio Code, pulsando ctrl+mayus+v renderiza este archivo de manera amigable (Sobre todo para imágenes).
- Repositorio GitHub de asignatura: puedes subir los programas desarrollados en el laboratorio.

## Pen-testing con ZAP y Multillidae

El pen-testing consiste en buscar vulnerabilidades en sistemas Web. Para hacerlo vamos a usar un proyecto web vulnerable (Mutillidae) y un scaner de vulnerabilidades (ZAP).

## Desplegar Mutillidae 

Clona el repositorio de Mutillidae:

```bash
git clone https://github.com/webpwnized/mutillidae-dockerhub
```

Levanta el proyecto dentro de la carpeta `mutillidae-dockerhub`:

```bash
docker compose up
```
Ir a http://localhost:80. Si aparece un error del estilo "Database not set", pulsar en "Set up database".

## Instalar ZAP

Ir a https://www.zaproxy.org/download/, bajar el archivo `Linux package` y descomprimir. En el directorio apropiado, ejecutar ZAP:

```bash
./zap.sh
```

Elegir "Escaneo automático", http://localhost:80, y "atacar". Cuando termine el escaneo automático:

> ¿Qué vulnerabilidades has encontrado? ¿A qué CVEs o CWEs se mapean?  
> *CVE - **Common Weakness Enumeration** y CWE - **Common Vulnerabilities and Exposures***
> - *PII Disclosure: Filtración de información personal (CWE-539)*
> - *Absence of Anti-CSRF Tokens: Ausencia de tokens anti falsificación de petición en sitios cruzados (Cross-site Request Forgery) (CWE-352)*
> - *Application Error Disclosure: Filtrado de errores de aplciación (CWE-550)*
> - *Content Security Policy (CSP) Header Not Set: Política de seguridad de contenido, cabecera asuente (CWE-693)*
> - *Cross-Domain Misconfiguration: Falta de configuración entre dominios (CWE-264)*
> - *Otros...*

> Intenta realizar el escaneo en la IP Google Cloud proporcionada por el profesor, ¿Has encontrado las mismas vulnerabilidades?  
> *No se hace*

