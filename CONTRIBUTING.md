# Contributing to BharatAI Citizen Assistant

Thank you for your interest in contributing to BharatAI! We welcome contributions from the community to help make government information more accessible to every Indian citizen.

## How to Contribute

### Reporting Bugs
- Search existing [Issues](https://github.com/bharatai/citizenai_assistant/issues) to see if the bug has already been reported.
- If not, open a new issue. Use a clear and descriptive title.
- Provide a step-by-step reproduction of the bug, including your environment (OS, Python version) and any error logs.

### Proposing Features
- We love new ideas! Please open an issue with the "feature request" label.
- Describe the feature, why it’s useful for citizens, and how you imagine it working.

### Pull Request Process
1. **Fork the repository** and create your branch from `main`.
2. **Set up the development environment**:
   - Backend: `cd backend && pip install -r requirements.txt`
   - Frontend: `pip install streamlit requests`
3. **Make your changes**. Ensure your code follows PEP 8 for Python and maintain consistency with the existing codebase.
4. **Add tests** if you're adding new functionality.
5. **Update documentation** if your changes affect how users interact with the application.
6. **Submit the PR**:
   - Provide a clear description of the changes.
   - Reference any related issues (e.g., "Closes #123").
   - Ensure the CI/CD pipeline passes.

## Development Standards
- **Clarity over Complexity**: Our goal is to serve citizens. Keep the logic transparent and well-documented.
- **Security**: Never commit API keys or sensitive environment variables.
- **Accuracy**: BharatAI relies on official sources. Ensure any changes to the RAG pipeline maintain high retrieval accuracy and verification.

## Questions?
If you have any questions, feel free to reach out via GitHub Discussions or open an issue for clarification.
