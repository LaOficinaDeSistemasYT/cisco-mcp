# Claude Code + MCP en routers Cisco (GNS3)

Servidor MCP de solo lectura que permite a Claude Code diagnosticar routers Cisco IOSv por SSH.
Código del video de La Oficina de Sistemas: [enlace al video]

## Qué hace

- `list_devices`: lista los routers del laboratorio y su IP de gestión.
- `run_show_command`: ejecuta un comando `show` en un router. Cualquier otro comando se rechaza.

## Requisitos

- GNS3 y GNS3 VM con la imagen Cisco IOSv
- VM Ubuntu 24.04 con 2 tarjetas de red: una con Internet y otra en la red de gestión de los routers
- uv, curl y git
- Claude Code con una cuenta de Claude Pro o superior

## Instalación

```bash
git clone https://github.com/LaOficinaDeSistemasYT/cisco-mcp.git
cd cisco-mcp
uv sync
cp .env.example .env
nano .env        # opcional: cambia las IP o la clave si tu lab es distinto
chmod 600 .env
claude mcp add --transport stdio cisco-lab -- uv --directory "$PWD" run server.py
claude --permission-mode manual
```

## Lab y falla de la demo

1. Carga `routers/R1.cfg` y `routers/R2.cfg` en los routers.
2. Comprueba que son vecinos: `show ip ospf neighbor` en R1.
3. Para repetir la demo del video, aplica en R2 los comandos de `routers/falla-ospf.txt`. Al final del archivo están los comandos para quitar la falla.

## Seguridad

- El servidor solo acepta comandos `show`.
- `.claude/settings.json` le quita a Claude Code la terminal y la escritura de archivos, para que solo use las herramientas MCP.
- El usuario de los routers tiene privilegio 1: aunque alguien consiga la clave, no puede configurar nada.

## Nota sobre Paramiko

IOSv usa algoritmos SSH con SHA1 que Paramiko 5 ya no acepta. Por eso el proyecto fija `paramiko<5`. En producción, actualiza el IOS en lugar de bajar la versión.

## Más

- Guía paso a paso en PDF, con solución de errores: [enlace]
- Canal: https://www.youtube.com/@LaOficinaDeSistemas
