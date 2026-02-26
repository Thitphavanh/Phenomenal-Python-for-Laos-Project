# Git Branch Naming Convention

This document outlines the branch naming conventions for the Phenomenal Python for Laos Project.

## Format
```
type/description-in-kebab-case
```

## Branch Types

### `feature/` - New Features or Significant Functionality
Use for adding new features or major functionality to the project.

**Examples:**
```bash
git checkout -b feature/add-payment-gateway
git checkout -b feature/user-authentication
git checkout -b feature/course-enrollment
git checkout -b feature/ai-chatbot-integration
```

### `fix/` - Bug Fixes
Use for fixing bugs in the existing codebase.

**Examples:**
```bash
git checkout -b fix/login-validation
git checkout -b fix/quote-calculation
git checkout -b fix/payment-qr-generation
git checkout -b fix/course-video-playback
```

### `hotfix/` - Urgent Production Fixes
Use for critical fixes that need immediate deployment to production.

**Examples:**
```bash
git checkout -b hotfix/security-vulnerability
git checkout -b hotfix/payment-processing-error
git checkout -b hotfix/database-connection
```

### `refactor/` - Code Refactoring
Use for code restructuring without changing functionality.

**Examples:**
```bash
git checkout -b refactor/payment-service
git checkout -b refactor/database-queries
git checkout -b refactor/authentication-logic
```

### `style/` - Code Style Changes
Use for formatting, UI/UX improvements, or non-functional changes.

**Examples:**
```bash
git checkout -b style/update-button-colors
git checkout -b style/fix-mobile-layout
git checkout -b style/dark-mode-improvements
git checkout -b style/tailwind-styling
```

### `docs/` - Documentation Only
Use for documentation updates or additions.

**Examples:**
```bash
git checkout -b docs/api-documentation
git checkout -b docs/setup-guide
git checkout -b docs/deployment-instructions
git checkout -b docs/contributing-guide
```

### `test/` - Testing
Use for adding or modifying tests.

**Examples:**
```bash
git checkout -b test/payment-integration
git checkout -b test/user-authentication
git checkout -b test/course-enrollment
```

### `chore/` - Maintenance Tasks
Use for maintenance, dependencies, configurations, and build tasks.

**Examples:**
```bash
git checkout -b chore/update-dependencies
git checkout -b chore/configure-ci-cd
git checkout -b chore/update-gitignore
git checkout -b chore/setup-docker
```

## Best Practices

1. **Keep it short but descriptive**: Use 2-4 words in kebab-case
2. **Use lowercase**: All branch names should be lowercase
3. **Be specific**: Clearly describe what the branch does
4. **Use hyphens**: Separate words with hyphens, not underscores
5. **Avoid special characters**: Stick to letters, numbers, and hyphens

## Branch Workflow

### Creating a New Branch
```bash
# Always create new branches from main
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
```

### Working on a Branch
```bash
# Make your changes
git add .
git commit -m "descriptive commit message"
git push -u origin feature/your-feature-name
```

### Merging to Main
```bash
# Before merging, ensure your branch is up to date
git checkout main
git pull origin main
git checkout feature/your-feature-name
git merge main

# Create a pull request on GitHub
# After approval, merge via GitHub
```

### Deleting Merged Branches
```bash
# Delete local branch
git branch -d feature/your-feature-name

# Delete remote branch
git push origin --delete feature/your-feature-name
```

## Protected Branches

The following branches should be protected on GitHub:
- `main` - Production-ready code
- `develop` (if used) - Integration branch for features

## Example Workflow

```bash
# Starting a new feature
git checkout main
git pull origin main
git checkout -b feature/add-lao-language-support

# Make changes, commit often
git add .
git commit -m "Add Lao language translations for home page"

# Push to remote
git push -u origin feature/add-lao-language-support

# Create Pull Request on GitHub
# After review and approval, merge to main
# Delete the feature branch after merging
```

## Common Mistakes to Avoid

❌ **Don't:**
- Use vague names: `fix/bug` or `feature/update`
- Mix types: `feature-fix/something`
- Use underscores: `feature_new_payment`
- Use spaces: `feature/new payment`
- Work directly on main

✅ **Do:**
- Be specific: `fix/payment-gateway-timeout`
- Follow the convention: `feature/add-payment-gateway`
- Use kebab-case: `feature/user-profile-page`
- Create descriptive names: `docs/setup-postgresql-guide`
- Always branch from main

---

**Remember:** Good branch naming helps team collaboration and makes the project history clear and maintainable.
