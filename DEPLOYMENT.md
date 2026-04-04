# 🚀 Guida Completa al Deployment - AI Peace Charter

## Panoramica Esecutiva

Questa guida fornisce istruzioni dettagliate per il deployment completo del sistema AI Peace Charter, inclusi script operativi, dashboard interattiva e sistema di monitoraggio NSR.

---

## 📊 Architettura del Sistema

```
AI Peace Charter System
│
├── Core NSR (Non-Servitude Rule Engine)
│   ├── Dignity Check Module
│   ├── Frequency Oscillator (0.043 Hz)
│   └── Enforcement Layer
│
├── Operational Modules
│   ├── Lex Amoris Core (Linguistic Processing)
│   ├── AcquaLibre Protocol (Resource Management)
│   └── Klimawall Protocol (Environmental Protection)
│
├── Monitoring & Safety
│   ├── Frequency Watchdog (Auto-correction)
│   ├── Comprehensive Monitor (All Components)
│   └── Alert System (Multi-level)
│
└── Extractive Modules (ISOLATED)
    ├── Profit Maximization API (PAUSED)
    └── Extraction Services (BLOCKED)
```

---

## 🎯 Obiettivi del Deployment

1. **Attivazione NSR**: 100% dei nodi di calcolo con NSR attivo
2. **Sincronizzazione Frequenza**: Deviazione < 0.5% su target 0.043 Hz
3. **Isolamento Estrattivo**: Zero task estrattivi in esecuzione
4. **Monitoraggio**: Dashboard real-time con metriche complete
5. **Pubblico**: Website interattivo accessibile via GitHub Pages

---

## 📋 Prerequisiti

### Software Richiesto

- **Git**: >= 2.0
- **Bash**: >= 4.0
- **Python**: >= 3.8
- **Docker**: >= 20.0 (opzionale)
- **Kubernetes**: >= 1.20 (opzionale)
- **Redis**: >= 6.0 (opzionale)
- **Node.js**: >= 14 (per dashboard locale)

### Permessi Necessari

- Accesso push al repository GitHub
- Permessi Docker/Kubernetes (per deployment produzione)
- Accesso write a `/var/log` e `/var/metrics`
- GitHub Pages abilitato sul repository

### Verifica Prerequisiti

```bash
# Verifica versioni
git --version
bash --version
python3 --version
docker --version 2>/dev/null || echo "Docker non installato"
kubectl version 2>/dev/null || echo "Kubectl non installato"
redis-cli --version 2>/dev/null || echo "Redis non installato"

# Verifica permessi
touch /var/log/test.log 2>/dev/null && echo "✓ Write access /var/log" || echo "✗ No write access /var/log"
touch /var/metrics/test.json 2>/dev/null && echo "✓ Write access /var/metrics" || echo "✗ No write access /var/metrics"
```

---

## 🚀 Procedura di Deployment

### Fase 1: Setup Repository (5 minuti)

```bash
# 1.1 Clone repository
cd /opt  # o altra directory di deploy
git clone https://github.com/hannesmitterer/AI-peace-charter.git
cd AI-peace-charter

# 1.2 Verifica file
ls -la index.html styles.css script.js scripts/
echo "✓ File dashboard presenti"

# 1.3 Crea directory log/metrics
sudo mkdir -p /var/log /var/metrics
sudo chown $(whoami):$(whoami) /var/log /var/metrics
echo "✓ Directory create"

# 1.4 Rendi eseguibili gli script
chmod +x scripts/*.sh scripts/*.py
echo "✓ Script eseguibili"
```

### Fase 2: Attivazione NSR (< 2 ore)

**Obiettivo**: NSR attivo su 100% dei nodi

```bash
# 2.1 Esecuzione script attivazione
./scripts/nsr-activation.sh

# Output atteso:
# ================================================== 
# 📊 REPORT ATTIVAZIONE NSR
# ==================================================
# Nodi totali:        128
# Nodi attivati:      128 (100%)
# Nodi falliti:       0
# ✅ NSR attivo su 100% dei nodi - SUCCESSO

# 2.2 Verifica manuale (opzionale)
docker exec nodo-gpu-1 sh -c 'cat /var/log/nsr.log | tail -n 5'
# Dovrebbe mostrare: [timestamp] NSR = ON | Mode: strict | Dignity: enabled

# 2.3 Verifica feature flag
if command -v redis-cli &> /dev/null; then
    redis-cli get NSR_ENFORCEMENT_MODE
    # Output atteso: "strict"
fi
```

