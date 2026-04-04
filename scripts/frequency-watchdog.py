#!/usr/bin/env python3
"""
frequency-watchdog.py
Watchdog per monitoraggio e correzione automatica della frequenza 0.043 Hz
Team: Signal | Tempistica: < 6h | Priorità: ALTA
"""

import time
import sys
import signal
import logging
from datetime import datetime
from typing import List, Dict
import json

# Configurazione
TARGET_FREQ = 0.043  # Hz
TOLERANCE = 0.0005   # 0.5% (0.000215 Hz)
CHECK_INTERVAL = 1.0  # secondi
LOG_FILE = '/var/log/frequency-watchdog.log'
METRICS_FILE = '/var/metrics/frequency.json'

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class FrequencySensor:
    """Simulazione sensore di frequenza"""
    
    def __init__(self, sensor_id: int, base_freq: float = 0.043):
        self.sensor_id = sensor_id
        self.base_freq = base_freq
        self.offset = 0.0
        self.drift_factor = (sensor_id % 10) / 10000  # Drift simulato
        
    def read(self) -> float:
        """Legge la frequenza corrente con drift simulato"""
        import random
        noise = random.uniform(-0.0001, 0.0001)
        drift = self.drift_factor * time.time() / 10000
        return self.base_freq + self.offset + drift + noise
    
    def apply_offset(self, offset: float):
        """Applica un offset di correzione"""
        self.offset += offset
        logger.info(f"Sensore {self.sensor_id}: offset applicato {offset:.6f} Hz")

class FrequencyWatchdog:
    """Watchdog principale per monitoraggio frequenza"""
    
    def __init__(self, num_sensors: int = 96):
        self.sensors: List[FrequencySensor] = []
        self.running = True
        self.stats = {
            'corrections': 0,
            'total_checks': 0,
            'max_deviation': 0.0,
            'uptime_start': datetime.now().isoformat()
        }
        
        # Inizializza sensori
        logger.info(f"Inizializzazione di {num_sensors} sensori...")
        for i in range(num_sensors):
            self.sensors.append(FrequencySensor(i))
        
        logger.info(f"✓ {len(self.sensors)} sensori inizializzati")
        
    def handle_shutdown(self, signum, frame):
        """Gestione shutdown graceful"""
        logger.info("Segnale di shutdown ricevuto")
        self.running = False
        self.save_metrics()
        sys.exit(0)
    
    def calculate_statistics(self, frequencies: List[float]) -> Dict:
        """Calcola statistiche sulle frequenze"""
        avg_freq = sum(frequencies) / len(frequencies)
        deviation = abs(avg_freq - TARGET_FREQ)
        deviation_pct = (deviation / TARGET_FREQ) * 100
        
        return {
            'avg': avg_freq,
            'min': min(frequencies),
            'max': max(frequencies),
            'deviation': deviation,
            'deviation_pct': deviation_pct,
            'in_tolerance': deviation <= TOLERANCE
        }
    
    def apply_correction(self, avg_freq: float):
        """Applica correzione di frequenza a tutti i sensori"""
        offset = TARGET_FREQ - avg_freq
        
        logger.warning(f"⚠️  Drift rilevato - Applicazione correzione")
        logger.info(f"📊 Offset richiesto: {offset:.6f} Hz")
        
        # Applica offset a tutti i sensori
        for sensor in self.sensors:
            sensor.apply_offset(offset)
        
        self.stats['corrections'] += 1
        logger.info("✅ Ricalibrazione completata su tutti i sensori")
        
        # Verifica post-correzione
        time.sleep(0.5)
        verify_frequencies = [s.read() for s in self.sensors]
        verify_stats = self.calculate_statistics(verify_frequencies)
        
        if verify_stats['in_tolerance']:
            logger.info(f"✓ Verifica post-correzione OK: {verify_stats['avg']:.6f} Hz")
            return True
        else:
            logger.error(f"✗ Verifica post-correzione FALLITA: {verify_stats['avg']:.6f} Hz")
            logger.error("⚠️  ESCALATION: Notifica Team Signal richiesta")
            return False
    
    def save_metrics(self):
        """Salva metriche su file"""
        try:
            with open(METRICS_FILE, 'w') as f:
                json.dump(self.stats, f, indent=2)
            logger.info(f"Metriche salvate in {METRICS_FILE}")
        except Exception as e:
            logger.error(f"Errore nel salvataggio metriche: {e}")
    
    def monitor_loop(self):
        """Loop principale di monitoraggio"""
        logger.info("🔍 Avvio loop di monitoraggio...")
        logger.info(f"Frequenza target: {TARGET_FREQ} Hz")
        logger.info(f"Tolleranza: ±{TOLERANCE} Hz ({TOLERANCE/TARGET_FREQ*100:.2f}%)")
        logger.info(f"Intervallo check: {CHECK_INTERVAL}s")
        logger.info("")
        
        # Registra handler per shutdown
        signal.signal(signal.SIGINT, self.handle_shutdown)
        signal.signal(signal.SIGTERM, self.handle_shutdown)
        
        while self.running:
            try:
                # Leggi tutte le frequenze
                frequencies = [sensor.read() for sensor in self.sensors]
                stats = self.calculate_statistics(frequencies)
                
                self.stats['total_checks'] += 1
                self.stats['max_deviation'] = max(
                    self.stats['max_deviation'],
                    stats['deviation']
                )
                
                # Logging dello stato
                if stats['in_tolerance']:
                    logger.info(
                        f"✓ Frequenza OK: {stats['avg']:.6f} Hz "
                        f"(Δ {stats['deviation_pct']:.2f}%) "
                        f"[{stats['min']:.6f} - {stats['max']:.6f}]"
                    )
                else:
                    logger.warning(
                        f"⚠️  Frequenza FUORI TOLLERANZA: {stats['avg']:.6f} Hz "
                        f"(Δ {stats['deviation_pct']:.2f}%)"
                    )
                    
                    # Applica correzione
                    success = self.apply_correction(stats['avg'])
                    
                    if not success:
                        # Escalation fallita, continua monitoraggio
                        logger.error("Continuazione monitoraggio nonostante errore")
                
                # Salva metriche periodicamente
                if self.stats['total_checks'] % 100 == 0:
                    self.save_metrics()
                
                time.sleep(CHECK_INTERVAL)
                
            except Exception as e:
                logger.error(f"Errore nel loop di monitoraggio: {e}")
                time.sleep(CHECK_INTERVAL)

def main():
    """Entry point"""
    print("=" * 60)
    print("🛡️  FREQUENCY WATCHDOG 0.043 Hz")
    print("=" * 60)
    print()
    
    try:
        watchdog = FrequencyWatchdog(num_sensors=96)
        watchdog.monitor_loop()
    except KeyboardInterrupt:
        logger.info("\nShutdown richiesto dall'utente")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Errore fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
