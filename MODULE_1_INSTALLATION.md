# 🚀 MODULE 1 : CORE - Installation

## 📦 Ce module contient :

- ✅ Django 5.0.0 configuré
- ✅ Django REST Framework
- ✅ Swagger (documentation API)
- ✅ CORS
- ✅ BaseModel (modèle de base pour tous les autres modules)
- ✅ Health check endpoint

## 📋 Dépendances (6 packages) :

1. Django==5.0.0
2. djangorestframework==3.14.0
3. django-filter==23.5
4. drf-spectacular==0.27.0
5. django-cors-headers==4.3.1
6. python-decouple==3.8

---

## 🔧 INSTALLATION PAS À PAS

### ÉTAPE 1 : Extraire le ZIP

Extrais le ZIP dans un dossier, par exemple : `C:\colisso`

### ÉTAPE 2 : Ouvrir le terminal

1. Va dans le dossier `colisso_module1`
2. Clique dans la barre d'adresse
3. Tape : `cmd`
4. Appuie sur Entrée

### ÉTAPE 3 : Créer le venv

```bash
python -m venv venv
```

### ÉTAPE 4 : Activer le venv

```bash
venv\Scripts\activate
```

Tu dois voir `(venv)` au début de la ligne.

### ÉTAPE 5 : Installer les dépendances

```bash
pip install -r requirements.txt
```

**Attends 1-2 minutes.**

Tu devrais voir :
```
Successfully installed Django-5.0.0 djangorestframework-3.14.0 ...
```

### ÉTAPE 6 : Créer .env

```bash
copy .env.example .env
```

### ÉTAPE 7 : Migrations

```bash
python manage.py migrate
```

Tu devrais voir plein de lignes avec "... OK"

### ÉTAPE 8 : Créer un superuser (optionnel)

```bash
python manage.py createsuperuser
```

Suis les instructions.

### ÉTAPE 9 : Lancer le serveur !

```bash
python manage.py runserver
```

Tu devrais voir :
```
Starting development server at http://127.0.0.1:8000/
```

---

## ✅ TESTER

### Test 1 : Swagger

Ouvre ton navigateur :
**http://localhost:8000/swagger/**

Tu devrais voir la documentation API !

### Test 2 : Health Check

Ouvre ton navigateur :
**http://localhost:8000/api/v1/health/**

Tu devrais voir :
```json
{
  "status": "ok",
  "message": "Colisso API - Module 1 is running!",
  "database": "connected",
  "module": "CORE"
}
```

### Test 3 : Admin

Ouvre ton navigateur :
**http://localhost:8000/admin/**

Connecte-toi avec ton superuser.

---

## 🎉 SUCCÈS !

Le **MODULE 1 : CORE** fonctionne !

---

## ⏭️ PROCHAINE ÉTAPE

Une fois que ce module fonctionne, tu pourras installer :

**MODULE 2 : LOCATIONS** (Pays, Villes, Gares)

---

## ⚠️ EN CAS D'ERREUR

Si une étape échoue, note :
1. Quelle étape ?
2. Quelle commande ?
3. Quel message d'erreur ?

Et demande de l'aide !

---

## 📊 Structure du projet

```
colisso_module1/
├── manage.py
├── requirements.txt
├── .env.example
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── apps/
    └── core/
        ├── __init__.py
        ├── apps.py
        ├── models.py     (BaseModel)
        ├── views.py      (HealthCheckView)
        ├── urls.py
        └── admin.py
```

---

**Bon développement !** 🚀
