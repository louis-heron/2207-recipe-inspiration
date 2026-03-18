# Déploiement de l'API sur Google Cloud Run

## Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installé et lancé
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (`gcloud`) installé et authentifié
- Être connecté au bon compte GCP :
  ```bash
  gcloud auth login
  gcloud config set project modular-hulling-489209-r6
  ```
- Docker configuré pour pousser vers l'Artifact Registry :
  ```bash
  gcloud auth configure-docker europe-west1-docker.pkg.dev
  ```

---

## Informations du projet

| Paramètre         | Valeur                                      |
|-------------------|---------------------------------------------|
| Projet GCP        | `modular-hulling-489209-r6`                 |
| Région            | `europe-west1`                              |
| Service Cloud Run | `recipe-inspiration-api`                    |
| Artifact Registry | `recipe-inspiration`                        |
| Image             | `europe-west1-docker.pkg.dev/modular-hulling-489209-r6/recipe-inspiration/recipe-inspiration-api` |
| URL de l'API      | https://recipe-inspiration-api-606532030834.europe-west1.run.app |

---

## Étapes de déploiement

### 1. Build de l'image Docker

> **Important :** Toujours builder avec `--platform linux/amd64`.
> Sur Mac Apple Silicon (M1/M2/M3), Docker produit par défaut une image `arm64` incompatible avec Cloud Run.

```bash
docker build --platform linux/amd64 \
  -t europe-west1-docker.pkg.dev/modular-hulling-489209-r6/recipe-inspiration/recipe-inspiration-api \
  .
```

### 2. Vérification locale avant de pousser

Lancer le container localement pour s'assurer qu'il démarre correctement :

```bash
docker run --rm -d -p 8080:8080 --platform linux/amd64 --name recipe-test \
  europe-west1-docker.pkg.dev/modular-hulling-489209-r6/recipe-inspiration/recipe-inspiration-api
```

Attendre ~30 secondes (chargement des modèles YOLO + pickles), puis tester :

```bash
curl http://localhost:8080/
# Réponse attendue : {"greeting":"Recipe Recommander API v1.0","status":"healthy",...}
```

Arrêter le container de test :

```bash
docker stop recipe-test
```

### 3. Push de l'image vers l'Artifact Registry

```bash
docker push europe-west1-docker.pkg.dev/modular-hulling-489209-r6/recipe-inspiration/recipe-inspiration-api
```

> Le push peut prendre plusieurs minutes — l'image fait ~1.2 Go.
> Les layers déjà présents dans le registre sont réutilisés, les pushes suivants seront plus rapides.

### 4. Déploiement sur Cloud Run

```bash
gcloud run deploy recipe-inspiration-api \
  --image europe-west1-docker.pkg.dev/modular-hulling-489209-r6/recipe-inspiration/recipe-inspiration-api \
  --region europe-west1 \
  --project modular-hulling-489209-r6 \
  --platform managed \
  --allow-unauthenticated
```

Le déploiement prend quelques minutes (Cloud Run doit pull l'image et démarrer le container).

---

## Erreurs connues et solutions

### `exec format error`
**Cause :** L'image a été buildée en `arm64` (Mac Apple Silicon) au lieu de `linux/amd64`.
**Solution :** Toujours utiliser `--platform linux/amd64` dans la commande `docker build`.

### `libxcb.so.1: cannot open shared object file`
**Cause :** Librairies système X11 manquantes dans l'image slim, requises par OpenCV (ultralytics).
**Solution :** Le `Dockerfile` installe déjà `libxcb1`, `libgl1-mesa-glx` et `libglib2.0-0`. Si ce problème réapparaît, vérifier que ces lignes sont bien présentes dans le Dockerfile.

### `Form data requires "python-multipart" to be installed`
**Cause :** `python-multipart` absent de `requirements.txt`, nécessaire pour l'upload de fichiers avec FastAPI.
**Solution :** `python-multipart` est déjà dans `requirements.txt`. Si retiré par erreur, le rajouter.

### `No space left on device` (pendant le build)
**Cause :** Docker Desktop manque d'espace disque (images et caches accumulés).
**Solution :**
```bash
docker system prune -f
```

---

## Fichiers importants

| Fichier               | Rôle                                              |
|-----------------------|---------------------------------------------------|
| `Dockerfile`          | Définition de l'image                             |
| `requirements.txt`    | Dépendances Python                                |
| `api/main.py`         | Point d'entrée FastAPI                            |
| `api/Model/model.pkl` | Modèle de recommandation (chargé au démarrage)    |
| `api/Model/vectorizer.pkl` | Vectorizer TF-IDF (chargé au démarrage)      |
| `api/Vision/best.pt`  | Modèle YOLO pour la détection d'ingrédients       |

> `ingredients.parquet` n'est **pas** nécessaire au runtime — il est uniquement utilisé lors de l'entraînement (`api/Model/train.py`).
