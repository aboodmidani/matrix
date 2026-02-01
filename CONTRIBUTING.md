# Contributing to Web Security Matrix

Thank you for your interest in contributing to Web Security Matrix! We welcome contributions from the community and are committed to making the contribution process as smooth as possible.

## 🚀 Quick Start

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/web-security-matrix.git
   cd web-security-matrix
   ```
3. **Set up development environment**:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # Frontend (new terminal)
   cd frontend
   npm install
   npm run dev
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/amazing-feature
   ```

## 📋 Contribution Guidelines

### 🐛 Reporting Bugs

When reporting bugs, please include:

- **Clear title** describing the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs. actual behavior
- **Environment details**: OS, Python/Node versions
- **Screenshots** if applicable
- **Log output** if relevant

### 💡 Suggesting Features

For feature requests:

- **Check existing issues** first to avoid duplicates
- **Describe the problem** the feature would solve
- **Explain the solution** you'd like to see
- **Consider alternatives** you've thought about
- **Include mockups** if applicable

### 🔧 Pull Request Process

1. **Update documentation** for any changed functionality
2. **Add tests** for new features or bug fixes
3. **Ensure all tests pass** locally
4. **Update CHANGELOG.md** with your changes
5. **Follow the existing code style**
6. **Write clear commit messages**

### 📝 Code Style

#### Python (Backend)
- Follow **PEP 8** style guidelines
- Use **type hints** for function parameters and return values
- Write **docstrings** for all functions and classes
- Maximum line length: **88 characters** (Black formatter)
- Use **meaningful variable names**

#### JavaScript/Vue (Frontend)
- Use **ES6+** syntax where possible
- Follow **Vue.js style guide**
- Use **meaningful component and variable names**
- Consistent **indentation** (2 spaces)
- **Single quotes** for strings, **double quotes** for JSX attributes

### 🧪 Testing

#### Backend Tests
```bash
cd backend
python -m pytest tests/ -v --cov=. --cov-report=html
```

#### Frontend Tests
```bash
cd frontend
npm run test
npm run test:e2e  # End-to-end tests
```

#### Test Coverage
- Maintain **80%+ code coverage**
- Write tests for **new features**
- Test **error conditions** and **edge cases**

## 🏗️ Architecture Guidelines

### Backend Structure
```
backend/
├── main.py              # FastAPI application and routes
├── scanners.py          # Scanning modules and utilities
├── intelligence.py      # Technology detection and intelligence
├── vulnerabilities.py   # Vulnerability scanning logic
├── tests/               # Unit and integration tests
├── requirements.txt     # Python dependencies
└── Dockerfile          # Container configuration
```

### Frontend Structure
```
frontend/
├── src/
│   ├── App.vue         # Main Vue application
│   ├── components/     # Reusable Vue components
│   └── assets/         # Static assets
├── public/             # Public static files
├── package.json        # Node dependencies
└── Dockerfile         # Container configuration
```

## 🔒 Security Considerations

### 🔐 When Adding New Features

- **Validate all inputs** thoroughly
- **Implement proper error handling** - never expose sensitive information
- **Consider rate limiting** for resource-intensive operations
- **Use secure defaults** for any configurable options
- **Document security implications** in code comments

### 🚨 Reporting Security Issues

If you discover a security vulnerability, please:

- **DO NOT** create a public issue
- **Email** security@example.com with details
- **Allow time** for the issue to be resolved before public disclosure

## 📚 Documentation

### Code Documentation
- **Function docstrings** explaining purpose, parameters, and return values
- **Inline comments** for complex logic
- **README updates** for new features
- **API documentation** for backend endpoints

### User Documentation
- **Installation instructions** in README.md
- **Usage examples** and screenshots
- **Troubleshooting guide** for common issues
- **Configuration options** clearly documented

## 🎯 Development Workflow

### 1. Choose an Issue
- Check the [Issues](https://github.com/yourusername/web-security-matrix/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Development Process
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes with clear commit messages
git commit -m "feat: add new vulnerability scan type"

# Push changes
git push origin feature/your-feature-name
```

### 3. Pull Request
- **Title**: Clear, descriptive summary
- **Description**: Detailed explanation of changes
- **Screenshots**: For UI changes
- **Tests**: Ensure all tests pass
- **Documentation**: Updated as needed

## 🌟 Recognition

Contributors will be:
- Listed in **CONTRIBUTORS.md**
- Mentioned in **CHANGELOG.md**
- Featured in release notes
- Acknowledged in documentation

## 📞 Getting Help

- **GitHub Discussions**: General questions and help
- **GitHub Issues**: Bug reports and feature requests
- **Discord**: Real-time chat (if available)

## 📜 Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## 📋 License

By contributing to Web Security Matrix, you agree that your contributions will be licensed under the same MIT License that covers the project.

---

**Thank you for contributing to Web Security Matrix! 🚀**
