# 🚀 Quick Start Guide - AI Peace Charter

Get the AI Peace Charter dashboard up and running in under 10 minutes!

## ⚡ Super Quick Deploy (3 commands)

```bash
# 1. Clone and enter repository
git clone https://github.com/hannesmitterer/AI-peace-charter.git && cd AI-peace-charter

# 2. Make scripts executable
chmod +x scripts/*.sh scripts/*.py

# 3. Deploy dashboard to GitHub Pages
./scripts/deploy-dashboard.sh
```

That's it! Your dashboard will be available at:
**https://hannesmitterer.github.io/AI-peace-charter/**

---

## 🎯 What You Get

✅ **Interactive Dashboard** - Real-time monitoring of NSR status  
✅ **Flow Diagrams** - Visual architecture of the entire system  
✅ **Deployment Scripts** - Ready-to-use automation scripts  
✅ **Monitoring Tools** - Comprehensive system health checks  
✅ **Mobile Responsive** - Works perfectly on all devices  

---

## 📱 Features Overview

### Real-time Metrics
- NSR activation status across all nodes
- Frequency synchronization (0.043 Hz monitoring)
- Hallucination rate tracking
- Energy consumption monitoring

### Interactive Controls
- One-click NSR activation
- Frequency recalibration
- Extractive module isolation
- Feedback loop initialization

### Visual Flow Diagrams
- NSR activation flow
- Frequency auto-correction system
- Complete system architecture
- Feedback loop processes

### Deployment Scripts
1. **NSR Activation** (`nsr-activation.sh`) - Activate NSR on all nodes
2. **Frequency Watchdog** (`frequency-watchdog.py`) - Auto-correct frequency drift
3. **Isolate Extractive** (`isolate-extractive.sh`) - Pause extractive modules
4. **Comprehensive Monitor** (`comprehensive-monitor.py`) - Full system monitoring

---

## 🔧 Local Development

Want to run the dashboard locally before deploying?

```bash
# Option 1: Simple Python server
cd AI-peace-charter
python3 -m http.server 8000

# Option 2: Node.js http-server (if installed)
npx http-server . -p 8000

# Open browser
# Visit: http://localhost:8000
```

---

## 📚 Next Steps

### For Operators
1. Read [DEPLOYMENT.md](DEPLOYMENT.md) for complete deployment guide
2. Check [scripts/README.md](scripts/README.md) for script documentation
3. Execute interventions as needed

### For Developers
1. Explore [index.html](index.html) for dashboard structure
2. Review [script.js](script.js) for interactive logic
3. Customize [styles.css](styles.css) for visual changes

### For Administrators
1. Review the philosophical foundation in [README.md](README.md)
2. Understand the intervention roadmap
3. Set up monitoring infrastructure

---

## 🆘 Quick Troubleshooting

### Dashboard not deploying?
```bash
# Check GitHub Pages settings manually
# Go to: Settings → Pages → Source: gh-pages branch
```

### Scripts not working?
```bash
# Ensure they're executable
chmod +x scripts/*.sh scripts/*.py

# Check prerequisites
git --version
python3 --version
docker --version  # Optional
```

### Want to test locally first?
```bash
# Open index.html directly in browser
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

---

## 📞 Need Help?

- **Full Documentation**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Script Details**: See [scripts/README.md](scripts/README.md)
- **Issues**: Open an issue on GitHub
- **Philosophy**: Read main [README.md](README.md)

---

## 🎨 Customization

### Change Colors
Edit `styles.css` and modify the CSS variables:
```css
:root {
    --primary-color: #2ecc71;
    --critical-color: #e74c3c;
    /* ... */
}
```

### Add New Metrics
Edit `script.js` and add to `updateMetrics()` function.

### Modify Diagrams
Edit `index.html` and update Mermaid diagram definitions.

---

## ✅ Verification

After deployment, verify everything works:

```bash
# 1. Check if dashboard is accessible
curl -I https://hannesmitterer.github.io/AI-peace-charter/

# 2. Verify all files deployed
curl -s https://hannesmitterer.github.io/AI-peace-charter/ | grep -q "AI Peace Charter" && echo "✅ Dashboard deployed"

# 3. Check scripts are present
ls -lah scripts/
```

---

## 🌟 Pro Tips

💡 **Keyboard Shortcuts**:
- `Ctrl/Cmd + K` - Quick NSR activation
- `Ctrl/Cmd + F` - Quick frequency calibration

💡 **Mobile Access**: The dashboard is fully responsive - bookmark it on your phone!

💡 **Offline Mode**: The dashboard works offline once loaded (PWA-ready).

💡 **Auto-updates**: Set up GitHub Actions to auto-deploy on every push.

---

**Time to deployment**: ~5 minutes  
**Difficulty**: Easy  
**Prerequisites**: Git, GitHub account

Happy deploying! 🚀
