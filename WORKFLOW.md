# ProjectForge Development Workflow

This guide outlines the branching strategy and development workflow for ProjectForge.

## Branch Structure

- **`main`** - Production branch (deployed to https://projectforge.streamlit.app/)
- **`dev`** - Development/integration branch (for testing before production)
- **`feature/*`** - Feature branches (optional, for larger features)
- **`hotfix/*`** - Emergency fixes for production

---

## Daily Development Workflow

Use the `dev` branch for all regular development work.

### 1. Start Your Work Session

```bash
# Make sure you're on dev branch
git checkout dev

# Pull latest changes
git pull origin dev

# Activate virtual environment
source .venv/bin/activate
```

### 2. Make Changes

Edit code, add features, fix bugs as needed.

### 3. Test Locally

```bash
# Launch Streamlit app
.venv/bin/python -m streamlit run app.py

# Open http://localhost:8501
# Test your changes in both light and dark modes
```

### 4. Commit and Push to Dev

```bash
# Stage your changes
git add .

# Commit with descriptive message
git commit -m "feat: add user authentication feature"

# Push to dev branch
git push origin dev
```

**Commit Message Conventions:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, no logic change)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

---

## Deploying to Production

When `dev` is stable and tested, promote it to production.

### 1. Switch to Main Branch

```bash
git checkout main
```

### 2. Pull Latest Main

```bash
git pull origin main
```

### 3. Merge Dev into Main

```bash
# Merge dev branch
git merge dev

# If there are conflicts, resolve them and commit
```

### 4. Push to Trigger Deployment

```bash
# This triggers Streamlit Cloud to redeploy
git push origin main
```

### 5. Verify Production Deployment

- Visit https://projectforge.streamlit.app/
- Test critical functionality
- Check for any deployment errors in Streamlit Cloud dashboard

### 6. Return to Dev Branch

```bash
git checkout dev
```

---

## Quick Hotfix Workflow

For urgent production bugs that can't wait for the normal dev cycle.

### 1. Create Hotfix Branch from Main

```bash
# Make sure main is up to date
git checkout main
git pull origin main

# Create hotfix branch
git checkout -b hotfix/fix-pdf-generation-error
```

### 2. Fix the Bug

Make minimal changes to fix the critical issue.

### 3. Test the Hotfix

```bash
# Test locally
.venv/bin/python -m streamlit run app.py

# Verify the fix works
```

### 4. Commit and Merge to Main

```bash
# Commit the fix
git add .
git commit -m "hotfix: fix PDF generation memory leak"

# Switch to main
git checkout main

# Merge hotfix
git merge hotfix/fix-pdf-generation-error

# Push to production
git push origin main
```

### 5. Merge Hotfix Back to Dev

```bash
# Switch to dev
git checkout dev

# Merge the hotfix so dev stays in sync
git merge hotfix/fix-pdf-generation-error

# Push to dev
git push origin dev
```

### 6. Clean Up Hotfix Branch

```bash
# Delete local hotfix branch
git branch -d hotfix/fix-pdf-generation-error

# Delete remote hotfix branch (optional)
git push origin --delete hotfix/fix-pdf-generation-error
```

---

## Feature Branch Workflow (Optional)

For larger features that take multiple days/sessions.

### 1. Create Feature Branch from Dev

```bash
git checkout dev
git pull origin dev
git checkout -b feature/web-hitl-implementation
```

### 2. Develop the Feature

Work on the feature over multiple sessions, committing regularly.

### 3. Keep Feature Branch Updated

```bash
# Periodically merge dev to avoid conflicts
git checkout feature/web-hitl-implementation
git merge dev
```

### 4. Merge Back to Dev When Complete

```bash
# Switch to dev
git checkout dev

# Merge feature branch
git merge feature/web-hitl-implementation

# Push to dev
git push origin dev

# Delete feature branch
git branch -d feature/web-hitl-implementation
```

---

## Branch Protection Best Practices

### Protect Main Branch

On GitHub, configure branch protection rules:

1. Go to **Settings → Branches → Add rule**
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Include administrators

### Pull Request Template

When merging to `main`, create a PR with:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tested locally
- [ ] Tested in dev branch
- [ ] Light mode verified
- [ ] Dark mode verified

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No console errors
```

---

## Quick Reference Commands

```bash
# Check current branch
git branch

# See all branches
git branch -a

# Switch branches
git checkout <branch-name>

# See uncommitted changes
git status

# See commit history
git log --oneline --graph --all

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Discard all local changes
git reset --hard origin/dev
```

---

## Troubleshooting

### Merge Conflicts

```bash
# When merge conflicts occur
git status  # See conflicting files

# Edit files to resolve conflicts
# Look for <<<<<<, ======, >>>>>> markers

# After resolving
git add .
git commit -m "resolve merge conflicts"
```

### Accidentally Committed to Main

```bash
# If you committed to main instead of dev
git checkout main
git reset --soft HEAD~1  # Undo commit, keep changes
git stash  # Save changes
git checkout dev
git stash pop  # Apply changes to dev
git add .
git commit -m "your message"
```

### Lost Work

```bash
# Find lost commits
git reflog

# Recover specific commit
git cherry-pick <commit-hash>
```

---

## Support

For questions or issues with the workflow:
- Check existing GitHub Issues
- Review commit history: `git log`
- Contact repository maintainer
