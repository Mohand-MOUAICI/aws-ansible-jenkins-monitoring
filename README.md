
# AWS – Ansible + Jenkins + Monitoring (Prometheus/Grafana) – Starter Kit

Ce dépôt te permet de déployer rapidement une petite app FastAPI sur AWS avec :
- **Jenkins** pour CI/CD (build & push sur **ECR**, puis déploiement via **Ansible**)
- **Monitoring** : Prometheus, Grafana, cAdvisor, Node Exporter

## Architecture
- 2 EC2 (Ubuntu 22.04) :
  - `jenkins` : Jenkins en conteneur + Ansible + Docker CLI
  - `app-monitor` : App FastAPI + Prometheus + Grafana + cAdvisor + Node Exporter
- Registry : Amazon **ECR**

## Pré-requis
- `aws` CLI configuré (compte avec droits ECR/EC2/IAM/SG)
- Clef SSH créée (`devops-key.pem`) et utilisable pour `ubuntu@...`
- Docker installé **localement** si tu veux tester le build

## Étapes rapides
1. **Créer le repo ECR** et garder son URI (ex: `ACCOUNT_ID.dkr.ecr.eu-west-3.amazonaws.com/hello-app`).
2. **Créer 2 EC2** (Security Groups + IAM role côté Jenkins). Tu peux utiliser les scripts cloud-init fournis :
   - `cloud-init/jenkins-userdata.sh`
   - `cloud-init/app-userdata.sh`
3. Récupère les **IPs publiques** et mets-les dans `ansible/inventory.ini` + dans `ci/Jenkinsfile` (env `SSH_TARGET`/`APP_PUBLIC_IP`).
4. Sur la VM `jenkins` :
   - Ouvre Jenkins (`http://IP_JENKINS:8080`), termine le setup.
   - Ajoute un job **Pipeline** pointant sur ce repo (ou copie-colle `ci/Jenkinsfile`).
5. Lance le premier **déploiement complet** (monitoring + app) :
   ```bash
   cd ansible
   ansible-playbook -i inventory.ini playbooks/site.yml -e image=ECR_URI:latest
   ```
6. **CI/CD** : à chaque `git push`, Jenkins :
   - build l'image, push vers ECR, puis déploie via Ansible `deploy-app.yml`.

## URLs utiles
- App : `http://APP_PUBLIC_IP/`
- Prometheus : `http://APP_PUBLIC_IP:9090`
- Grafana : `http://APP_PUBLIC_IP:3000` (admin / admin au premier login — change le mot de passe !)
- cAdvisor : `http://APP_PUBLIC_IP:8081`

## Sécurité minimale
- Remplace les CIDR 0.0.0.0/0 par ton IP quand possible.
- Change le mot de passe Grafana.
- Sauvegarde `/var/jenkins_home` (volume Docker Jenkins).

## Variables à remplacer
- `APP_PUBLIC_IP` : IP publique de l’instance app-monitor.
- `ECR_URI` : URI complet du repo ECR (ex: `123456789012.dkr.ecr.eu-west-3.amazonaws.com/hello-app`).

Bonne construction !
