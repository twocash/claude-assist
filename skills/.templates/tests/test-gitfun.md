# Test: gitfun

## Scenario 1: Simple npm Package (Easy)

**Input:**
```
User: gitfun https://github.com/lodash/lodash
```

**Expected Behavior:**
- Fetches repository README
- Identifies as JavaScript/npm package
- Counts minimal dependencies
- Rates as 🟢 EASY
- Time estimate: 5-15 minutes
- Clear installation command shown

**Verification:**
- [ ] Correctly identifies primary language
- [ ] Dependency count accurate
- [ ] Setup steps extracted from README
- [ ] Complexity rating makes sense
- [ ] Time estimate realistic
- [ ] Red flags section appropriate (or empty)

---

## Scenario 2: Complex Full-Stack App (Hard)

**Input:**
```
User: how hard to install https://github.com/nextcloud/server
```

**Expected Behavior:**
- Identifies multiple prerequisites (PHP, MySQL/PostgreSQL, web server)
- Counts extensive configuration requirements
- Lists multiple setup steps
- Rates as 🔴 HARD or 🟠 CHALLENGING
- Time estimate: 4-6+ hours
- Red flags about server configuration

**Verification:**
- [ ] Identifies all major prerequisites
- [ ] Configuration complexity noted
- [ ] Realistic time estimate (not optimistic)
- [ ] Red flags include server setup, database config
- [ ] Recommended approach includes warnings

---

## Scenario 3: Python CLI Tool (Moderate)

**Input:**
```
User: analyze github repo https://github.com/django/django
```

**Expected Behavior:**
- Identifies Python project
- Checks for requirements.txt / pyproject.toml
- Counts dependencies
- Notes database requirement
- Rates as 🟡 MODERATE to 🟠 CHALLENGING
- Time estimate: 1-3 hours

**Verification:**
- [ ] Python dependencies counted
- [ ] Database prerequisite identified
- [ ] Configuration requirements noted
- [ ] Documentation quality assessed
- [ ] Rating reflects web framework complexity

---

## Scenario 4: Docker-Based Project

**Input:**
```
User: gitfun https://github.com/some/docker-app
```

**Expected Behavior:**
- Identifies Docker requirement immediately
- Notes docker-compose.yml presence
- Checks for .env.example files
- Rates based on service complexity
- Warns about Docker resource requirements

**Verification:**
- [ ] Docker listed as prerequisite
- [ ] Multi-service setup noted if applicable
- [ ] Memory/resource requirements mentioned
- [ ] Port conflicts flagged if many services
- [ ] Time estimate includes container build time

---

## Scenario 5: Well-Documented Simple Project

**Input:**
```
User: is this easy to set up https://github.com/simple/well-docs
```

**Expected Behavior:**
- Identifies excellent documentation
- Subtracts points for doc quality
- May rate as EASY despite some complexity
- Clear step-by-step installation shown
- Acknowledges good docs in summary

**Verification:**
- [ ] Documentation quality bonus applied (-1 or -2 points)
- [ ] Final rating benefits from good docs
- [ ] Installation summary references clear instructions
- [ ] Recommended approach mentions following README

---

## Scenario 6: Poorly Documented Complex Project

**Input:**
```
User: gitfun https://github.com/complex/no-docs
```

**Expected Behavior:**
- Notes missing/poor documentation
- No documentation bonus (0 adjustment)
- May rate higher difficulty due to doc issues
- Red flag about documentation quality
- Recommended approach includes "expect to debug"

**Verification:**
- [ ] Documentation quality issue identified
- [ ] No points subtracted for docs
- [ ] Red flag mentions poor documentation
- [ ] Time estimate inflated due to debugging
- [ ] Recommended approach warns about trial-and-error

---

*Test template for gitfun v1.0*
