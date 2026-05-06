# Jenkins Job Factory

`jenkins-job-factory` es una herramienta de automatización por línea de comandos (CLI) escrita en Python que permite crear de forma declarativa carpetas y trabajos del tipo "Multibranch Pipeline" en Jenkins, basándose en un archivo de configuración YAML.

## Características

- **Configuración Declarativa (YAML)**: Define la estructura de carpetas y repositorios a crear.
- **Soporte para Valores por Defecto**: Permite configurar de forma global parámetros comunes como credenciales, scripts de pipeline (`script_id`) y expresiones regulares de ramas (`branch_regex`), evitando la repetición.
- **Idempotencia Básica**: Antes de crear un folder o un job, la herramienta verifica a través de la API si ya existe.
- **Escaneo Automático**: Por defecto, dispara automáticamente el proceso de escaneo (Scan Multibranch Pipeline) inmediatamente después de crear el job. Esto se puede deshabilitar mediante la bandera `--no-scan`.
- **Plantillas XML Nativas**: Se integra directamente con la API REST de Jenkins subiendo configuraciones en XML.

## Requisitos

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) para la gestión de dependencias y ejecución.
- Acceso de red a un servidor Jenkins y un Token de API de usuario.

## Configuración del Entorno

La herramienta requiere que las credenciales de conexión a Jenkins estén disponibles a través de variables de entorno. Crea un archivo `.env` en la raíz del proyecto (puedes basarte en `.env.local` si existe):

```env
JENKINS_URL=https://tu-jenkins.com/
JENKINS_USER=tu_usuario
JENKINS_TOKEN=tu_token_api
```

## Estructura del Archivo de Configuración (`jobs.yml`)

Para comenzar, haz una copia del archivo de ejemplo y adáptalo a tus necesidades:
```bash
cp jobs.yml.example jobs.yml
```

El archivo YAML principal (por defecto `jobs.yml`) define la topología de lo que se creará en Jenkins.

```yaml
# Carpeta raíz donde se crearán todas las subcarpetas y jobs
root_folder: root_folder

# (Opcional) Valores por defecto a aplicar a todos los jobs
defaults:
  credentials_id: credentials_id
  script_id: golden_pipe
  branch_regex: "^(?:dev|qa|main|master)$"

# Lista de carpetas secundarias
folders:
  - name: unidad_negocio
    jobs:
      - name: mi_microservicio
        repo_url: https://git.midominio.com/unidad_negocio/mi_microservicio
        # branch_regex, credentials_id y script_id se heredarán de "defaults"

      - name: otro_microservicio
        repo_url: https://git.midominio.com/unidad_negocio/otro_microservicio
        # Puedes sobrescribir valores específicos aquí
        # credentials_id: otro-token
```

## Instalación y Uso

Este proyecto utiliza `uv` como gestor de paquetes.

Para ejecutar la herramienta directamente sin necesidad de instalar el entorno de manera global, puedes usar:

```bash
# Ejecutar usando la configuración por defecto (jobs.yml)
uv run jjf

# Usar un archivo de configuración específico
uv run jjf --config mi-configuracion.yml

# Crear los jobs sin lanzar un scan automático
uv run jjf --no-scan
```

## Arquitectura del Proyecto

- `src/jenkins_job_factory/main.py`: Punto de entrada del CLI. Maneja los argumentos y orquesta la creación.
- `src/jenkins_job_factory/config.py`: Definición de las estructuras de datos (Dataclasses) y carga del archivo YAML.
- `src/jenkins_job_factory/client.py`: Cliente HTTP (vía `requests`) para interactuar con la API REST de Jenkins.
- `src/jenkins_job_factory/xml_templates.py`: Plantillas XML que definen la estructura base de los Folders y Multibranch Pipelines.
