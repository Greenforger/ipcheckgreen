import requests
import sys

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
C = '\033[96m'
W = '\033[97m'
DIM = '\033[2m'
BOLD = '\033[1m'
RESET = '\033[0m'

def si_no(val, peligroso=False):
    if val:
        return f"{R}Si{RESET}" if peligroso else f"{G}Si{RESET}"
    return f"{G}No{RESET}" if peligroso else f"{DIM}No{RESET}"

def geo(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,isp,org,as,proxy,hosting,mobile", timeout=5)
        d = r.json()
        if d.get("status") == "success":
            print(f"\n{BOLD}{B}UBICACION{RESET}")
            print(f"  {DIM}Pais:   {RESET} {W}{d.get('country', 'N/A')}{RESET}")
            print(f"  {DIM}Region: {RESET} {W}{d.get('regionName', 'N/A')}{RESET}")
            print(f"  {DIM}Ciudad: {RESET} {W}{d.get('city', 'N/A')}{RESET}")
            print(f"  {DIM}ISP:    {RESET} {C}{d.get('isp', 'N/A')}{RESET}")
            print(f"  {DIM}ORG:    {RESET} {C}{d.get('org', 'N/A')}{RESET}")
            print(f"  {DIM}ASN:    {RESET} {C}{d.get('as', 'N/A')}{RESET}")
            print(f"  {DIM}Proxy:  {RESET} {si_no(d.get('proxy'), True)}")
            print(f"  {DIM}Hosting:{RESET} {si_no(d.get('hosting'))}")
            print(f"  {DIM}Movil:  {RESET} {si_no(d.get('mobile'))}")
        else:
            print(f"  {R}No se pudo obtener ubicacion{RESET}")
    except Exception as e:
        print(f"  {R}Error: {e}{RESET}")

def reputation_noc(ip):
    try:
        r = requests.get(f"https://reputation.noc.org/api/?ip={ip}", timeout=5)
        d = r.json()
        rep = d.get("reputation", {})
        uso = d.get("usage", {})
        rec = d.get("recommendations", {})
        print(f"\n{BOLD}{Y}REPUTACION (noc.org){RESET}")
        print(f"  {DIM}Reverse:    {RESET} {W}{d.get('reverse', 'N/A')}{RESET}")
        print(f"  {DIM}Tor:        {RESET} {si_no(uso.get('is_tor'), True)}")
        print(f"  {DIM}Proxy:      {RESET} {si_no(uso.get('is_proxy'), True)}")
        print(f"  {DIM}Hosting:    {RESET} {si_no(uso.get('is_hosting'))}")
        print(f"  {DIM}Web Spam:   {RESET} {si_no(rep.get('web_spam'), True)}")
        print(f"  {DIM}Ataques Web:{RESET} {si_no(rep.get('web_attacks'), True)}")
        print(f"  {DIM}Botnet:     {RESET} {si_no(rep.get('botnet'), True)}")
        print(f"  {DIM}Email Spam: {RESET} {si_no(rep.get('email_spam'), True)}")
        print(f"  {DIM}Brute Force:{RESET} {si_no(rep.get('brute_force'), True)}")
        print(f"  {DIM}DDoS:       {RESET} {si_no(rep.get('ddos'), True)}")
        print(f"  {DIM}Bloquear:   {RESET} {si_no(rec.get('block_traffic'), True)}")
        return any(rep.values())
    except Exception:
        print(f"  {R}No disponible{RESET}")
        return None

def reputation_ipaudit(ip):
    try:
        r = requests.get(f"https://ipaudit.dev/api/analyze?ip={ip}", timeout=5)
        d = r.json()
        ts = d.get("trust_score", {})
        score = ts.get("score", "N/A") if isinstance(ts, dict) else ts
        grade = ts.get("grade", "") if isinstance(ts, dict) else ""
        signals = ts.get("signals", d.get("signals", [])) if isinstance(ts, dict) else d.get("signals", [])
        color = G if isinstance(score, int) and score >= 70 else Y if isinstance(score, int) and score >= 40 else R
        print(f"\n{BOLD}{Y}REPUTACION (ipaudit.dev){RESET}")
        print(f"  {DIM}Trust Score:{RESET} {color}{score}/100 ({grade}){RESET}")
        if signals:
            for s in signals[:6]:
                v = s.get('verdict', '')
                vc = G if v == 'consistent' else Y if v == 'disputed' else R
                print(f"  {DIM}{s.get('key',''):15}{RESET} {vc}{v}{RESET}")
    except Exception:
        print(f"\n{BOLD}{Y}REPUTACION (ipaudit.dev){RESET}")
        print(f"  {R}No disponible{RESET}")

def reported(ip):
    try:
        r = requests.get(f"https://reportedip.de/wp-json/reportedip/v2/check-public?ip={ip}", timeout=5)
        d = r.json().get("data", {})
        score = d.get("abuseConfidencePercentage", 0)
        reports = d.get("totalReports", 0)
        last = d.get("lastReportedAt", "Nunca")
        color = R if score >= 50 else Y if score >= 20 else G
        print(f"\n{BOLD}{Y}REPUTACION (reportedip.de){RESET}")
        print(f"  {DIM}Score abuso:{RESET} {color}{score}/100{RESET}")
        print(f"  {DIM}Reportes:   {RESET} {W}{reports}{RESET}")
        print(f"  {DIM}Ultimo:     {RESET} {DIM}{last}{RESET}")
    except Exception:
        print(f"\n{BOLD}{Y}REPUTACION (reportedip.de){RESET}")
        print(f"  {R}No disponible{RESET}")

def veredicto(ip, peligrosa):
    print(f"\n{BOLD}VEREDICTO FINAL{RESET}")
    if peligrosa:
        print(f"  {R}{BOLD}PELIGROSA{RESET} — IP {ip} tiene actividad maliciosa detectada")
    elif peligrosa is False:
        print(f"  {G}{BOLD}LIMPIA{RESET} — IP {ip} sin amenazas detectadas")
    else:
        print(f"  {Y}{BOLD}INDETERMINADO{RESET} — No se pudo verificar la reputacion")

def check_ip(ip):
    print(f"\n{BOLD}{G}Analizando: {W}{ip}{RESET}")
    print(f"{DIM}{'=' * 50}{RESET}")
    geo(ip)
    peligrosa = reputation_noc(ip)
    reputation_ipaudit(ip)
    reported(ip)
    veredicto(ip, peligrosa)
    print(f"{DIM}{'=' * 50}{RESET}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{R}Uso: python3 ipcheck.py <IP>{RESET}")
        sys.exit(1)
    check_ip(sys.argv[1])
