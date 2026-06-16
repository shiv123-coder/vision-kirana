# VisionKirana

![VisionKirana Banner](https://via.placeholder.com/1200x300.png?text=VisionKirana+-+AI-Powered+Micro-Lending+for+Kirana+Stores)

[![Build Status](https://img.shields.io/github/actions/workflow/status/your-org/vision-kirana/ci.yml?branch=main)](https://github.com/your-org/vision-kirana/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/)
[![Vite / React](https://img.shields.io/badge/Vite-React%2019-purple.svg)](https://vitejs.dev/)

VisionKirana is an enterprise-grade fintech platform designed to democratize access to micro-lending for Kirana store owners across India. By utilizing cutting-edge AI and Machine Learning, VisionKirana bypasses traditional credit scores, assessing loan eligibility purely through Computer Vision, OCR, Voice Intelligence, and Location Proxies.

## 🚀 Features

- **PWA & Offline-First**: Installable frontend that gracefully handles spotty network connections. Queue form submissions completely offline.
- **Computer Vision Pipeline**: Evaluates uploaded store images to determine Shelf Density and Brand Diversity, instantly proxying the health of physical inventory.
- **OCR Validation Engine**: Extracts textual data from physical invoices, intelligently mapping Supplier names and Amount consistencies.
- **Voice Intelligence**: NLP-powered extraction of Business Summaries, Loan Purposes, and Sentiment Analysis directly from merchant voice recordings.
- **Location Intelligence**: Mocked geographic data engine to calculate Competition Density, Footfall Proxies, and Market Area favorability.
- **Automated Risk Engine**: Consolidates all AI models into a single 0-100 Business Health Score, classifying loans from "Low Risk" to "Very High Risk".

## 🛠 Tech Stack

- **Frontend**: React 19, TypeScript, Vite, TailwindCSS, Recharts, Vite-PWA
- **Backend**: FastAPI (Python 3.12), SQLAlchemy, PostgreSQL
- **AI/ML**: EasyOCR, OpenCV, PyMuPDF, Scikit-Image
- **DevOps**: Docker, Docker Compose, GitHub Actions

## 📖 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-org/vision-kirana.git
cd vision-kirana

# 2. Boot up the entire stack using Docker Compose
docker-compose up --build
```
- **Frontend App**: `http://localhost:5173`
- **Backend API**: `http://localhost:8000`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`

## 🔒 Security & Roles

VisionKirana ships with robust JWT authentication and Role-Based Access Control (RBAC).
- `admin`: Full platform overview, risk distribution access.
- `loan_officer`: Access to application queues, risk reports, and approval matrices.
- `shop_owner`: Access to personal shop profiles, document uploading, and health trends.

## 📚 Documentation
- [Deployment Guide](./DEPLOYMENT.md)
- [Testing Strategy](./TESTING.md)

---
*Built to empower the unbanked.*