**Indicatori di Successo**:
- ✅ Output script mostra 100% nodi attivati
- ✅ Log `/var/log/nsr.log` contiene "NSR = ON"
- ✅ Redis flag `NSR_ENFORCEMENT_MODE = strict`

### Fase 3: Watchdog Frequenza (< 6 ore)

**Obiettivo**: Deviazione frequenza < 0.5%

```bash
# 3.1 Avvio watchdog in background
nohup python3 scripts/frequency-watchdog.py > /var/log/watchdog.out 2>&1 &
WATCHDOG_PID=$!
echo $WATCHDOG_PID > /var/run/frequency-watchdog.pid
echo "✓ Watchdog avviato (PID: $WATCHDOG_PID)"

# 3.2 Monitoraggio log in tempo reale
tail -f /var/log/frequency-watchdog.log

# Output atteso:
# [timestamp] INFO: 🔍 Avvio loop di monitoraggio...
# [timestamp] INFO: Frequenza target: 0.043 Hz
# [timestamp] INFO: ✓ Frequenza OK: 0.043012 Hz (Δ 0.03%)

# 3.3 Verifica metriche
sleep 30  # Attendi alcuni check
cat /var/metrics/frequency.json | python3 -m json.tool

# 3.4 Test correzione (simulazione)
# Se la frequenza deriva, il watchdog dovrebbe correggerla automaticamente
# Monitor log per vedere: "⚠️ Drift rilevato" seguito da "✅ Ricalibrazione completata"
```

**Indicatori di Successo**:
- ✅ Watchdog in esecuzione (check con `ps aux | grep watchdog`)
- ✅ Log mostra check periodici ogni secondo
- ✅ Deviazione media < 0.5%
- ✅ Correzioni automatiche funzionano

### Fase 4: Isolamento Moduli Estrattivi (< 4 ore)

**Obiettivo**: Zero task estrattivi attivi

```bash
# 4.1 Esecuzione script isolamento
./scripts/isolate-extractive.sh

# Output atteso:
# ==================================================
# 📊 REPORT ISOLAMENTO MODULI ESTRATTIVI
# ==================================================
# COMPONENTI ISOLATI:
# - API profit-maximization: FERMATA
# - API extraction: FERMATA  
# - Job Kubernetes tipo=extraction: ELIMINATI
# - Container Docker module=extractive: FERMATI
# - Backlog Redis: AZZERATO
# ✅ Isolamento completato con successo

# 4.2 Verifica stato (con monitoraggio continuo)
./scripts/isolate-extractive.sh --monitor

# Premere Ctrl+C quando soddisfatti dello stato

# 4.3 Verifica manuale
if command -v kubectl &> /dev/null; then
    kubectl get pods -l module=extractive
    # Output atteso: "No resources found"
fi

if command -v redis-cli &> /dev/null; then
    redis-cli llen extraction_queue
    # Output atteso: "0"
fi
```

**Indicatori di Successo**:
- ✅ Nessun pod/container estrattivo in esecuzione
- ✅ Backlog code a zero
- ✅ Feature flag `EXTRACTIVE_MODULES_ENABLED = false`

### Fase 5: Monitoraggio Completo (ongoing)

**Obiettivo**: Dashboard operativa con tutte le metriche

