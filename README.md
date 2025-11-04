# 🏦 Application Bancaire — Projet Docker / FastAPI / PostgreSQL / Nginx

## 📘 Présentation

Ce projet illustre la mise en place d’une **application bancaire conteneurisée** à l’aide de **Docker** et **Docker Compose**.
Il a été réalisé dans le cadre du cours sur les technologies de virtualisation et d’orchestration.

L’application comporte trois services principaux :
- **API (FastAPI)** — expose les fonctionnalités bancaires (création, dépôt, retrait, suppression de comptes) ;
- **Base de données (PostgreSQL)** — assure la persistance des données ;
- **Serveur web (nginx)** — héberge la page d’accueil et sert de reverse proxy vers l’API.

L’objectif du projet est de démontrer la **portabilité**, la **reproductibilité** et la **modularité** offertes par la conteneurisation.

## ⚙️ Structure du projet

```
banque-docker/
├── api/
│   ├── app.py
│   ├── db.py
│   ├── models.py
│   ├── requirements.txt
│   └── Dockerfile
├── nginx/
│   ├── default.conf
│   ├── index.html
│   └── Dockerfile
├── docker-compose.yml
├── .env
└── README.md

```

## 🚀 Lancer le projet localement

### 1️⃣ Prérequis

Assurez-vous d’avoir installé :
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

### 2️⃣ Cloner le projet

```bash
git clone https://github.com/suitqb/banque-docker.git
cd banque-docker
````

### 3️⃣ Configurer les variables d’environnement

Créez un fichier `.env` à la racine du projet :

```bash
POSTGRES_USER=banque
POSTGRES_PASSWORD=banque
POSTGRES_DB=banque
DOCKERHUB_USERNAME=id_docker
```

---

## 🏗️ Construction et exécution

### Étape 1 — Construire les images

```bash
docker compose build
```

### Étape 2 — Démarrer les conteneurs

```bash
docker compose up -d
```

### Étape 3 — Vérifier l’état des services

```bash
docker compose ps
```

---

## 🌐 Accès à l’application

| Service                | URL                                                                    | Description                     |
| ---------------------- | ---------------------------------------------------------------------- | ------------------------------- |
| **Frontend (nginx)**   | [http://localhost:8080](http://localhost:8080)                         | Page d’accueil de l’application |
| **API Docs (Swagger)** | [http://localhost:8080/api/docs](http://localhost:8080/api/docs)       | Documentation interactive       |
| **API JSON brut**      | [http://localhost:8080/api/comptes](http://localhost:8080/api/comptes) | Endpoint de gestion des comptes |

---

## 🔧 Tests rapides (via cURL)

Créer un compte :

```bash
curl -X POST http://localhost:8080/api/comptes \
     -H "Content-Type: application/json" \
     -d '{"nom":"Alice","solde_initial":100.00}'
```

Consulter le compte :

```bash
curl http://localhost:8080/api/comptes/1
```

Déposer de l’argent :

```bash
curl -X POST http://localhost:8080/api/comptes/1/depot \
     -H "Content-Type: application/json" \
     -d '{"montant":50.00}'
```

Retirer de l’argent :

```bash
curl -X POST http://localhost:8080/api/comptes/1/retrait \
     -H "Content-Type: application/json" \
     -d '{"montant":20.00}'
```

Supprimer un compte :

```bash
curl -X DELETE http://localhost:8080/api/comptes/1
```

---

## 🗃️ Vérifier la base de données PostgreSQL

Connexion au conteneur :

```bash
docker exec -it banque-db psql -U banque -d banque
```

Lister les comptes :

```sql
SELECT * FROM comptes;
```

---

## ☁️ Publication sur Docker Hub

1️⃣ Se connecter à Docker Hub :

```bash
docker login
```

2️⃣ Pousser les images :

```bash
docker compose push
```

3️⃣ Vérifier les images publiées :

* [`suit0/banque-api:1.0.0`](https://hub.docker.com/)
* [`suit0/banque-web:1.0.0`](https://hub.docker.com/)

---

## 💻 Exécution sur une autre machine

Télécharger et lancer directement depuis Docker Hub :

```bash
docker compose pull
docker compose up -d
```

L’application sera disponible à :
👉 [http://localhost:8080](http://localhost:8080)

---

## 📚 Documentation technique

### Endpoints principaux

| Méthode  | Endpoint                    | Description         |
| -------- | --------------------------- | ------------------- |
| `POST`   | `/api/comptes`              | Créer un compte     |
| `GET`    | `/api/comptes/{id}`         | Consulter un compte |
| `POST`   | `/api/comptes/{id}/depot`   | Dépôt d’argent      |
| `POST`   | `/api/comptes/{id}/retrait` | Retrait d’argent    |
| `DELETE` | `/api/comptes/{id}`         | Supprimer un compte |

### Volumes et réseau

* Volume persistant : `db_data` pour PostgreSQL
* Réseau interne généré automatiquement par Compose : `banque-docker_default`

---

## 🧠 Points techniques importants

* **Isolation** : chaque service tourne dans son propre conteneur.
* **Séparation des rôles** : base, API, serveur web clairement délimités.
* **Reproductibilité** : même environnement sur toute machine.
* **Portabilité** : images poussées sur Docker Hub, exécution simple via `compose pull`.
* **Sécurité** : services indépendants, ports exposés minimaux.

## 🧩 Conclusion

Ce projet démontre la mise en œuvre complète d’une architecture **multi-conteneurs** reposant sur Docker et Docker Compose.
L’approche utilisée garantit :

* la portabilité entre environnements,
* la reproductibilité du déploiement,
* et la simplicité de maintenance.

Grâce à Docker, l’application bancaire peut être exécutée sur n’importe quel poste ou serveur sans modification du code source.

---

© 2025 — Projet universitaire réalisé par Balezeau Quentin
