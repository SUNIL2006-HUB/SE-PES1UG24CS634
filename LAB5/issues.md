# Static Code Analysis Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Unsafe object deserialization using pickle | Security (High) | Original backup/restore functions | Pickle can execute malicious code when loading an untrusted backup. | Replaced pickle serialization with JSON. |
| Hardcoded synchronization password | Security (Medium) | Original constant declaration | A password embedded in source code can be exposed to anyone who reads the file. | Removed the unused hardcoded password. |
| Missing module and function documentation | Code Quality (Low) | Throughout original file | Missing docstrings make the program harder to understand and maintain. | Added module and function docstrings. |
| Non-standard naming conventions | Code Quality (Low) | Original function declarations | CamelCase names do not follow the usual Python function naming convention. | Used lowercase names with underscores. |
| Broad exception handling | Code Quality (Medium) | Original city update function | Catching every exception can hide unexpected programming errors. | Caught only `KeyError` when the contact does not exist. |
| File operations without explicit encoding | Code Quality (Low) | Original CSV and backup functions | The default text encoding can vary between environments. | Specified UTF-8 for text file operations. |
| Weak hash algorithm used for contact ID | Security/Design | Original contact ID function | MD5 is not suitable for security-sensitive hashing. | Retained MD5 only for a short, non-security identifier and explicitly marked it as non-security use. |
