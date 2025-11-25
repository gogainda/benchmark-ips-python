# Naming Conventions for Software Ports

## Common Patterns for Language Ports

### Pattern 1: Prefix with Language Name
**Format:** `language-originalname` or `py-originalname`

**Examples:**
- `requests` (Python) ← `HTTParty` (Ruby concept)
- `py-bcrypt` ← `bcrypt` (C library)
- `python-dateutil` ← Various date utilities
- `py-pillow` ← PIL (Python Imaging Library)

**Pros:**
✅ Immediately clear it's a Python version
✅ Easy to find in package searches
✅ Common in package managers (pip, apt, etc.)

**Cons:**
❌ Longer name
❌ Less memorable

**Used by:** PyPI packages, system packages (apt, yum)

---

### Pattern 2: Suffix with Language Name
**Format:** `originalname-python` or `originalname-py`

**Examples:**
- `redis-py` ← Redis (C)
- `mysql-python` ← MySQL client
- `stripe-python` ← Stripe API
- `openai-python` ← OpenAI API

**Pros:**
✅ Keeps original name prominent
✅ Clear it's a port/client
✅ Groups related projects together

**Cons:**
❌ Less common for pure ports

**Used by:** API clients, database drivers

---

### Pattern 3: Keep Original Name
**Format:** `originalname` (same as original)

**Examples:**
- `pytest` (Python) vs `RSpec` (Ruby) - different name, same concept
- `flask` (Python) vs `Sinatra` (Ruby) - similar concept, different name
- `numpy` (Python) - no direct equivalent, unique name
- `django` (Python) - unique name

**Pros:**
✅ Simple, memorable
✅ Can become the "canonical" name for that language
✅ No confusion about which version

**Cons:**
❌ May conflict with original
❌ Not clear it's related to original
❌ Only works if original name isn't taken

**Used by:** Standalone projects, reimplementations

---

### Pattern 4: Modified/Related Name
**Format:** Creative variation on original

**Examples:**
- `pytest` ← concept from `RSpec`, `unittest`
- `httpx` ← next gen of `httplib`/`requests`
- `uvicorn` ← related to `Gunicorn`
- `pydantic` ← "pedantic" + "Python"

**Pros:**
✅ Shows relationship but unique
✅ Can indicate improvements/differences
✅ Memorable

**Cons:**
❌ May not be obvious connection
❌ Requires creative naming

**Used by:** Spiritual successors, inspired-by projects

---

## PyPI (Python Package Index) Examples

### Direct Ports of Ruby Gems:

| Ruby Gem | Python Package | Pattern |
|----------|---------------|---------|
| `rake` | `pynt` | Modified name |
| `bundler` | `pip` | Different name (equivalent tool) |
| `rspec` | `pytest` | Modified name (inspired by) |
| `rails` | `django` | Different name (similar concept) |
| `sinatra` | `flask` | Different name (inspired by) |
| `nokogiri` | `lxml` / `beautifulsoup` | Different name |

### Observation:
**Most Ruby → Python ports use DIFFERENT names** because:
1. Python ecosystem already has established tools
2. Ports often have different philosophies
3. Direct ports are rare (usually reimagined)

---

## For Our Case: benchmark-ips

### Current Ruby Gem:
```
Name: benchmark-ips
Repo: github.com/evanphx/benchmark-ips
```

### Naming Options for Python Port:

#### Option 1: `benchmark-ips` (Keep Same Name)
```python
# PyPI: benchmark-ips
# Import: import benchmark_ips
# Repo: benchmark-ips-python or python-benchmark-ips
```

**Pros:**
- ✅ Same name as Ruby gem (clear relationship)
- ✅ Name not taken on PyPI (checked)
- ✅ Users familiar with Ruby gem find it easily
- ✅ Shows it's a direct port

**Cons:**
- ❌ Repo name needs language identifier
- ❌ Might cause confusion (which language?)

#### Option 2: `python-benchmark-ips`
```python
# PyPI: python-benchmark-ips
# Import: import benchmark_ips
# Repo: python-benchmark-ips
```

**Pros:**
- ✅ Very clear it's Python
- ✅ Consistent naming everywhere
- ✅ Common pattern for ports

