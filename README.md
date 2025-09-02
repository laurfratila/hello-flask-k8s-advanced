# hello-flask-k8s-advanced

Flask app with:
- /health endpoint
- background writer to /data/counter.txt (interval via env var)
- multi-stage Dockerfile, non-root user, Docker HEALTHCHECK

Kubernetes (next steps):
- ConfigMap + Secret as env
- Readiness/Liveness probes
- Ingress
- HPA
- PVC to persist /data