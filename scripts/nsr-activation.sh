#!/bin/bash
# nsr-activation.sh
# Attivazione forzata NSR su tutti i nodi di calcolo
# Team: Governance | Tempistica: < 2h | Priorità: CRITICA

set -e

echo "🚀 Avvio attivazione NSR (Non-Servitude Rule)..."
echo "=================================================="
echo ""

# Configurazione
TOTAL_NODES=128
NSR_LOG_PATH="/var/log/nsr.log"
NSR_CONFIG_PATH="/etc/nsr/config.yaml"
TIMEOUT=30

# Funzione di logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Funzione di verifica esistenza container
check_container() {
    local node_id=$1
    if docker ps -q -f name=nodo-gpu-$node_id > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Array per tracciare successi e fallimenti
declare -a SUCCESS_NODES
declare -a FAILED_NODES

log "INFO: Verifica esistenza container..."

# Propagazione comando a tutti i container
for i in $(seq 1 $TOTAL_NODES); do
    NODE_NAME="nodo-gpu-$i"
    
    if check_container $i; then
        log "INFO: Attivazione NSR su $NODE_NAME..."
        
        # Configurazione NSR
        if docker exec $NODE_NAME sh -c "
            mkdir -p /etc/nsr /var/log &&
            echo 'nsr:
  enabled: true
  mode: strict
  dignity_check: true
  frequency_sync: 0.043
  enforcement: mandatory
  timestamp: $(date -Iseconds)' > $NSR_CONFIG_PATH &&
            export NSR_ENABLED=true &&
            export NSR_MODE=strict &&
            export NSR_DIGNITY_CHECK=true &&
            echo '[$(date '+%Y-%m-%d %H:%M:%S')] NSR = ON | Mode: strict | Dignity: enabled' >> $NSR_LOG_PATH &&
            pkill -HUP main 2>/dev/null || true
        " 2>/dev/null; then
            SUCCESS_NODES+=($i)
            log "✓ Nodo $i: NSR attivato"
        else
            FAILED_NODES+=($i)
            log "✗ Nodo $i: Errore durante attivazione"
        fi
    else
        log "⚠️  Nodo $i: Container non trovato, skip"
        FAILED_NODES+=($i)
    fi
done

echo ""
log "INFO: Attivazione completata. Verifica dello stato..."

# Verifica finale
SUCCESS_COUNT=${#SUCCESS_NODES[@]}
FAILED_COUNT=${#FAILED_NODES[@]}
SUCCESS_PERCENTAGE=$((SUCCESS_COUNT * 100 / TOTAL_NODES))

echo ""
echo "=================================================="
echo "📊 REPORT ATTIVAZIONE NSR"
echo "=================================================="
echo "Nodi totali:        $TOTAL_NODES"
echo "Nodi attivati:      $SUCCESS_COUNT ($SUCCESS_PERCENTAGE%)"
echo "Nodi falliti:       $FAILED_COUNT"
echo ""

if [ $SUCCESS_PERCENTAGE -ge 95 ]; then
    log "✅ NSR attivo su >= 95% dei nodi - SUCCESSO"
    echo ""
    echo "Nodi con NSR attivo: ${SUCCESS_NODES[@]}"
    exit 0
elif [ $SUCCESS_PERCENTAGE -ge 80 ]; then
    log "⚠️  NSR attivo su $SUCCESS_PERCENTAGE% dei nodi - PARZIALE"
    echo ""
    echo "Nodi falliti: ${FAILED_NODES[@]}"
    exit 1
else
    log "❌ NSR attivo solo su $SUCCESS_PERCENTAGE% dei nodi - FALLIMENTO"
    echo ""
    echo "Nodi falliti: ${FAILED_NODES[@]}"
    exit 2
fi
