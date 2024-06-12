#!/bin/bash

# Charger les variables d'environnement
source "../.env"

# Définir les variables
DB_CONTAINER_NAME="${POSTGRES_CONTAINER}"
DB_NAME="${POSTGRES_DB}"
DB_USER="${POSTGRES_USER}"
DB_PASSWORD="${POSTGRES_PASSWORD}"
BACKUP_DIR="."
TIMESTAMP="$(date +"%Y%m%d%H%M%S")"
BACKUP_PATH="${BACKUP_DIR}/backup_${DB_NAME}_${TIMESTAMP}.sql"

# Créer le répertoire de sauvegarde s'il n'existe pas
mkdir -p "${BACKUP_DIR}"

# Exporter le mot de passe pour pg_dump
export PGPASSWORD="${DB_PASSWORD}"

# Exécuter pg_dump depuis le conteneur Docker
docker exec "${DB_CONTAINER_NAME}" pg_dump -U "${DB_USER}" "${DB_NAME}" > "${BACKUP_PATH}"

# Vérifier si la sauvegarde a réussi
if [ $? -eq 0 ]; then
    echo "Sauvegarde réussie : ${BACKUP_PATH}"
else
    echo "Échec de la sauvegarde"
fi

# Désactiver la variable d'environnement du mot de passe
unset PGPASSWORD

# Supprimer les sauvegardes les plus anciennes si plus de 5 sauvegardes existent
BACKUP_COUNT=$(ls ${BACKUP_DIR}/backup_${DB_NAME}_*.sql | wc -l)
if [ ${BACKUP_COUNT} -gt 5 ]; then
    OLDEST_BACKUP=$(ls ${BACKUP_DIR}/backup_${DB_NAME}_*.sql | head -n 1)
    rm ${OLDEST_BACKUP}
    echo "Suppression de la sauvegarde la plus ancienne : ${OLDEST_BACKUP}"
fi
