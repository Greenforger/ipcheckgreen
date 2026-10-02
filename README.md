# IPCheckGreen

Herramienta para analizar la reputación de una IP usando múltiples fuentes sin API key.

## Instalación

```bash
git clone https://github.com/Greenforger/ipcheckgreen.git
cd ipcheckgreen
pip install requests
```

## Uso

```bash
python3 ipcheck.py <IP>
```

## Ejemplo

```bash
python3 ipcheck.py 8.8.8.8
```

## Qué muestra

- Ubicación geográfica (país, ciudad, ISP, ASN)
- Detección de proxy, hosting, Tor, móvil
- Reputación desde 3 fuentes independientes
- Score de abuso y reportes
- Veredicto final con colores

## Fuentes

- ip-api.com
- reputation.noc.org
- ipaudit.dev
- reportedip.de

## Créditos

Desarrollado por [Green Forger](https://greenforger.com)
