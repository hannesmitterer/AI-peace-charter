#!/bin/bash
# deploy-dashboard.sh
# Deploy dashboard interattivo su GitHub Pages
# Deployment automatizzato della dashboard di monitoraggio NSR

set -e

echo "📦 DEPLOYMENT DASHBOARD AI PEACE CHARTER"
echo "=========================================="
echo ""

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Verifica prerequisiti
log "INFO: Verifica prerequisiti..."

# Check git
if ! command -v git &> /dev/null; then
    log "❌ Git non installato"
    exit 1
fi

# Check gh (GitHub CLI) - opzionale
GH_CLI_AVAILABLE=false
if command -v gh &> /dev/null; then
    GH_CLI_AVAILABLE=true
    log "✓ GitHub CLI disponibile"
else
    log "⚠️  GitHub CLI non disponibile (alcune funzioni limitate)"
fi

# Ottieni informazioni repository
REPO_ROOT=$(git rev-parse --show-toplevel)
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)

log "INFO: Repository root: $REPO_ROOT"
log "INFO: Branch corrente: $CURRENT_BRANCH"

# Vai alla root del repository
cd "$REPO_ROOT"

# Verifica che i file necessari esistano
log "INFO: Verifica file dashboard..."
REQUIRED_FILES=("index.html" "styles.css" "script.js")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        log "❌ File mancante: $file"
        exit 1
    fi
    log "✓ File trovato: $file"
done

# Salva il branch corrente
ORIGINAL_BRANCH=$CURRENT_BRANCH

# Crea/aggiorna branch gh-pages
log "INFO: Preparazione branch gh-pages..."

# Verifica se gh-pages esiste già
if git show-ref --verify --quiet refs/heads/gh-pages; then
    log "INFO: Branch gh-pages esiste, checkout..."
    git checkout gh-pages
    
    # Merge delle modifiche dal branch originale (solo i file dashboard)
    log "INFO: Aggiornamento file dashboard..."
    git checkout $ORIGINAL_BRANCH -- index.html styles.css script.js README.md scripts/ 2>/dev/null || true
else
    log "INFO: Creazione nuovo branch gh-pages..."
    git checkout --orphan gh-pages
    
    # Rimuovi tutti i file tranne quelli necessari
    git rm -rf . 2>/dev/null || true
    
    # Recupera i file dashboard dal branch originale
    git checkout $ORIGINAL_BRANCH -- index.html styles.css script.js README.md scripts/ 2>/dev/null || true
fi

# Crea file .nojekyll per evitare processing Jekyll
log "INFO: Configurazione GitHub Pages..."
touch .nojekyll

# Crea un file README per gh-pages
cat > README-PAGES.md << 'EOF'
# AI Peace Charter - Dashboard

Questa è la dashboard interattiva del progetto AI Peace Charter.

## Accesso

La dashboard è disponibile pubblicamente tramite GitHub Pages.

## Contenuto

- **Dashboard in tempo reale**: Monitoraggio NSR e frequenza 0.043 Hz
- **Interventi immediati**: Pannello di controllo per azioni critiche
- **Diagrammi di flusso**: Visualizzazione architettura del sistema
- **Script di deployment**: Guide operative per l'implementazione

## Tecnologie

- HTML5, CSS3, JavaScript (Vanilla)
- Chart.js per grafici interattivi
- Mermaid.js per diagrammi di flusso
- Design mobile-first responsive

## Aggiornamenti

Questa pagina viene aggiornata automaticamente tramite GitHub Actions ad ogni push sul branch principale.

EOF

# Aggiungi tutti i file
log "INFO: Commit modifiche..."
git add .
git commit -m "Deploy dashboard v$(date +%Y%m%d-%H%M%S)" || log "⚠️  Nessuna modifica da committare"

# Push al remote
log "INFO: Push su origin/gh-pages..."
if git push origin gh-pages --force; then
    log "✅ Push completato con successo"
else
    log "❌ Errore durante il push"
    git checkout $ORIGINAL_BRANCH
    exit 1
fi

# Ritorna al branch originale
log "INFO: Ritorno al branch $ORIGINAL_BRANCH..."
git checkout $ORIGINAL_BRANCH

# Abilita GitHub Pages tramite API (se gh CLI disponibile)
if [ "$GH_CLI_AVAILABLE" = true ]; then
    log "INFO: Configurazione GitHub Pages tramite API..."
    
    # Ottieni owner e repo name
    REPO_INFO=$(gh repo view --json owner,name)
    OWNER=$(echo $REPO_INFO | grep -o '"login":"[^"]*"' | head -1 | cut -d'"' -f4)
    REPO_NAME=$(echo $REPO_INFO | grep -o '"name":"[^"]*"' | head -1 | cut -d'"' -f4)
    
    if [ -n "$OWNER" ] && [ -n "$REPO_NAME" ]; then
        log "INFO: Repository: $OWNER/$REPO_NAME"
        
        # Abilita Pages (può fallire se già abilitato)
        gh api repos/$OWNER/$REPO_NAME/pages \
            -X POST \
            -f source[branch]=gh-pages \
            -f source[path]=/ 2>/dev/null || log "⚠️  Pages già abilitato o errore API"
        
        # URL della dashboard
        PAGES_URL="https://$OWNER.github.io/$REPO_NAME/"
        
        echo ""
        echo "=================================================="
        echo "✅ DEPLOYMENT COMPLETATO"
        echo "=================================================="
        echo ""
        echo "Dashboard disponibile su:"
        echo "  $PAGES_URL"
        echo ""
        echo "Nota: Potrebbero essere necessari alcuni minuti"
        echo "      per la propagazione delle modifiche."
        echo ""
        echo "=================================================="
        
        # Salva URL in un file
        echo $PAGES_URL > .github-pages-url
        log "INFO: URL salvato in .github-pages-url"
    else
        log "⚠️  Impossibile ottenere informazioni repository"
    fi
else
    echo ""
    echo "=================================================="
    echo "✅ DEPLOYMENT COMPLETATO"
    echo "=================================================="
    echo ""
    echo "Per abilitare GitHub Pages:"
    echo "1. Vai su https://github.com/[owner]/[repo]/settings/pages"
    echo "2. Seleziona branch: gh-pages"
    echo "3. Seleziona directory: / (root)"
    echo "4. Clicca 'Save'"
    echo ""
    echo "La dashboard sarà disponibile su:"
    echo "  https://[owner].github.io/[repo]/"
    echo ""
    echo "=================================================="
fi

log "✅ Script completato"
exit 0
