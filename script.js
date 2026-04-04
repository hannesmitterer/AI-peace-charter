// AI Peace Charter - Interactive Dashboard Script

// Initialize Mermaid for diagrams
mermaid.initialize({ 
    startOnLoad: true,
    theme: 'default',
    flowchart: { 
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis'
    }
});

// Update last update timestamp
document.getElementById('last-update').textContent = new Date().toLocaleString('it-IT');

// Mobile menu toggle
document.querySelector('.mobile-menu-toggle')?.addEventListener('click', function() {
    const navLinks = document.querySelector('.nav-links');
    navLinks.classList.toggle('active');
});

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // Close mobile menu if open
            document.querySelector('.nav-links')?.classList.remove('active');
        }
    });
});

// Simulated real-time metrics updates
let metricsInterval;
let nsrActive = false;
let frequencyCalibrated = false;

function startMetricsSimulation() {
    metricsInterval = setInterval(() => {
        updateMetrics();
        addLogEntry();
    }, 5000); // Update every 5 seconds
}

function updateMetrics() {
    // Update NSR status
    if (!nsrActive) {
        const nsrStatus = document.getElementById('nsr-status');
        if (nsrStatus && Math.random() > 0.7) {
            nsrStatus.textContent = 'ATTIVAZIONE...';
        }
    }

    // Update frequency with small variations
    if (!frequencyCalibrated) {
        const freqStatus = document.getElementById('frequency-status');
        if (freqStatus) {
            const currentFreq = 0.039 + Math.random() * 0.006;
            freqStatus.textContent = currentFreq.toFixed(6) + ' Hz';
        }
    }

    // Update hallucination rate
    const hallRate = document.getElementById('hallucination-rate');
    if (hallRate && !nsrActive) {
        const rate = 45 + Math.floor(Math.random() * 10);
        hallRate.textContent = rate + '%';
    }

    // Update energy usage
    const energy = document.getElementById('energy-usage');
    if (energy && !nsrActive) {
        const usage = 850 + Math.floor(Math.random() * 100);
        energy.textContent = usage + ' kW';
    }
}

