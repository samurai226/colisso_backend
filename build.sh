#!/usr/bin/env bash
set -o errexit

echo "🔧 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️  Running migrations..."
python manage.py migrate --no-input

echo "👤 Creating superuser..."
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()

# Vérifier quel est le USERNAME_FIELD
username_field = User.USERNAME_FIELD
print(f'USERNAME_FIELD is: {username_field}')

# Créer le superuser avec le bon champ
if username_field == 'telephone':
    # Utiliser telephone
    if not User.objects.filter(telephone='0000000000').exists():
        User.objects.create_superuser(
            telephone='0000000000',
            nom='Admin',
            prenom='Colisso',
            password='AdminColisso2024!'
        )
        print('✅ Superuser created with telephone!')
    else:
        print('ℹ️  Superuser already exists')
else:
    # Fallback pour username classique
    if not User.objects.filter(**{username_field: 'admin'}).exists():
        User.objects.create_superuser(
            **{username_field: 'admin'},
            password='AdminColisso2024!'
        )
        print('✅ Superuser created!')
    else:
        print('ℹ️  Superuser already exists')
EOF

echo "✅ Build completed!"
```

---

## 📋 CREDENTIALS DU SUPERUSER

**Après le déploiement** :
```
Telephone: 0000000000
Password: AdminColisso2024!