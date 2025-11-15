#!/usr/bin/env python3

import sys
import os
import subprocess
import json
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

def get_staged_diff():
    """Obtiene el diff de los cambios staged."""
    try:
        diff_command = ["git", "diff", "--staged", "--binary", "--no-color"]
        result = subprocess.run(diff_command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener el diff: {e}", file=sys.stderr)
        return None

def build_gemini_prompt(staged_diff, conventional_commits_guide):
    """Construye el prompt para Gemini."""
    if not staged_diff:
        return "Genera un mensaje de commit vacío o un placeholder."

    prompt = f"""
Eres un experto en Git y en la convención Conventional Commits. Tu tarea es generar un mensaje de commit conciso y descriptivo basado en los cambios proporcionados.

Sigue estrictamente la siguiente guía de Conventional Commits:

{conventional_commits_guide}

---

Basándote en los siguientes cambios en el código (diff), genera un mensaje de commit que cumpla con la guía anterior.
Asegúrate de que el mensaje sea relevante para los cambios y que el tipo y el ámbito sean apropiados.
Si los cambios son muy pequeños o no claros, puedes sugerir un tipo 'chore' o 'refactor'.
Si no hay cambios significativos, puedes generar un mensaje de commit vacío o un placeholder.

Cambios en el código (diff):
```diff
{staged_diff}
```

Mensaje de commit (solo el texto del mensaje, sin encabezados ni explicaciones adicionales):
"""
    return prompt

def call_gemini_api(prompt):
    """Llama a la API de Gemini para generar el mensaje de commit."""
    if not GEMINI_API_KEY:
        print("Error: La clave API de Gemini no está configurada (GEMINI_API_KEY).", file=sys.stderr)
        return None

    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    try:
        response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al llamar a la API de Gemini: {e}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"Error al parsear la respuesta JSON de Gemini: {e}", file=sys.stderr)
        print(f"Respuesta cruda: {response.text if 'response' in locals() else 'N/A'}", file=sys.stderr)
        return None
    except requests.exceptions.Timeout as e:
        print(f"Error: La llamada a la API de Gemini excedió el tiempo de espera: {e}", file=sys.stderr)
        return None


def main():
    if len(sys.argv) < 2:
        print("Uso: prepare-commit-msg <COMMIT_EDITMSG_FILE>", file=sys.stderr)
        sys.exit(1)

    commit_editmsg_file = sys.argv[1]

    # Leer la guía de Conventional Commits desde el directorio de instalación global
    global_install_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "gemini-commit-hook")
    prompt_guide_path = os.path.join(global_install_dir, "prompt_guide.md")

    try:
        with open(prompt_guide_path, 'r', encoding='utf-8') as f:
            conventional_commits_guide = f.read()
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo de la guía de Conventional Commits en '{prompt_guide_path}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error al leer la guía de Conventional Commits: {e}", file=sys.stderr)
        sys.exit(1)

    staged_diff = get_staged_diff()
    if staged_diff is None:
        sys.exit(1)

    if not staged_diff.strip():
        print("No hay cambios staged. No se generará un mensaje de commit.", file=sys.stderr)
        sys.exit(0)

    prompt = build_gemini_prompt(staged_diff, conventional_commits_guide)
    gemini_response_json = call_gemini_api(prompt)

    if gemini_response_json:
        try:
            # La respuesta de Gemini se espera en 'candidates[0].content.parts[0].text'
            generated_message = gemini_response_json['candidates'][0]['content']['parts'][0]['text']
            
            # Eliminar posibles bloques de código markdown si Gemini los incluye
            if generated_message.startswith("```") and generated_message.endswith("```"):
                generated_message = generated_message.strip("`").strip()
            
            with open(commit_editmsg_file, 'w') as f:
                f.write(generated_message.strip())
            print("Mensaje de commit generado por Gemini y pre-rellenado.", file=sys.stderr)
        except (KeyError, IndexError) as e:
            print(f"Error al parsear la respuesta de Gemini: {e}", file=sys.stderr)
            print("Respuesta completa de Gemini:", gemini_response_json, file=sys.stderr)
    else:
        print("No se pudo obtener un mensaje de commit de Gemini.", file=sys.stderr)

if __name__ == "__main__":
    main()
