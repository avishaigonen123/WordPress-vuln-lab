#!/bin/bash

PLUGIN_SLUG=$1

if [ -z "$PLUGIN_SLUG" ]; then
    echo "Usage: $0 <plugin-slug>"
    exit 1
fi

echo "Deactivating and uninstalling plugin: $PLUGIN_SLUG"
docker exec my_wordpress wp plugin deactivate "$PLUGIN_SLUG" --allow-root
docker exec my_wordpress wp plugin delete "$PLUGIN_SLUG" --allow-root

# Search for ZIP file in plugins folder
ZIP_FILE=$(find ./plugins -type f -iname "*$PLUGIN_SLUG*.zip")

if [ -n "$ZIP_FILE" ]; then
    echo "Found corresponding ZIP file: $ZIP_FILE"
    read -p "Do you want to delete this ZIP file? [y/N]: " CONFIRM
    if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
        rm "$ZIP_FILE"
        echo "ZIP file removed."
    else
        echo "ZIP file kept."
    fi
fi
