#!/bin/bash
PLUGIN=$1

if [ -z "$PLUGIN" ]; then
    echo "Usage: $0 <plugin-slug-or-zip>"
    exit 1
fi

if [[ $PLUGIN == *.zip ]]; then
  docker cp "$PLUGIN" my_wordpress:/tmp/
  ZIP_NAME=$(basename "$PLUGIN")
  docker exec -it my_wordpress wp plugin install /tmp/$ZIP_NAME --activate --allow-root
else
  docker exec -it my_wordpress wp plugin install "$PLUGIN" --activate --allow-root
fi
