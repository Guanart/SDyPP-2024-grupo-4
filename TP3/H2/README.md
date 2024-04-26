# Comparación velocidades de descarga

### Consigna: 
Conéctese por ssh y haga un wget de un archivo grande (por ejemplo ISO de ubuntu: https://releases.ubuntu.com/jammy/ubuntu-22.04.2-desktop-amd64.iso) desde su pc y uno desde la instancia virtual.  Compare y comente las velocidades de descarga. ¿A qué se debe esta diferencia?

### Respuesta:
La descarga de la imagen desde una computadora personal tardó aproximadamente 30 minutos, mientras que la descarga de la imagen desde la instancia virtual tardó aproximadamente 2 minutos.
Esto se debe a que los proveedores de servicios en la nube, como Google Cloud Compute, tienen conexiones de red de alta velocidad. Pueden transferir los datos a velocidades mucho más altas que las conexiones de red domésticas típicas.
