
### Updated Project Structure
```
simple-python-app/
├── app.py
├── requirements.txt
├── Dockerfile
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
└── .github/workflows/deploy.yml
```

https://github.com/jonathanbaraldi/simple-python-app


## Setup Instructions (Step-by-Step, Updated for K8s)

1. **Prepare Your Kubeconfig**:
   - In Rancher: Go to your cluster → **Kubeconfig File** → Download or copy the contents.
   - This file authenticates GitHub Actions to your cluster. Ensure it has permissions for `default` namespace (or update manifests for your namespace).
   - **Security Tip:** Use a service account with minimal RBAC (e.g., edit/deploy in `default` ns). Avoid cluster-admin.

2. **Create/Update GitHub Repo**:
   - Use your existing repo or create a new one (e.g., `simple-python-app`).
   - Add all files above (app.py, requirements.txt,- Added Kubernetes manifests (`k8s/deployment.yaml`, `k8s/service.yaml`, and `k8s/ingress.yaml`) for a basic Deployment + Service + Ingress.yml).
   - In `k8s/deployment.yaml`, replace `<YOUR_DOCKERHUB_USERNAME>` with your Docker Hub username.

3. **Add Secrets in GitHub**:
   - Go to **Settings > Secrets and variables > Actions**.
   - Add:
     - `DOCKERHUB_USERNAME` → Your Docker Hub username.
     jonathanbaraldi
     - `DOCKERHUB_TOKEN` → Docker Hub Access Token (create at [hub.docker.com/settings/security](https://hub.docker.com/settings/security)).


     - `KUBECONFIG` → **Paste the entire contents** of your kubeconfig file (as a multi-line secret). It looks like YAML with clusters, users, contexts.

4. **Push to `main`**:
   ```bash
   git add .
   git commit -m "Add Kubernetes manifests and CI/CD pipeline"
   git push origin main
   ```

5. **Monitor the Pipeline**:
   - Go to **Actions tab** in your repo.
   - Watch "Build, Push, and Deploy to Kubernetes" → It builds/pushes the image, then deploys to K8s.
   - If errors: Check logs (e.g., kubeconfig auth, image pull issues).

6. **Access Your App**:
   - After deployment: `kubectl get svc -n default` (in your local setup with kubeconfig).
   - Look for `EXTERNAL-IP` under `simple-python-app-service`. If `pending`, wait (EC2 load balancer provisioning).
   - Visit `http://<external-ip>` → See "Hello from Simple Python App!".
   - For local testing: `kubectl port-forward svc/simple-python-app-service 5000:80` then visit `http://localhost:5000`.
   - Health check: `/health` endpoint.

---

## 6. New: `k8s/ingress.yaml` – Kubernetes Ingress Manifest

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: simple-python-app-ingress
  namespace: default
spec:
  rules:
  - host: python.rancher.devopsforlife.io
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: simple-python-app-service
            port:
              number: 80
```

**Note:** This exposes the service at `python.rancher.devopsforlife.io`. Ensure your DNS points to your cluster's Ingress Controller.

---

## Potential Gotchas & Tips
- **Image Pull Policy:** Defaults to `IfNotPresent`; for always-latest, add `imagePullPolicy: Always` to the container spec in deployment.yaml.
- **Namespace:** All manifests use `default`. Create/change with `kubectl create ns myns` and update YAMLs.
- **Rancher-Specific:** Ensure your EC2 nodes can pull from Docker Hub (no firewall blocks). Rancher Desktop? Use its kubeconfig.
- **Scaling/Security:** Add Ingress for HTTPS (e.g., with cert-manager). Use GitHub Container Registry (ghcr.io) instead of Docker Hub for private images.
- **Rollback:** `kubectl rollout undo deployment/simple-python-app`.
- **Costs:** EC2 instances run your cluster—monitor AWS billing.

This gives you a fully automated pipeline: Push code → New image → Updated K8s pods. Simple, functional, and Rancher/EC2-ready!

Let me know if you need Helm charts, multi-env deploys, or ArgoCD integration. 🚀