# IPCheckGreen

Herramienta para analizar la reputación de una IP usando múltiples fuentes sin API key.

## Características

- Ubicación geográfica (país, ciudad, ISP, ASN)
- Detección de proxy, hosting, Tor
- Reputación desde noc.org, ipaudit.dev y reportedip.de
- Veredicto final con colores

## Uso

```bash
python3 ipcheck.py <IP>
```

## Ejemplo

```bash
python3 ipcheck.py 8.8.8.8
```

## Fuentes

- ip-api.com
- reputation.noc.org
- ipaudit.dev
- reportedip.de

## Créditos

Desarrollado por [Green Forger](https://greenforger.com)
