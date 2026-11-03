# DevOps Lab

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)
![Git](https://img.shields.io/badge/Git-Version_Control-F05032?logo=git&logoColor=white)
![Status](https://img.shields.io/badge/Status-In_Development-orange)

**DevOps Lab** is a hands-on engineering project focused on building, testing, automating, deploying, and maintaining modern software applications using industry-standard DevOps practices.

The project follows a practical, incremental learning approach: writing code regularly, applying engineering principles, documenting progress, and continuously improving the application.

## Project Objectives

- Develop maintainable and scalable Python applications.
- Implement automated testing and code quality checks.
- Containerize applications using Docker.
- Build Continuous Integration and Continuous Deployment (CI/CD) pipelines.
- Apply Linux and server administration practices.
- Implement application logging and monitoring.
- Understand deployment workflows and production infrastructure.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | API framework |
| Git | Version control |
| GitHub | Collaboration and source code hosting |
| Pytest | Automated testing |
| Docker | Application containerization |
| GitHub Actions | CI/CD automation |
| Linux | Server administration |

*Additional technologies will be introduced as the project evolves.*

## Project Structure

```text
Devops_lab/
├── app/
│   ├── __init__.py
│   └── main.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git
- PowerShell, Linux terminal, or macOS terminal

### Installation

1. Clone the repository:

```bash
git clone https://github.com/Ronniee7/Devops_lab.git
cd Devops_lab
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the environment.

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
uvicorn app.main:app --reload
```

The API documentation will be available at:

- http://127.0.0.1:8000/docs

## Development Roadmap

The project is being developed incrementally through the following stages:

- [x] Initialize repository and Python development environment.
- [ ] Establish API architecture.
- [ ] Implement API endpoints and request validation.
- [ ] Introduce automated testing with Pytest.
- [ ] Containerize the application with Docker.
- [ ] Implement CI pipelines using GitHub Actions.
- [ ] Configure automated deployment.
- [ ] Implement logging and monitoring.
- [ ] Document production deployment procedures.

## Contribution Guidelines

Contributions, suggestions, and improvements are welcome.

To contribute:

1. Fork the repository.
2. Create a feature branch:

```bash
git switch -c feature/your-feature-name
```

3. Implement your changes.
4. Test your changes.
5. Commit using a descriptive message:

```bash
git commit -m "feat: describe your contribution"
```

6. Push your branch and open a Pull Request.

Please ensure that contributions are clear, focused, and properly documented.

## Engineering Philosophy

This project emphasizes:

- **Consistency:** Regular development and incremental improvements.
- **Automation:** Reducing repetitive manual operations.
- **Reliability:** Building software that is testable and maintainable.
- **Security:** Protecting application data and configuration.
- **Collaboration:** Using professional Git workflows and code reviews.
- **Documentation:** Making engineering decisions understandable and reproducible.

## License

This project is currently under development. Licensing information will be added as the project evolves.
