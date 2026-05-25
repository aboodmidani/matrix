import re
import logging
from typing import List, Dict, Any
from tools import check_tool, run_command

logger = logging.getLogger(__name__)

PORTS = [
    21, 22, 23, 25, 53, 80, 110, 143, 443,
    445, 465, 587, 993, 995, 1433, 1521,
    2049, 2375, 2376, 3306, 3389, 5432, 5900,
    6379, 6443, 8000, 8080, 8443, 8888,
    9200, 9443, 11211, 27017, 27018, 50000,
]


def run_nmap_scan(domain: str) -> List[Dict[str, Any]]:
    if check_tool('nmap'):
        return _nmap_scan(domain)
    return _powershell_port_scan(domain)


def _nmap_scan(domain: str) -> List[Dict[str, Any]]:
    port_list = ','.join(str(p) for p in PORTS)
    success, stdout, stderr = run_command(
        [
            'nmap', '-sT', '-sV',
            '--version-intensity', '5',
            '-T4',
            '-p', port_list,
            '--open',
            domain,
        ],
        timeout=120
    )
    if success and stdout:
        result = _parse_nmap_output(stdout)
        if result:
            return result
    return []


def _parse_nmap_output(output: str) -> List[Dict[str, Any]]:
    ports = []
    current = None
    for line in output.splitlines():
        match = re.match(r'(\d+)/(tcp|udp)\s+open\s+(\S+)\s*(.*)', line)
        if match:
            current = {
                'port':     int(match.group(1)),
                'protocol': match.group(2),
                'service':  match.group(3),
                'version':  match.group(4).strip(),
                'state':    'open',
                'info':     [],
            }
            ports.append(current)
            continue
        if current and re.match(r'\|', line):
            info_line = re.sub(r'^\|[_\s]*', '', line).strip()
            if info_line:
                current['info'].append(info_line)
    for p in ports:
        info = p.pop('info', [])
        if info and not p['version']:
            p['version'] = info[0]
        elif info:
            first = info[0]
            if first and first not in p['version']:
                p['version'] = f"{p['version']} | {first}".strip(' |')
    return ports


def _powershell_port_scan(domain: str) -> List[Dict[str, Any]]:
    port_list = ','.join(str(p) for p in PORTS)
    ps_script = (
        f'@({",".join(str(p) for p in PORTS)}) | ForEach-Object {{ '
        f'try {{ '
        f'$c = New-Object Net.Sockets.TcpClient; '
        f'$async = $c.ConnectAsync("{domain}", $_); '
        f'if ($async.Wait(1500)) {{ Write-Output $_ }} '
        f'}} catch {{ }} '
        f'finally {{ try {{ $c.Dispose() }} catch {{ }} }} '
        f'}}'
    )
    success, stdout, stderr = run_command(
        ['powershell', '-NoProfile', '-Command', ps_script],
        timeout=120
    )
    ports = []
    if success and stdout.strip():
        for line in stdout.splitlines():
            line = line.strip()
            if line.isdigit():
                ports.append({
                    'port': int(line),
                    'protocol': 'tcp',
                    'state': 'open',
                    'service': '',
                    'version': '',
                })
    if not ports:
        logger.info("PowerShell port scan returned no open ports for %s", domain)
    return ports
