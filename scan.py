import socket
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor

def scan_ports(ip, ports):
    """Berilgan IP uchun ochiq portlarni skanerlaydi."""
    open_ports = []
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)  # Har bir port uchun kutish vaqti (soniyalar)
                if s.connect_ex((ip, port)) == 0:  # Port ochiq bo'lsa
                    open_ports.append(port)
        except Exception:
            pass
    return open_ports

def scan_network(network, ports):
    """Berilgan tarmoq diapazoni bo'yicha skanerlaydi."""
    print(f"Tarmoqni skanerlayapman: {network}")
    network_ips = list(ip_network(network, strict=False).hosts())
    results = {}

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_ip = {executor.submit(scan_ports, str(ip), ports): ip for ip in network_ips}
        for future in future_to_ip:
            ip = future_to_ip[future]
            try:
                open_ports = future.result()
                if open_ports:
                    results[str(ip)] = open_ports
            except Exception as e:
                print(f"Xato: {e}")

    return results

if __name__ == "__main__":
    # Foydalanuvchi parametrlarini kiritadi
    tarmoq = input("Tarmoq diapazonini kiriting (masalan: 192.168.1.0/24): ")
    portlar = range(1, 1025)  # Skannerlanadigan portlar diapazoni (1-1024)

    natijalar = scan_network(tarmoq, portlar)
    
    print("\nSkanerlash yakunlandi. Natijalar:")
    for ip, ports in natijalar.items():
        print(f"{ip} -> Ochiq portlar: {ports}")