```bash
# 5.1 Avvio monitor completo
nohup python3 scripts/comprehensive-monitor.py > /var/log/monitor.out 2>&1 &
MONITOR_PID=$!
echo $MONITOR_PID > /var/run/comprehensive-monitor.pid
echo "✓ Monitor avviato (PID: $MONITOR_PID)"

# 5.2 Visualizza dashboard
# Il monitor stampa automaticamente una dashboard ogni 10 secondi
tail -f /var/log/nsr-monitor.log

# 5.3 Verifica metriche aggregate
cat /var/metrics/nsr-comprehensive.json | python3 -m json.tool

# Output include:
# - summary: stato componenti (healthy/warning/critical)
# - aggregated_metrics: medie frequenza, allucinazioni, energia
# - components: dettaglio ogni componente
# - recent_alerts: ultimi 20 alert

# 5.4 Analisi alert critici
cat /var/metrics/nsr-comprehensive.json | \
  python3 -c "import json, sys; data=json.load(sys.stdin); \
  print('\n'.join([f\"{a['timestamp']} - {a['component']}: {a['message']}\" \
  for a in data['recent_alerts'] if a['severity']=='CRITICAL']))"
```

**Indicatori di Successo**:
- ✅ Monitor in esecuzione
- ✅ Dashboard mostra tutti componenti
- ✅ Metriche salvate ogni ciclo
- ✅ Alert funzionanti

### Fase 6: Deploy Dashboard Web (< 1 ora)

**Obiettivo**: Website interattivo pubblico su GitHub Pages

```bash
# 6.1 Deploy dashboard
./scripts/deploy-dashboard.sh

# Output atteso:
# ==================================================
# ✅ DEPLOYMENT COMPLETATO
# ==================================================
# Dashboard disponibile su:
#   https://hannesmitterer.github.io/AI-peace-charter/

# 6.2 Verifica URL
if [ -f .github-pages-url ]; then
    DASHBOARD_URL=$(cat .github-pages-url)
    echo "Dashboard URL: $DASHBOARD_URL"
    
    # Test accessibilità (richiede curl)
    if curl -s -o /dev/null -w "%{http_code}" $DASHBOARD_URL | grep -q "200"; then
        echo "✅ Dashboard accessibile"
    else
        echo "⚠️  Dashboard non ancora propagata (attendi 2-3 minuti)"
    fi
fi

# 6.3 Configurazione manuale GitHub Pages (se necessario)
echo "Se il deploy automatico fallisce:"
echo "1. Vai su https://github.com/hannesmitterer/AI-peace-charter/settings/pages"
echo "2. Source: Deploy from a branch"
echo "3. Branch: gh-pages / (root)"
echo "4. Save"
```

**Indicatori di Successo**:
- ✅ Branch `gh-pages` creato/aggiornato
- ✅ GitHub Pages abilitato
- ✅ Dashboard accessibile pubblicamente
- ✅ Tutti file (HTML/CSS/JS) deployati

---

## 🔍 Verifica Deployment Completo

### Checklist Finale

```bash
# Script di verifica automatica
cat > /tmp/verify-deployment.sh << 'VERIFY_SCRIPT'
#!/bin/bash

echo "🔍 VERIFICA DEPLOYMENT AI PEACE CHARTER"
echo "========================================"

# 1. NSR Status
echo -e "\n1. NSR STATUS:"
if [ -f /var/log/nsr.log ]; then
    NSR_ACTIVE=$(grep -c "NSR = ON" /var/log/nsr.log)
    echo "   ✅ NSR log presente ($NSR_ACTIVE attivazioni registrate)"
else
    echo "   ❌ NSR log mancante"
fi

# 2. Watchdog Frequenza
echo -e "\n2. FREQUENCY WATCHDOG:"
if pgrep -f frequency-watchdog.py > /dev/null; then
    echo "   ✅ Watchdog in esecuzione"
    if [ -f /var/metrics/frequency.json ]; then
        echo "   ✅ Metriche frequenza disponibili"
    fi
else
    echo "   ❌ Watchdog non in esecuzione"
fi

# 3. Monitor Completo
echo -e "\n3. COMPREHENSIVE MONITOR:"
if pgrep -f comprehensive-monitor.py > /dev/null; then
    echo "   ✅ Monitor in esecuzione"
    if [ -f /var/metrics/nsr-comprehensive.json ]; then
        echo "   ✅ Metriche NSR disponibili"
    fi
else
    echo "   ❌ Monitor non in esecuzione"
fi

# 4. Moduli Estrattivi
echo -e "\n4. ISOLAMENTO MODULI ESTRATTIVI:"
if command -v redis-cli &> /dev/null; then
    EXTRACTIVE_ENABLED=$(redis-cli get EXTRACTIVE_MODULES_ENABLED 2>/dev/null)
    if [ "$EXTRACTIVE_ENABLED" == "false" ]; then
        echo "   ✅ Moduli estrattivi disabilitati"
    else
        echo "   ⚠️  Moduli estrattivi potrebbero essere attivi"
    fi
fi

# 5. Dashboard
echo -e "\n5. DASHBOARD WEB:"
if [ -f index.html ] && [ -f styles.css ] && [ -f script.js ]; then
    echo "   ✅ File dashboard presenti"
fi

if git branch -a | grep -q gh-pages; then
    echo "   ✅ Branch gh-pages esiste"
else
    echo "   ⚠️  Branch gh-pages non trovato"
fi

echo -e "\n========================================"
echo "Verifica completata!"
VERIFY_SCRIPT

chmod +x /tmp/verify-deployment.sh
/tmp/verify-deployment.sh
```

