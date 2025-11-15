# Gemini Commit Hook

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## ¿Qué es?

**Gemini Commit Hook** es una herramienta que automatiza la generación de mensajes de commit de Git utilizando la inteligencia artificial de **Google Gemini**. Se integra como un hook `prepare-commit-msg` en tus repositorios Git, ayudándote a mantener un historial de commits limpio y consistente, siguiendo la especificación de [Conventional Commits](https://www.conventionalcommits.org/es/v1.0.0/).

## ¿Qué hace?

Cuando inicias un commit (`git commit`), este hook analiza automáticamente tus cambios staged (`git diff --staged`) y envía esta información a la API de Gemini. Gemini, actuando como un experto en Git y Conventional Commits, genera un mensaje de commit descriptivo y formateado. Este mensaje se pre-rellena en tu editor de commit, listo para que lo revises, edites y confirmes.

## Características

*   **Generación Automática de Mensajes**: Ahorra tiempo y esfuerzo al obtener sugerencias de mensajes de commit inteligentes.
*   **Adherencia a Conventional Commits**: Asegura que tus mensajes sigan un estándar, facilitando la lectura del historial y la automatización de tareas (como la generación de changelogs).
*   **Fácil Configuración**: Diseñado para una puesta en marcha sencilla y adaptable en tus proyectos Git.

## Requisitos

Para usar Gemini Commit Hook, necesitas:

1.  **Python 3.x**: Asegúrate de tener Python 3 instalado en tu sistema.
2.  **Clave API de Google Gemini**: Necesitas una clave válida para acceder a la API de Gemini. Puedes obtenerla en [Google AI Studio](https://aistudio.google.com/).
3.  **Git**: Obviamente, necesitas Git instalado para trabajar con repositorios.

## Instalación

La instalación de Gemini Commit Hook se realiza en dos pasos: primero, una instalación global en tu sistema para hacer la herramienta disponible, y luego, la activación del hook en cada repositorio Git donde desees usarla.

### 1. Instalación Global (Recomendado)

Esta opción instala los componentes principales de la herramienta en tu sistema, haciendo que el comando `install_repo_hook` esté disponible globalmente.

1.  **Clona este repositorio**:
    ```bash
    git clone https://github.com/ejsalasdev/gemini-commit-hook.git
    cd gemini-commit-hook
    ```
2.  **Ejecuta el script de instalación global**:
    ```bash
    ./install.sh
    ```
    Este script configurará un entorno Python virtual dedicado, instalará las dependencias y copiará el ejecutable `install_repo_hook` a `~/.local/bin`.

    **Nota**: Asegúrate de que `~/.local/bin` esté en la variable de entorno `PATH` de tu sistema.

### 2. Instalación por Repositorio (Activación del Hook)

Después de la instalación global, debes activar el hook en cada repositorio Git donde quieras usarlo.

Navega a la raíz de tu repositorio Git (donde está la carpeta `.git/`) y ejecuta:

```bash
install_repo_hook
```

Esto instalará el hook `prepare-commit-msg` específicamente para ese repositorio, permitiendo que Gemini genere tus mensajes de commit.

## Uso

1.  **Prepara tus cambios**: Añade los archivos que deseas incluir en tu commit:
    ```bash
    git add .
    ```
2.  **Inicia el commit**:
    ```bash
    git commit
    ```
    El hook se activará automáticamente, generará un mensaje de commit y lo pre-rellenará en tu editor. Revisa el mensaje, haz los ajustes necesarios y guarda para completar el commit.

### Configuración de la Clave API de Gemini

Es **esencial** configurar tu clave API de Gemini como una variable de entorno. Añade la siguiente línea a tu archivo de configuración de shell (por ejemplo, `~/.bashrc`, `~/.zshrc`, `~/.profile`):

```bash
export GEMINI_API_KEY="TU_CLAVE_API_AQUI"
```

Después de añadirla, recarga tu shell (`source ~/.bashrc` o similar) o abre una nueva terminal.
```
