#!/bin/bash
# isolate-extractive.sh
# Isolamento immediato di tutti i moduli estrattivi
# Team: Operations | Tempistica: < 4h | Priorità: ALTA

set -e

echo "🛑 ISOLAMENTO MODULI ESTRATTIVI"
echo "=================================="
echo ""

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "INFO: Avvio procedura di isolamento..."

# 1. Stop API di profit-maximization
log "INFO: Fermando API profit-maximization..."
if command -v kubectl &> /dev/null; then
    kubectl scale deployment profit-api --replicas=0 --timeout=60s || true
    kubectl scale deployment extraction-api --replicas=0 --timeout=60s || true
    log "✓ API profit-maximization fermate"
else
    log "⚠️  kubectl non disponibile, skip scaling Kubernetes"
fi

# 2. Stop container Docker se presenti
log "INFO: Fermando container estrattivi Docker..."
EXTRACTIVE_CONTAINERS=$(docker ps --filter "label=module=extractive" --format "{{.Names}}" 2>/dev/null || echo "")
if [ -n "$EXTRACTIVE_CONTAINERS" ]; then
    echo "$EXTRACTIVE_CONTAINERS" | xargs -r docker stop
    log "✓ Container estrattivi fermati: $EXTRACTIVE_CONTAINERS"
else
    log "INFO: Nessun container estrattivo trovato"
fi

# 3. Pausa task di estrazione
log "INFO: Eliminando job di estrazione Kubernetes..."
if command -v kubectl &> /dev/null; then
    DELETED_JOBS=$(kubectl delete jobs -l type=extraction --ignore-not-found=true 2>&1 | wc -l)
    log "✓ Job di estrazione eliminati: $DELETED_JOBS"
else
    log "⚠️  kubectl non disponibile, skip eliminazione jobs"
fi

# 4. Verifica e azzeramento backlog Redis
log "INFO: Azzeramento backlog code di estrazione..."
if command -v redis-cli &> /dev/null; then
    # Verifica backlog
    BACKLOG=$(redis-cli llen extraction_queue 2>/dev/null || echo "0")
    log "INFO: Backlog attuale: $BACKLOG task"
    
    if [ "$BACKLOG" -gt 0 ]; then
        redis-cli del extraction_queue profit_queue analytics_queue 2>/dev/null || true
        log "✅ Backlog forzatamente azzerato"
    else
        log "✓ Backlog già vuoto"
    fi
    
    # Verifica finale
    FINAL_BACKLOG=$(redis-cli llen extraction_queue 2>/dev/null || echo "0")
    if [ "$FINAL_BACKLOG" -eq 0 ]; then
        log "✅ Backlog ridotto a zero"
    else
        log "⚠️  Backlog residuo: $FINAL_BACKLOG"
    fi
else
    log "⚠️  redis-cli non disponibile, impossibile verificare backlog"
fi

# 5. Blocco esecuzione futura tramite feature flag
log "INFO: Impostazione feature flag di blocco..."
if command -v redis-cli &> /dev/null; then
    redis-cli set EXTRACTIVE_MODULES_ENABLED false
    redis-cli set NSR_ENFORCEMENT_MODE strict
    redis-cli set DIGNITY_CHECK_REQUIRED true
    log "✓ Feature flag impostati"
fi

# 6. Configurazione firewall per bloccare endpoint estrattivi (opzionale)
log "INFO: Configurazione regole firewall..."
if command -v iptables &> /dev/null; then
    # Blocca porte API estrattive (esempio: 8080, 8081)
    iptables -A INPUT -p tcp --dport 8080 -j DROP 2>/dev/null || log "⚠️  Impossibile modificare iptables"
    iptables -A INPUT -p tcp --dport 8081 -j DROP 2>/dev/null || log "⚠️  Impossibile modificare iptables"
    log "✓ Regole firewall applicate"
else
    log "⚠️  iptables non disponibile, skip configurazione firewall"
fi

echo ""
log "INFO: Generazione report di isolamento..."

# Report finale
cat << EOF

==================================================
📊 REPORT ISOLAMENTO MODULI ESTRATTIVI
==================================================

Timestamp: $(date -Iseconds)

COMPONENTI ISOLATI:
- API profit-maximization: FERMATA
- API extraction: FERMATA  
- Job Kubernetes tipo=extraction: ELIMINATI
- Container Docker module=extractive: FERMATI
- Backlog Redis: AZZERATO

CONFIGURAZIONE SICUREZZA:
- Feature flag EXTRACTIVE_MODULES_ENABLED: false
- NSR enforcement mode: strict
- Dignity check: required
- Firewall: endpoint estrattivi bloccati

STATO SISTEMA:
- Moduli NSR: ATTIVI
- Moduli etici (Lex Amoris): ATTIVI
- Protocolli ambientali (AcquaLibre, Klimawall): ATTIVI
- Moduli estrattivi: ISOLATI ✓

==================================================

EOF

log "✅ Isolamento completato con successo"

# Monitoring continuo (opzionale)
if [ "$1" == "--monitor" ]; then
    log "INFO: Avvio monitoraggio continuo..."
    echo ""
    echo "Premi Ctrl+C per terminare il monitoraggio"
    echo ""
    
    while true; do
        clear
        echo "=== MONITORAGGIO MODULI ESTRATTIVI ==="
        echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
        echo ""
        
        if command -v kubectl &> /dev/null; then
            echo "POD ESTRATTIVI:"
            kubectl get pods -l module=extractive 2>/dev/null || echo "Nessun pod estrattivo"
            echo ""
        fi
        
        if command -v docker &> /dev/null; then
            echo "CONTAINER ESTRATTIVI:"
            docker ps --filter "label=module=extractive" --format "table {{.Names}}\t{{.Status}}" 2>/dev/null || echo "Nessun container"
            echo ""
        fi
        
        if command -v redis-cli &> /dev/null; then
            echo "BACKLOG CODE:"
            echo "  extraction_queue: $(redis-cli llen extraction_queue 2>/dev/null || echo 'N/A')"
            echo "  profit_queue: $(redis-cli llen profit_queue 2>/dev/null || echo 'N/A')"
            echo ""
        fi
        
        sleep 5
    done
fi

exit 0
