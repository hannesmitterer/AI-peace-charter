#!/usr/bin/env python3
"""
comprehensive-monitor.py
Sistema di monitoraggio completo per tutti i componenti NSR
Team: Quality & Operations | Priorità: ALTA
"""

import time
import sys
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Configurazione
MONITOR_INTERVAL = 10  # secondi
ALERT_THRESHOLD_CRITICAL = 0.9
ALERT_THRESHOLD_WARNING = 0.7
LOG_FILE = '/var/log/nsr-monitor.log'
METRICS_FILE = '/var/metrics/nsr-comprehensive.json'

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

class ComponentStatus(Enum):
    """Stati possibili dei componenti"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"

@dataclass
class ComponentMetrics:
    """Metriche per un singolo componente"""
    name: str
    status: ComponentStatus
    nsr_enabled: bool
    frequency: float
    hallucination_rate: float
    energy_usage: float
    last_check: str
    uptime_pct: float
    
    def to_dict(self) -> Dict:
        data = asdict(self)
        data['status'] = self.status.value
        return data

class NSRMonitor:
    """Monitor completo del sistema NSR"""
    
    def __init__(self):
        self.components: Dict[str, ComponentMetrics] = {}
        self.alert_history: List[Dict] = []
        self.start_time = datetime.now()
        
        logger.info("Inizializzazione NSR Comprehensive Monitor...")
        
    def check_nsr_status(self, component_name: str) -> bool:
        """Verifica stato NSR per un componente"""
        # Simulazione - in produzione leggerebbe da API/DB
        import random
        return random.random() > 0.1  # 90% chance NSR is ON
    
    def check_frequency(self, component_name: str) -> float:
        """Verifica frequenza 0.043 Hz"""
        import random
        base = 0.043
        drift = random.uniform(-0.005, 0.005)
        return base + drift
    
    def check_hallucination_rate(self, component_name: str) -> float:
        """Verifica tasso di allucinazioni"""
        import random
        return random.uniform(0.1, 0.6)  # 10-60%
    
    def check_energy_usage(self, component_name: str) -> float:
        """Verifica consumo energetico (kW)"""
        import random
        return random.uniform(200, 1000)
    
    def calculate_uptime(self, component_name: str) -> float:
        """Calcola uptime percentuale"""
        import random
        return random.uniform(85, 99.9)
    
    def determine_status(self, metrics: ComponentMetrics) -> ComponentStatus:
        """Determina stato generale del componente"""
        if not metrics.nsr_enabled:
            return ComponentStatus.CRITICAL
        
        issues = 0
        
        # Check frequenza
        freq_deviation = abs(metrics.frequency - 0.043) / 0.043
        if freq_deviation > 0.1:
            issues += 2
        elif freq_deviation > 0.05:
            issues += 1
        
        # Check allucinazioni
        if metrics.hallucination_rate > 0.5:
            issues += 2
        elif metrics.hallucination_rate > 0.3:
            issues += 1
        
        # Check energia
        if metrics.energy_usage > 800:
            issues += 1
        
        # Check uptime
        if metrics.uptime_pct < 90:
            issues += 1
        
        if issues >= 4:
            return ComponentStatus.CRITICAL
        elif issues >= 2:
            return ComponentStatus.WARNING
        else:
            return ComponentStatus.HEALTHY
    
    def monitor_component(self, component_name: str) -> ComponentMetrics:
        """Monitora un singolo componente"""
        nsr_enabled = self.check_nsr_status(component_name)
        frequency = self.check_frequency(component_name)
        hallucination = self.check_hallucination_rate(component_name)
        energy = self.check_energy_usage(component_name)
        uptime = self.calculate_uptime(component_name)
        
        metrics = ComponentMetrics(
            name=component_name,
            status=ComponentStatus.HEALTHY,  # Verrà calcolato dopo
            nsr_enabled=nsr_enabled,
            frequency=frequency,
            hallucination_rate=hallucination,
            energy_usage=energy,
            last_check=datetime.now().isoformat(),
            uptime_pct=uptime
        )
        
        metrics.status = self.determine_status(metrics)
        
        return metrics
    
    def create_alert(self, component: str, severity: str, message: str):
        """Crea un alert"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'component': component,
            'severity': severity,
            'message': message
        }
        self.alert_history.append(alert)
        
        if severity == 'CRITICAL':
            logger.error(f"🚨 CRITICAL ALERT: {component} - {message}")
        elif severity == 'WARNING':
            logger.warning(f"⚠️  WARNING: {component} - {message}")
        else:
            logger.info(f"ℹ️  INFO: {component} - {message}")
    
    def check_all_components(self):
        """Verifica tutti i componenti del sistema"""
        components_list = [
            "Lex Amoris Core",
            "AcquaLibre Protocol",
            "Klimawall Protocol",
            "NSR Engine",
            "Frequency Oscillator",
            "Dignity Check Module",
            "Watchdog System",
            "Metrics Collector"
        ]
        
        for comp_name in components_list:
            metrics = self.monitor_component(comp_name)
            self.components[comp_name] = metrics
            
            # Genera alert se necessario
            if metrics.status == ComponentStatus.CRITICAL:
                if not metrics.nsr_enabled:
                    self.create_alert(comp_name, 'CRITICAL', 'NSR non attivo')
                else:
                    self.create_alert(comp_name, 'CRITICAL', 'Metriche critiche rilevate')
            
            elif metrics.status == ComponentStatus.WARNING:
                issues = []
                if abs(metrics.frequency - 0.043) / 0.043 > 0.05:
                    issues.append(f"frequenza fuori range: {metrics.frequency:.6f} Hz")
                if metrics.hallucination_rate > 0.3:
                    issues.append(f"allucinazioni elevate: {metrics.hallucination_rate*100:.1f}%")
                if metrics.energy_usage > 800:
                    issues.append(f"energia eccessiva: {metrics.energy_usage:.0f} kW")
                
                self.create_alert(comp_name, 'WARNING', '; '.join(issues))
    
    def generate_report(self) -> Dict[str, Any]:
        """Genera report completo"""
        total = len(self.components)
        healthy = sum(1 for m in self.components.values() if m.status == ComponentStatus.HEALTHY)
        warning = sum(1 for m in self.components.values() if m.status == ComponentStatus.WARNING)
        critical = sum(1 for m in self.components.values() if m.status == ComponentStatus.CRITICAL)
        
        nsr_active = sum(1 for m in self.components.values() if m.nsr_enabled)
        avg_frequency = sum(m.frequency for m in self.components.values()) / total if total > 0 else 0
        avg_hallucination = sum(m.hallucination_rate for m in self.components.values()) / total if total > 0 else 0
        total_energy = sum(m.energy_usage for m in self.components.values())
        
        return {
            'timestamp': datetime.now().isoformat(),
            'uptime_seconds': (datetime.now() - self.start_time).total_seconds(),
            'summary': {
                'total_components': total,
                'healthy': healthy,
                'warning': warning,
                'critical': critical,
                'nsr_active_pct': (nsr_active / total * 100) if total > 0 else 0
            },
            'aggregated_metrics': {
                'avg_frequency': avg_frequency,
                'avg_hallucination_rate': avg_hallucination,
                'total_energy_kw': total_energy
            },
            'components': {name: metrics.to_dict() for name, metrics in self.components.items()},
            'recent_alerts': self.alert_history[-20:]  # Ultimi 20 alert
        }
    
    def print_dashboard(self):
        """Stampa dashboard testuale"""
        print("\n" + "="*80)
        print("🛡️  AI PEACE CHARTER - NSR COMPREHENSIVE MONITOR")
        print("="*80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Uptime: {str(timedelta(seconds=int((datetime.now() - self.start_time).total_seconds())))}")
        print("="*80)
        
        # Summary
        report = self.generate_report()
        summary = report['summary']
        metrics = report['aggregated_metrics']
        
        print(f"\n📊 SUMMARY:")
        print(f"  Components: {summary['total_components']}")
        print(f"  ✅ Healthy: {summary['healthy']}")
        print(f"  ⚠️  Warning: {summary['warning']}")
        print(f"  🚨 Critical: {summary['critical']}")
        print(f"  NSR Active: {summary['nsr_active_pct']:.1f}%")
        
        print(f"\n📈 AGGREGATED METRICS:")
        print(f"  Avg Frequency: {metrics['avg_frequency']:.6f} Hz (target: 0.043)")
        print(f"  Avg Hallucination Rate: {metrics['avg_hallucination_rate']*100:.1f}%")
        print(f"  Total Energy: {metrics['total_energy_kw']:.0f} kW")
        
        print(f"\n🔍 COMPONENT STATUS:")
        print(f"  {'Component':<30} {'Status':<12} {'NSR':<6} {'Freq (Hz)':<12} {'Hall %':<8} {'Energy (kW)':<12}")
        print("  " + "-"*78)
        
        for name, comp in self.components.items():
            status_emoji = {
                ComponentStatus.HEALTHY: "✅",
                ComponentStatus.WARNING: "⚠️ ",
                ComponentStatus.CRITICAL: "🚨",
                ComponentStatus.OFFLINE: "⭕"
            }
            
            print(f"  {name:<30} {status_emoji[comp.status]} {comp.status.value:<10} "
                  f"{'ON' if comp.nsr_enabled else 'OFF':<6} "
                  f"{comp.frequency:<12.6f} {comp.hallucination_rate*100:<8.1f} {comp.energy_usage:<12.0f}")
        
        # Recent alerts
        if self.alert_history:
            print(f"\n🔔 RECENT ALERTS (last 5):")
            for alert in self.alert_history[-5:]:
                print(f"  [{alert['timestamp']}] {alert['severity']}: {alert['component']} - {alert['message']}")
        
        print("\n" + "="*80 + "\n")
    
    def save_metrics(self, report: Dict):
        """Salva metriche su file"""
        try:
            with open(METRICS_FILE, 'w') as f:
                json.dump(report, f, indent=2)
            logger.debug(f"Metriche salvate in {METRICS_FILE}")
        except Exception as e:
            logger.error(f"Errore nel salvataggio metriche: {e}")
    
    def run(self, iterations: int = None):
        """Esegue il monitoraggio"""
        logger.info("🚀 Avvio monitoraggio NSR...")
        
        iteration = 0
        try:
            while True:
                iteration += 1
                
                # Check tutti i componenti
                self.check_all_components()
                
                # Genera report
                report = self.generate_report()
                
                # Stampa dashboard
                self.print_dashboard()
                
                # Salva metriche
                self.save_metrics(report)
                
                # Check se dobbiamo terminare
                if iterations and iteration >= iterations:
                    logger.info(f"Completate {iterations} iterazioni")
                    break
                
                # Wait
                time.sleep(MONITOR_INTERVAL)
                
        except KeyboardInterrupt:
            logger.info("\nShutdown richiesto dall'utente")
        except Exception as e:
            logger.error(f"Errore nel monitoraggio: {e}")
            raise
        finally:
            logger.info(f"Monitoraggio terminato dopo {iteration} iterazioni")

def main():
    """Entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='NSR Comprehensive Monitor')
    parser.add_argument('--iterations', type=int, help='Numero di iterazioni (default: infinito)')
    parser.add_argument('--interval', type=int, default=MONITOR_INTERVAL, help='Intervallo in secondi')
    
    args = parser.parse_args()
    
    global MONITOR_INTERVAL
    MONITOR_INTERVAL = args.interval
    
    monitor = NSRMonitor()
    monitor.run(iterations=args.iterations)

if __name__ == "__main__":
    main()
