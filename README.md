# Momenti — поддержка и политика конфиденциальности

Статические страницы для App Store Connect:

- `index.html` — страница поддержки (Support URL)
- `privacy.html` — политика конфиденциальности (Privacy Policy URL)

`privacy.html` собирается из `../privacy-policy.md` скриптом `build.py`,
чтобы текст политики жил в одном месте вместе с остальными материалами стора:

```
python3 build.py workspace.kleiman@gmail.com
```