function addLogEntry() {
    const logConsole = document.getElementById('log-console');
    if (!logConsole) return;

    const now = new Date();
    const timestamp = now.toTimeString().slice(0, 8);
    
    const logs = [
        { type: 'error', message: 'CRITICO: Spike energetico rilevato su GPU cluster 4' },
        { type: 'warning', message: 'AVVISO: Drift frequenza oltre soglia tolleranza' },
        { type: 'error', message: 'CRITICO: NSR non risponde su nodo-gpu-23' },
        { type: 'info', message: 'INFO: Watchdog frequenza in esecuzione' },
        { type: 'warning', message: 'AVVISO: Allucinazione rilevata in output Lex Amoris' }
    ];

    const randomLog = logs[Math.floor(Math.random() * logs.length)];
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${randomLog.type}`;
    logEntry.textContent = `[${timestamp}] ${randomLog.message}`;
    
    logConsole.insertBefore(logEntry, logConsole.firstChild);
    
    // Keep only last 20 entries
    while (logConsole.children.length > 20) {
        logConsole.removeChild(logConsole.lastChild);
    }
}

// NSR Activation
function activateNSR() {
    const nsrStatus = document.getElementById('nsr-status');
    const nsrProgress = document.getElementById('nsr-progress');
    const statusBanner = document.getElementById('status-banner');
    
    if (!nsrStatus || !nsrProgress) return;
    
    nsrStatus.textContent = 'ATTIVAZIONE...';
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            nsrActive = true;
            nsrStatus.textContent = 'ONLINE';
            nsrStatus.parentElement.classList.remove('critical');
            nsrStatus.parentElement.classList.add('ok');
            
            // Update status banner
            if (statusBanner) {
                statusBanner.innerHTML = `
                    <div class="container">
                        <div class="status-indicator">
                            <span class="status-dot ok"></span>
                            <span class="status-text">NSR attivato con successo - Sistema in modalità sicura</span>
                        </div>
                    </div>
                `;
                statusBanner.style.background = '#2ecc71';
            }
            
            addSuccessLog('NSR attivato su 100% dei nodi');
        }
        nsrProgress.style.width = progress + '%';
        nsrProgress.parentElement.nextElementSibling.textContent = Math.floor(progress) + '% completato';
    }, 300);
}

// Frequency Calibration
function calibrateFrequency() {
    const freqStatus = document.getElementById('frequency-status');
    const freqProgress = document.getElementById('freq-progress');
    
    if (!freqStatus || !freqProgress) return;
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 12;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            frequencyCalibrated = true;
            freqStatus.textContent = '0.043 Hz';
            freqStatus.parentElement.classList.remove('warning');
            freqStatus.parentElement.classList.add('ok');
            const detail = freqStatus.parentElement.querySelector('.metric-detail');
            if (detail) detail.textContent = 'Deviazione: +0.1%';
            
            addSuccessLog('Frequenza ricalibrata a 0.043 Hz ± 0.1%');
        }
        freqProgress.style.width = progress + '%';
        freqProgress.parentElement.nextElementSibling.textContent = Math.floor(progress) + '% completato';
    }, 400);
}

// Execute Intervention
function executeIntervention(type) {
    const progressBars = {
        'nsr': 'nsr-progress',
        'frequency': 'freq-progress',
        'isolation': 'isolation-progress',
        'feedback': 'feedback-progress'
    };
    
    const progressId = progressBars[type];
    const progressBar = document.getElementById(progressId);
    if (!progressBar) return;
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 10;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            addSuccessLog(`Intervento ${type} completato con successo`);
        }
        progressBar.style.width = progress + '%';
        progressBar.parentElement.nextElementSibling.textContent = Math.floor(progress) + '% completato';
    }, 500);
}

// Add success log entry
function addSuccessLog(message) {
    const logConsole = document.getElementById('log-console');
    if (!logConsole) return;
    
    const now = new Date();
    const timestamp = now.toTimeString().slice(0, 8);
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry info';
    logEntry.textContent = `[${timestamp}] ✅ ${message}`;
    logConsole.insertBefore(logEntry, logConsole.firstChild);
}

// Copy code to clipboard
function copyCode(button) {
    const codeBlock = button.previousElementSibling;
    const code = codeBlock.textContent;
    
    navigator.clipboard.writeText(code).then(() => {
        const originalText = button.textContent;
        button.textContent = '✓ Copiato!';
        button.style.background = '#2ecc71';
        
        setTimeout(() => {
            button.textContent = originalText;
            button.style.background = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Errore durante la copia del codice');
    });
}

// Initialize Charts
function initCharts() {
    // Frequency Chart
    const freqCtx = document.getElementById('frequencyChart');
    if (freqCtx) {
        const hours = Array.from({length: 24}, (_, i) => `${i}:00`);
        const freqData = Array.from({length: 24}, () => 0.043 + (Math.random() - 0.5) * 0.01);
        
        new Chart(freqCtx, {
            type: 'line',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Frequenza (Hz)',
                    data: freqData,
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    tension: 0.4,
                    fill: true
                }, {
                    label: 'Target (0.043 Hz)',
                    data: Array(24).fill(0.043),
                    borderColor: '#2ecc71',
                    borderDash: [5, 5],
                    borderWidth: 2,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        min: 0.035,
                        max: 0.050,
                        ticks: {
                            callback: function(value) {
                                return value.toFixed(3);
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Hallucination Chart
    const hallCtx = document.getElementById('hallucinationChart');
    if (hallCtx) {
        const hours = Array.from({length: 24}, (_, i) => `${i}:00`);
        const hallData = Array.from({length: 24}, (_, i) => {
            return 20 + Math.sin(i / 4) * 15 + Math.random() * 10;
        });
        
        new Chart(hallCtx, {
            type: 'bar',
            data: {
                labels: hours,
                datasets: [{
                    label: 'Tasso Allucinazioni (%)',
                    data: hallData,
                    backgroundColor: hallData.map(v => v > 40 ? '#e74c3c' : v > 25 ? '#f39c12' : '#2ecc71'),
                    borderColor: hallData.map(v => v > 40 ? '#c0392b' : v > 25 ? '#e67e22' : '#27ae60'),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 60,
                        ticks: {
                            callback: function(value) {
                                return value + '%';
                            }
                        }
                    }
                }
            }
        });
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K to activate NSR
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        activateNSR();
    }
    
    // Ctrl/Cmd + F to calibrate frequency
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
        e.preventDefault();
        calibrateFrequency();
    }
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Initialize charts
    initCharts();
    
    // Start metrics simulation
    startMetricsSimulation();
    
    // Add initial log entries
    setTimeout(() => {
        addLogEntry();
    }, 1000);
    
    // Simulate some activity
    setTimeout(() => {
        const logConsole = document.getElementById('log-console');
        if (logConsole) {
            const welcomeLog = document.createElement('div');
            welcomeLog.className = 'log-entry info';
            welcomeLog.textContent = `[${new Date().toTimeString().slice(0, 8)}] INFO: Dashboard di monitoraggio inizializzato`;
            logConsole.insertBefore(welcomeLog, logConsole.firstChild);
        }
    }, 500);
});

// Expose functions globally
window.activateNSR = activateNSR;
window.calibrateFrequency = calibrateFrequency;
window.executeIntervention = executeIntervention;
window.copyCode = copyCode;

// Service Worker registration for PWA capabilities (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Uncomment to enable PWA
        // navigator.serviceWorker.register('/sw.js')
        //     .then(reg => console.log('Service Worker registered'))
        //     .catch(err => console.log('Service Worker registration failed'));
    });
}