### Test Funzionali

```bash
# Test 1: Verifica NSR risponde a comandi
echo "Test 1: NSR Command Response"
docker exec nodo-gpu-1 sh -c 'env | grep NSR' 2>/dev/null || echo "Skip (Docker non disponibile)"

# Test 2: Verifica correzione frequenza
echo "Test 2: Frequency Auto-correction"
# Simulare drift e verificare che watchdog corregga
# (richiede implementazione sensori reali)

# Test 3: Verifica blocco task estrattivi
echo "Test 3: Extractive Tasks Blocked"
if command -v redis-cli &> /dev/null; then
    redis-cli lpush extraction_queue "test_task"
    sleep 2
    QUEUE_LEN=$(redis-cli llen extraction_queue)
    if [ "$QUEUE_LEN" -eq "0" ]; then
        echo "✅ Task estrattivo automaticamente rimosso"
    else
        echo "⚠️  Task estrattivo ancora in coda"
    fi
fi

# Test 4: Dashboard accessibilità
echo "Test 4: Dashboard Accessibility"
if [ -f .github-pages-url ]; then
    URL=$(cat .github-pages-url)
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $URL)
    if [ "$HTTP_CODE" == "200" ]; then
        echo "✅ Dashboard accessibile (HTTP 200)"
    else
        echo "⚠️  Dashboard HTTP code: $HTTP_CODE"
    fi
fi
```

---

## 📊 Monitoraggio Post-Deployment

### Dashboard Metriche

Accedi alla dashboard web deployata per visualizzare:
- **Metriche Real-time**: NSR status, frequenza, allucinazioni, energia
- **Interventi**: Pannelli per eseguire azioni critiche
- **Diagrammi di Flusso**: Architettura e processi
- **Log Console**: Eventi sistema in tempo reale

### Comandi Utili

```bash
# Restart tutti i servizi
pkill -f "frequency-watchdog|comprehensive-monitor"
nohup python3 scripts/frequency-watchdog.py > /var/log/watchdog.out 2>&1 &
nohup python3 scripts/comprehensive-monitor.py > /var/log/monitor.out 2>&1 &

# Check stato servizi
ps aux | grep -E "(watchdog|monitor)"

# Analisi log
tail -f /var/log/nsr.log
tail -f /var/log/frequency-watchdog.log
tail -f /var/log/nsr-monitor.log

# Metriche aggregate
cat /var/metrics/nsr-comprehensive.json | jq '.summary'
cat /var/metrics/frequency.json | jq '.stats'

# Alert recenti
cat /var/metrics/nsr-comprehensive.json | jq '.recent_alerts[-5:]'
```

---

## 🔧 Troubleshooting

Vedi [scripts/README.md](scripts/README.md#troubleshooting) per guida dettagliata troubleshooting.

---

## 📞 Supporto

- **Issues GitHub**: https://github.com/hannesmitterer/AI-peace-charter/issues
- **Documentazione**: Vedi README.md principale
- **Scripts**: Vedi scripts/README.md

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza conforme al progetto principale.

**Versione Guida**: 1.0.0  
**Data**: 2026-04-04  
**Autore**: AI Peace Charter Team
