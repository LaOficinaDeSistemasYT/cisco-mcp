"""Servidor MCP de solo lectura para los routers Cisco del laboratorio (La Oficina de Sistemas)."""

import asyncio
import os
import re
from pathlib import Path

from dotenv import load_dotenv
from mcp.server import MCPServer
from netmiko import ConnectHandler

load_dotenv(Path(__file__).with_name(".env"))

mcp = MCPServer("cisco-lab")

DEVICES = {
    "R1": os.environ.get("R1_HOST", ""),
    "R2": os.environ.get("R2_HOST", ""),
}
USER = os.environ.get("LAB_USER", "")
PASSWORD = os.environ.get("LAB_PASSWORD", "")

# Solo comandos show (también sus abreviaturas: sh, sho), en una sola línea.
SHOW_ONLY = re.compile(r"^sh(o|ow)?\s+\S", re.IGNORECASE)


def _run(host: str, command: str) -> str:
    conn = ConnectHandler(
        device_type="cisco_ios",
        host=host,
        username=USER,
        password=PASSWORD,
        timeout=20,
    )
    try:
        return conn.send_command(command)
    finally:
        conn.disconnect()


@mcp.tool()
async def list_devices() -> str:
    """Lista los routers del laboratorio y su IP de gestión."""
    return "\n".join(f"{name}: {host}" for name, host in DEVICES.items())


@mcp.tool()
async def run_show_command(device: str, command: str) -> str:
    """Ejecuta un comando show de solo lectura en un router Cisco del laboratorio.

    Args:
        device: Nombre del router, por ejemplo R1 o R2
        command: Comando show, por ejemplo 'show ip ospf neighbor'
    """
    name = device.strip().upper()
    cmd = command.strip()
    if name not in DEVICES:
        return f"Error: el equipo '{device}' no existe. Opciones: {', '.join(DEVICES)}"
    if "\n" in cmd or "\r" in cmd or not SHOW_ONLY.match(cmd):
        return "Rechazado: este servidor solo permite comandos 'show' de solo lectura."
    output = await asyncio.to_thread(_run, DEVICES[name], cmd)
    return f"{name}# {cmd}\n{output}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
