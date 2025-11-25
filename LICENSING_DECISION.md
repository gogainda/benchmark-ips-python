# Licensing Decision for Python Port

## Summary

✅ **Decision:** Use MIT License (same as original)
✅ **Status:** Fully compliant with original license
✅ **Attribution:** Proper credit to original author

## Background

The original Ruby `benchmark-ips` gem is licensed under the **MIT License** (2015) by **Evan Phoenix**.

### What is the MIT License?

The MIT License is one of the most **permissive open-source licenses**. It allows:

- ✅ Commercial use
- ✅ Modification
- ✅ Distribution
- ✅ Private use
- ✅ **Creating derivative works** (like our Python port)

**Only requirement:** Include original copyright and license notices.

## Our Approach

### 1. License Choice: MIT (Maintained)

**Why MIT?**
- ✅ Original uses MIT - maintains compatibility
- ✅ Permissive - allows maximum freedom
- ✅ Simple - easy to understand
- ✅ Popular - widely accepted in Python community
- ✅ Compatible - works with other open-source projects

**Alternative considered:** Could have used different license, but MIT:
- Honors original author's intent
- Avoids license incompatibilities
- Simplifies usage for end users

### 2. Attribution Strategy

We properly attribute the original work through:

1. **LICENSE_PYTHON** - Dual copyright notice:
   ```
   Copyright (c) 2015 Evan Phoenix (Original Ruby implementation)
   Copyright (c) 2025 Python Port Contributors
   ```

2. **NOTICE** - Clear attribution:
   - States this is a derivative work
   - Credits original author
   - Links to original repository

3. **CREDITS.md** - Detailed acknowledgments:
   - Full credit to Evan Phoenix
   - Thanks to Ruby community
   - Explanation of translation approach

4. **README_PYTHON.md** - Prominent attribution:
   - Links to original project
   - Credits in introduction
   - License section

### 3. File Structure

```
LICENSE              - Original Ruby gem license (preserved)
LICENSE_PYTHON       - Python port license (includes original)
LICENSE_SUMMARY.md   - Easy-to-read summary
NOTICE               - Attribution notice
CREDITS.md           - Detailed credits
LICENSING_DECISION.md - This file (rationale)
```

## Legal Compliance

### MIT License Requirements

✅ **Include copyright notice** - Done in LICENSE_PYTHON
✅ **Include license text** - Done in LICENSE_PYTHON
✅ **Include in all copies** - Documented in all files

### Derivative Work Rules

✅ **Acknowledge original** - Multiple files credit Evan Phoenix
✅ **Same or compatible license** - Using same MIT License
✅ **Don't claim original authorship** - Clear it's a port

## Best Practices Followed

1. **Transparency**
   - Clear this is a port/translation
   - Not claiming to be official
   - Links to original prominently displayed

2. **Attribution**
   - Multiple places credit original author
   - CREDITS.md provides detailed acknowledgment
   - README includes prominent attribution

3. **License Compatibility**
   - Using same license as original
   - No license conflicts
   - Easy for users to understand

4. **Documentation**
   - Multiple license files for clarity
   - This rationale document
   - Summary for quick reference

## For Users

### Can I use this commercially?

✅ **Yes!** MIT License allows commercial use.

### Do I need to credit the authors?

✅ **Yes!** Include the license notices from LICENSE_PYTHON.

### Can I modify it?

✅ **Yes!** MIT License allows modification.

### Can I distribute it?

✅ **Yes!** MIT License allows distribution (with license notices).

### What about warranties?

❌ **No warranties** - Software provided "as is" (standard for MIT).

## For Contributors

If you contribute to this Python port:

1. **Your contributions** are under MIT License
2. **Maintain attribution** to original author
3. **Follow same license** for compatibility
4. **Update CREDITS.md** if you make significant contributions

## Relationship to Original

This Python port is:

- ✅ A **derivative work** (allowed by MIT License)
- ✅ An **independent implementation** (not a fork)
- ✅ **Properly attributed** (credits original)
- ✅ **Same license** (maintains compatibility)

**Not:**
- ❌ An official port (unless adopted by original author)
- ❌ A replacement for original (complements it)
- ❌ Claiming original authorship

## Future Considerations

### If Published to PyPI

When publishing to Python Package Index:

1. **Classifiers:** Include MIT License classifier
2. **Metadata:** Link to original Ruby gem
3. **Description:** State it's a port
4. **License file:** Include LICENSE_PYTHON

### If Original Author Wants Involvement

If Evan Phoenix or Ruby gem maintainers want to:

- ✅ Adopt this as official Python port
- ✅ Contribute improvements
- ✅ Suggest changes

**We welcome collaboration!** The MIT License makes this easy.

## References

- **Original Repository:** https://github.com/evanphx/benchmark-ips
- **MIT License Text:** https://opensource.org/licenses/MIT
- **MIT License Guide:** https://choosealicense.com/licenses/mit/

## Conclusion

Our licensing approach:

1. ✅ **Respects** the original author and their license choice
2. ✅ **Complies** fully with MIT License requirements
3. ✅ **Provides** clear attribution and credit
4. ✅ **Maintains** the open-source spirit of the original
5. ✅ **Enables** maximum freedom for users

**Bottom Line:** This is a properly licensed, compliant derivative work that honors the original while bringing the functionality to Python! 🎉

---

*Created: November 2025*
*License: MIT (same as original)*
