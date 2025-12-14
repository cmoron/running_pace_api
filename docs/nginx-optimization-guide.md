# Optimisation nginx pour mypacer.fr

## Problème actuel

En production, le front-end sur `mypacer.fr` appelle l'API via `https://api.mypacer.fr`.
Bien que le front et l'API soient sur le même serveur, cela provoque :

1. **Résolution DNS** inutile pour `api.mypacer.fr`
2. **Nouvelle connexion HTTPS** au lieu de réutiliser celle de `mypacer.fr`
3. **Latence réseau** supplémentaire

## Solution optimisée

Utiliser un proxy nginx sur `mypacer.fr` pour rediriger `/api/*` vers `localhost:8000`.

### Avantages

- ✅ Pas de résolution DNS
- ✅ Réutilise la connexion HTTPS existante
- ✅ Communication locale (127.0.0.1) ultra-rapide
- ✅ Évite les problèmes CORS
- ✅ Peut garder `api.mypacer.fr` pour les appels externes si nécessaire

### Étapes de déploiement

#### 1. Mettre à jour nginx sur le serveur

```bash
# Sur le serveur
sudo cp /etc/nginx/sites-enabled/mypacer.fr /etc/nginx/sites-enabled/mypacer.fr.backup
sudo nano /etc/nginx/sites-enabled/mypacer.fr
```

Ajouter le bloc `location /api/` comme dans `mypacer.fr.optimized`.

#### 2. Tester la configuration nginx

```bash
sudo nginx -t
```

#### 3. Recharger nginx

```bash
sudo systemctl reload nginx
```

#### 4. Builder le front avec la nouvelle config

```bash
# Dans le répertoire du projet front-end
cd <frontend>

# Le fichier .env.production est maintenant configuré avec VITE_API_URL=/api
npm run build

# Déployer le nouveau build
# (les fichiers sont déjà dans dist/ que nginx sert)
```

#### 5. Tester

Visiter `https://mypacer.fr` et vérifier dans les DevTools Network que :
- Les requêtes API sont vers `https://mypacer.fr/api/*`
- Les temps de réponse sont améliorés

### Gains de performance attendus

- **Latence DNS** : -10 à -50ms (économisé)
- **Handshake SSL** : -20 à -100ms (économisé car connexion réutilisée)
- **Latence réseau** : localhost au lieu de loopback externe

**Gain total estimé : 30-150ms par requête API**

### Rollback si nécessaire

```bash
# Restaurer l'ancienne config
sudo cp /etc/nginx/sites-enabled/mypacer.fr.backup /etc/nginx/sites-enabled/mypacer.fr
sudo systemctl reload nginx

# Rebuilder le front avec l'ancienne variable
cd <frontend>
VITE_API_URL=https://api.mypacer.fr npm run build
```

## Note sur api.mypacer.fr

Vous pouvez **garder** la config `api.mypacer.fr` pour :
- Des appels API externes (si besoin)
- Des tests
- Une API publique documentée

Elle ne gêne pas l'optimisation interne.
