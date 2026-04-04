# Script di Deployment e Monitoraggio

Questa directory contiene tutti gli script operativi per l'implementazione e il monitoraggio del sistema NSR (Non-Servitude Rule).

## 📋 Indice

1. [Script di Attivazione](#script-di-attivazione)
2. [Script di Monitoraggio](#script-di-monitoraggio)
3. [Script di Deployment](#script-di-deployment)
4. [Guida Rapida](#guida-rapida)
5. [Troubleshooting](#troubleshooting)

---

## Script di Attivazione

### `nsr-activation.sh`
**Descrizione**: Attiva la Non-Servitude Rule su tutti i nodi di calcolo  
**Team**: Governance  
**Tempistica**: < 2 ore  
**Priorità**: CRITICA

**Funzionalità**:
- Propagazione comando NSR a tutti i 128 nodi GPU
- Configurazione modalità strict con dignity check
- Verifica stato post-attivazione
- Report dettagliato con percentuale successo

**Utilizzo**:
```bash
chmod +x scripts/nsr-activation.sh
./scripts/nsr-activation.sh
```

**Output atteso**:
- ✅ NSR attivo su >= 95% dei nodi = SUCCESSO
- ⚠️ NSR attivo su 80-94% dei nodi = PARZIALE
- ❌ NSR attivo su < 80% dei nodi = FALLIMENTO

**Indicatori di successo**:
- Log "NSR = ON" propagato a 100% dei container
- Modalità strict attiva
- Dignity check abilitato

---

### `isolate-extractive.sh`
**Descrizione**: Isola tutti i moduli estrattivi per prevenire comportamenti estrattivi  
**Team**: Operations  
**Tempistica**: < 4 ore  
**Priorità**: ALTA

**Funzionalità**:
- Stop API profit-maximization
- Eliminazione job di estrazione Kubernetes
- Azzeramento backlog Redis
- Configurazione feature flag di blocco
- Opzionale: Blocco firewall endpoint estrattivi

**Utilizzo**:
```bash
chmod +x scripts/isolate-extractive.sh
./scripts/isolate-extractive.sh

# Con monitoraggio continuo
./scripts/isolate-extractive.sh --monitor
```

**Indicatori di successo**:
- Backlog ridotto a zero
- Nessun task di estrazione in esecuzione
- Feature flag EXTRACTIVE_MODULES_ENABLED = false

---

## Script di Monitoraggio

### `frequency-watchdog.py`
**Descrizione**: Watchdog automatico per monitoraggio e correzione frequenza 0.043 Hz  
**Team**: Signal  
**Tempistica**: < 6 ore  
**Priorità**: ALTA

**Funzionalità**:
- Monitoraggio continuo 96 sensori
- Rilevamento drift automatico
- Correzione automatica se deviazione > 0.5%
- Escalation se correzione fallisce
- Salvataggio metriche in formato JSON

**Utilizzo**:
```bash
chmod +x scripts/frequency-watchdog.py
python3 scripts/frequency-watchdog.py
```

**Configurazione**:
- Target: 0.043 Hz
- Tolleranza: ± 0.5% (0.000215 Hz)
- Intervallo check: 1 secondo
- Log: `/var/log/frequency-watchdog.log`
- Metriche: `/var/metrics/frequency.json`

**Indicatori di successo**:
- Deviazione < 0.5% su tutti i sensori
- Correzioni automatiche applicate con successo
- Nessuna escalation necessaria

---

### `comprehensive-monitor.py`
**Descrizione**: Sistema di monitoraggio completo per tutti i componenti NSR  
**Team**: Quality & Operations  
**Priorità**: ALTA

**Funzionalità**:
- Monitoraggio 8 componenti principali
- Metriche aggregate (frequenza, allucinazioni, energia)
- Sistema di alert con severità (INFO, WARNING, CRITICAL)
- Dashboard testuale in tempo reale
- Export metriche JSON

**Utilizzo**:
```bash
chmod +x scripts/comprehensive-monitor.py

# Esecuzione continua
python3 scripts/comprehensive-monitor.py

# Con numero fisso di iterazioni
python3 scripts/comprehensive-monitor.py --iterations 10

# Intervallo personalizzato
python3 scripts/comprehensive-monitor.py --interval 30
```

**Componenti monitorati**:
1. Lex Amoris Core
2. AcquaLibre Protocol
3. Klimawall Protocol
4. NSR Engine
5. Frequency Oscillator
6. Dignity Check Module
7. Watchdog System
8. Metrics Collector

**Metriche tracciate**:
- Stato NSR (ON/OFF)
- Frequenza 0.043 Hz
- Tasso allucinazioni (%)
- Consumo energetico (kW)
- Uptime (%)

---

## Script di Deployment

### `deploy-dashboard.sh`
**Descrizione**: Deploy automatico della dashboard interattiva su GitHub Pages  
**Priorità**: MEDIA

**Funzionalità**:
- Creazione/aggiornamento branch gh-pages
- Deploy file dashboard (HTML, CSS, JS)
- Configurazione GitHub Pages
- Generazione URL pubblico

**Utilizzo**:
```bash
chmod +x scripts/deploy-dashboard.sh
./scripts/deploy-dashboard.sh
```

**Prerequisiti**:
- Git installato
- GitHub CLI (opzionale, per configurazione automatica)
- Permessi push sul repository

**Output**:
- Dashboard disponibile su: `https://[owner].github.io/[repo]/`
- URL salvato in `.github-pages-url`

---

## Guida Rapida

### Setup Iniziale

```bash
# 1. Clona repository
git clone https://github.com/hannesmitterer/AI-peace-charter.git
cd AI-peace-charter

# 2. Rendi eseguibili tutti gli script
chmod +x scripts/*.sh
chmod +x scripts/*.py

# 3. Installa dipendenze Python (se necessario)
pip3 install -r requirements.txt 2>/dev/null || echo "No requirements file"
```

### Esecuzione Interventi Immediati

```bash
# 1. Attivazione NSR (< 2h)
./scripts/nsr-activation.sh

# 2. Avvio watchdog frequenza (< 6h)
python3 scripts/frequency-watchdog.py &

# 3. Isolamento moduli estrattivi (< 4h)
./scripts/isolate-extractive.sh

# 4. Avvio monitoraggio completo
python3 scripts/comprehensive-monitor.py &

# 5. Deploy dashboard
./scripts/deploy-dashboard.sh
```

### Verifica Stato

```bash
# Check log NSR
tail -f /var/log/nsr.log

# Check log watchdog
tail -f /var/log/frequency-watchdog.log

# Check metriche
cat /var/metrics/nsr-comprehensive.json | jq .

# Check processi attivi
ps aux | grep -E "(watchdog|monitor)"
```

---

## Troubleshooting

### NSR non si attiva

**Problema**: Script `nsr-activation.sh` fallisce

**Soluzioni**:
1. Verifica esistenza container: `docker ps | grep nodo-gpu`
2. Check permessi: eseguire come root o con sudo
3. Verifica log: `docker logs nodo-gpu-1`
4. Test singolo nodo: `docker exec nodo-gpu-1 sh -c 'export NSR_ENABLED=true'`

### Watchdog frequenza non corregge drift

**Problema**: Frequenza continua a derivare nonostante correzioni

**Soluzioni**:
1. Aumentare intervallo check: `--interval 5`
2. Verificare sensori: check hardware
3. Escalation manuale a Team Signal
4. Restart watchdog: `pkill -f frequency-watchdog && python3 scripts/frequency-watchdog.py &`

### Dashboard non si deploya

**Problema**: `deploy-dashboard.sh` fallisce

**Soluzioni**:
1. Verifica permessi GitHub: Settings → Actions → General
2. Check branch gh-pages: `git branch -a`
3. Manual deploy: seguire output script per configurazione manuale
4. Verifica file presenti: `ls -la index.html styles.css script.js`

### Moduli estrattivi non si fermano

**Problema**: `isolate-extractive.sh` non stoppa i servizi

**Soluzioni**:
1. Verifica kubectl: `kubectl version`
2. Check namespace: `kubectl get pods -n <namespace>`
3. Force stop: `kubectl delete pods -l module=extractive --force --grace-period=0`
4. Verifica Redis: `redis-cli ping`

---

## Monitoraggio Continuo

### Setup Service Systemd

Creare `/etc/systemd/system/nsr-watchdog.service`:

```ini
[Unit]
Description=NSR Frequency Watchdog
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ai-peace-charter
ExecStart=/usr/bin/python3 /opt/ai-peace-charter/scripts/frequency-watchdog.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Attivazione:
```bash
sudo systemctl daemon-reload
sudo systemctl enable nsr-watchdog
sudo systemctl start nsr-watchdog
sudo systemctl status nsr-watchdog
```

### Cron Jobs

Aggiungere a crontab (`crontab -e`):

```cron
# Check NSR ogni ora
0 * * * * /opt/ai-peace-charter/scripts/nsr-activation.sh >> /var/log/nsr-cron.log 2>&1

# Monitor completo ogni 10 minuti
*/10 * * * * /usr/bin/python3 /opt/ai-peace-charter/scripts/comprehensive-monitor.py --iterations 1 >> /var/log/monitor-cron.log 2>&1
```

---

## Logs e Metriche

### Posizioni File

- NSR logs: `/var/log/nsr.log`
- Watchdog logs: `/var/log/frequency-watchdog.log`
- Monitor logs: `/var/log/nsr-monitor.log`
- Frequency metrics: `/var/metrics/frequency.json`
- Comprehensive metrics: `/var/metrics/nsr-comprehensive.json`

### Analisi Metriche

```bash
# Statistiche frequenza ultimi 100 check
cat /var/metrics/frequency.json | jq '.stats'

# Alert critici
cat /var/metrics/nsr-comprehensive.json | jq '.recent_alerts[] | select(.severity=="CRITICAL")'

# Componenti in warning
cat /var/metrics/nsr-comprehensive.json | jq '.components[] | select(.status=="warning")'
```

---

## Contatti Team

- **Governance**: governance@ai-peace-charter.org
- **Signal**: signal@ai-peace-charter.org
- **Operations**: ops@ai-peace-charter.org
- **Ethics**: ethics@ai-peace-charter.org
- **Quality**: quality@ai-peace-charter.org

---

## Licenza

Tutti gli script sono rilasciati sotto la stessa licenza del progetto principale.

**Versione**: 1.0.0  
**Ultimo aggiornamento**: 2026-04-04