**Cons:**
- ❌ Longer name
- ❌ Less elegant

#### Option 3: `py-benchmark-ips`
```python
# PyPI: py-benchmark-ips  
# Import: import benchmark_ips
# Repo: py-benchmark-ips
```

**Pros:**
- ✅ Clear but shorter
- ✅ Common pattern (py-* packages)
- ✅ Matches BSD ports convention

**Cons:**
- ❌ Slightly less formal

#### Option 4: `benchmarkips` (No Hyphen)
```python
# PyPI: benchmarkips
# Import: import benchmarkips
# Repo: benchmarkips-python
```

**Pros:**
- ✅ Shorter, more Pythonic
- ✅ PEP 8 prefers underscores in imports

**Cons:**
- ❌ Loses the "IPS" distinction
- ❌ Less clear connection to original

---

## Research: Real PyPI Packages

### Checking Similar Patterns:

```bash
# Ports/Clients with language prefix:
python-dateutil       ← Date utilities
python-telegram-bot   ← Telegram API
python-jose           ← JOSE (JavaScript Object Signing)
python-multipart      ← Multipart handling

# Ports/Clients with language suffix:
redis-py             ← Redis client
mysql-python         ← MySQL client
stripe-python        ← Stripe API
```

---

## Recommendation for benchmark-ips

### **Recommended: Option 1 (Keep Original Name)**

**PyPI Package Name:** `benchmark-ips`
**Import Name:** `benchmark_ips`
**Repository Name:** `benchmark-ips-python`

### Rationale:

1. **Not Taken:** `benchmark-ips` is available on PyPI
2. **Clear Relationship:** Same name as Ruby gem
3. **Import Style:** Python convention uses underscores
4. **Repo Clarification:** `-python` suffix in repo URL

### Full Naming:

```python
# PyPI
pip install benchmark-ips

# Import
import benchmark_ips as bm

# Repository
github.com/YOUR_USERNAME/benchmark-ips-python

# Documentation
"benchmark-ips: Python port of the Ruby gem"
```

### Why This Works:

1. ✅ **Familiar:** Ruby users recognize the name
2. ✅ **Clear:** "-python" in repo shows language
3. ✅ **Pythonic:** Import uses underscores (PEP 8)
4. ✅ **Available:** Name is free on PyPI
5. ✅ **Honest:** Credits original in description

---

## Convention Summary

### For Direct Ports:
```
✅ Use: original-name (if available)
✅ Repo: original-name-python
✅ Import: original_name (Python convention)
✅ Docs: "Python port of [original]"
```

### For Inspired-By:
```
✅ Use: creative-related-name
✅ Repo: creative-name
✅ Import: creative_name
✅ Docs: "Inspired by [original]"
```

### For API Clients:
```
✅ Use: service-python
✅ Repo: service-python
✅ Import: service
✅ Docs: "Python client for [service]"
```

---

## Examples from the Wild

### Pattern Analysis:

| Original | Python Port | Naming Strategy |
|----------|-------------|-----------------|
| Redis | `redis-py` | Suffix pattern |
| PostgreSQL | `psycopg2` | Creative name |
| MySQL | `mysql-python` / `pymysql` | Both patterns exist! |
| Stripe API | `stripe-python` | Suffix pattern |
| AWS SDK | `boto3` | Creative name |
| Pillow | `Pillow` (PIL) | Same name (fork) |

---

## Final Recommendation

For `benchmark-ips` Python port:

### Package Naming:
```
PyPI:        benchmark-ips
Import:      benchmark_ips
Repository:  benchmark-ips-python
```

### Rationale:
1. Direct port (not inspired-by)
2. Name available on PyPI
3. Clear relationship to original
4. Python conventions followed
5. No namespace conflicts

### Alternative (if you prefer):
```
PyPI:        py-benchmark-ips
Import:      benchmark_ips
Repository:  py-benchmark-ips
```

**Both are valid! Choose based on preference.**

---

## References

- PEP 8: Python naming conventions
- PyPI: Python Package Index naming
- RubyGems: Ruby package naming
- npm: Node.js package naming (different conventions)

**Conclusion:** For a direct port, keeping the original name with language clarification in the repo is most common and user-friendly!
