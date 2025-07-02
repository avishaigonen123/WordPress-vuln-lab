# 🧪 WordPress Vulnerability Lab (Docker-based)

A clean, Docker-based WordPress lab designed for testing vulnerable plugins, switching WordPress versions, and running WP-CLI with ease.

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/avishaigonen123/WordPress-vuln-lab.git
cd WordPress-vuln-lab
```

### 2. Start the Lab Environment

```bash
docker-compose up -d
```

🔗 Your local WordPress site will be available at: [http://localhost:8080](http://localhost:8080)

### 3. Complete WordPress Setup

Go to the browser and complete the WordPress installation wizard (choose language, username, password, etc.).

---

## ⚙️ WordPress Version Control

To change WordPress version:

1. Edit `Dockerfile`:

```dockerfile
FROM wordpress:6.4-php8.2  # or any version you want
```

2. Then rebuild:

```bash
docker-compose down -v
docker-compose up -d --build
```

---

## 🧩 Installing Vulnerable Plugins (.zip)

You can download plugins from:  
📎 https://plugins.svn.wordpress.org/


For example:  
📎 https://plugins.svn.wordpress.org/wp-file-manager/tags/6.0/

In addition, you can install from here:
📎 https://downloads.wordpress.org/plugin/wp-file-manager.6.0.zip

Put your plugin `.zip` files in the `./plugins` folder.

Then install them via:

```bash
./scripts/install.sh ./plugins/PLUGIN_NAME.zip
```

This script will:
- Upload the plugin into the Docker container
- Install and activate it via WP-CLI
- Automatically add `--allow-root` (as WP-CLI is run as root in Docker)

---

## ❌ Removing Plugins

To uninstall a plugin and optionally delete the original `.zip` file from `./plugins`:

```bash
./scripts/remove.sh "plugin-slug"
```

✅ Example:
```bash
./scripts/remove.sh duplicator
```

The script will:
- Deactivate and uninstall the plugin via WP-CLI
- Search for a matching ZIP file in `./plugins/` and ask if you'd like to delete it

---

## 🧰 WP-CLI Access

The container includes **WP-CLI** (command-line interface for WordPress).  
Useful commands:

```bash
docker exec -it my_wordpress wp plugin list --allow-root
docker exec -it my_wordpress wp core version --allow-root
```

> Note: `--allow-root` is required because Docker runs as root inside the container.

---

## 🧼 Cleanup

Shut down the environment:

```bash
docker-compose down
```

Shut down and remove everything including database volumes:

```bash
docker-compose down -v
```

---

## 🛠️ Tools Folder

The [Tools](./tools) folder is packed with utilities and scripts designed to assist in testing WordPress vulnerabilities. As the project grows, more powerful and advanced tools will be added to enhance your security testing experience.

### Current Tools:

- **WPForce Brute-Force Wrapper**  
  A tool designed to brute-force login attempts on WordPress sites using a list of usernames and passwords.
  - **Location:** [WordPress Brute-force script](./tools/WordPress-Brute-force-Script/README.md)
  - **Description:** This tool helps to perform brute-force attacks against WordPress login pages, testing the strength of user credentials.

- **Plugin Vulnerability Tester** (Coming Soon) :)  
  A tool to check the vulnerabilities of installed plugins in your WordPress environment (currently in development).
  
---

**Stay tuned for more!** 🎉  
As we continue to improve and extend this lab, more tools for WordPress security testing will be available to you. Keep an eye on the `tools` folder! 🔧💡

---

## 🙏 Credits

Based on [vavkamil/dvwp](https://github.com/vavkamil/dvwp)  
Customized and improved by [Avishai Gonen](https://avishaigonen123.github.io/)

---

## 📜 License

MIT License – Use freely, modify as needed.