# 🔐 Security Policy

## Supported Versions

We regularly maintain and support the following versions of this project:

| Version | Supported          |
|---------|--------------------|
| 1.x     | ✅ Yes              |
| <1.0    | ❌ No (legacy only) |

---

## 📢 Reporting a Vulnerability

If you discover a security vulnerability, please **do not file a public issue**.

Instead, report it confidentially to:

📧 **your-email@example.com**

Please include:
- A clear description of the vulnerability
- Steps to reproduce
- The potential impact
- Suggested remediation (if known)

We aim to respond within **48 hours** and resolve validated issues as soon as possible.

---

## 🛡️ Security Best Practices

This project follows several best practices for security:

### 🔐 Authentication & Authorization
- Uses **JWT** for secure stateless authentication
- Implements **role-based access control** for API endpoints

### 🔒 Secrets Management
- All credentials and secrets are stored in **`.env`** files and **excluded** from version control
- No hardcoded secrets in source files

### 📦 Dependencies
- Uses **`pip`** and `requirements.txt` with pinned versions
- Monitored via GitHub Dependabot and **CodeQL analysis**

### 📄 Input Validation
- All user inputs are validated using Django REST Framework serializers
- File uploads are restricted and validated

### 🚫 Debug Mode
- `DEBUG = False` is enforced in production deployments
- `ALLOWED_HOSTS` is always defined

---

## 🔍 Security Scanning & Monitoring

| Tool        | Purpose                      | Status   |
|-------------|------------------------------|----------|
| Bandit      | Python code vulnerability scan | ✅ Manual / Optional |
| CodeQL      | GitHub static analysis         | ✅ Enabled via Actions |
| Dependabot  | Dependency vulnerability alerts | ✅ Enabled |
| Secret Scanning | Detect secrets in commits     | ✅ Enabled |

---

## 📢 Disclosure Policy

- We responsibly disclose security issues
- Users will be notified of any major vulnerability via GitHub Releases or Issues
- Patch releases will be issued as quickly as possible after confirming a vulnerability

---

## 📅 Security Update Schedule

This project receives:
- **Monthly reviews** for dependency updates
- **Immediate patching** for any critical vulnerability

---

## 📬 Contact

If you have general security concerns or need support:

**Email:** [your-email@example.com](mailto:your-email@example.com)

---

Thanks for helping us keep this project safe and secure!
