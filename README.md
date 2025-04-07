# 📚 Zotero Checker

**Zotero Checker** is a small utility that helps you keep your Zotero library in sync with a list of links or DOIs. It checks if every link in your list exists in your Zotero BibTeX export — and also finds:
- Extra entries in Zotero that aren’t in your link list
- Entries with missing metadata (title, author, year, etc.)
- Authors that are likely institutions (e.g. contain "University" or "College")

---

## 🔧 What You Need

1. A `.bib` file exported from your **Zotero collection** (see help below for more).
2. A `.txt` file that contains one **DOI or URL per line** (from your source list).

---

## 🖱 How to Use the Tool

1. Put your `ZoteroChecker.exe` in any folder.
2. Double-click to run it. A small window will open.
3. Click **Browse** and select your `.bib` file (Zotero export).
4. Click **Browse** and select your `.txt` file (list of links).
5. Click **Run Checker**.
6. The results will appear in the terminal and will be saved to:

```
zotero_check_result.txt
```

...in the same folder as your `.bib` file.

---

## 🔗 How to Get a List of Links (DOIs/URLs)

If you’re looking at a webpage that contains lots of DOIs or links to papers, here’s a quick way to extract them using your browser:

### ✅ Steps (in Chrome or Firefox):

1. Open the webpage that lists the papers.
2. Press `F12` or right-click and choose **Inspect** to open Developer Tools.
3. Go to the **Console** tab.
4. Paste and run this JavaScript code:
5. (You may need to enter "allow pasting" first)

```javascript
[...document.querySelectorAll('a')]
  .map(a => a.href)
  .filter(href => href.includes('doi.org') || href.includes('aisel.aisnet.org'))
  .forEach(link => console.log(link));
```

5. Copy the output and paste it into a plain text file.
6. Save the file as something like `links.txt`.

---

## 💡 What Kinds of Links Work?

- ✅ DOI links like: `https://doi.org/10.1057/jit.2014.30`
- ✅ Raw DOIs like: `10.1057/jit.2014.30`
- ✅ Conference URLs like: `https://aisel.aisnet.org/amcis2020/strategic_uses_it/12`

All of these are supported. You can mix them in the same file.

---

## 🧼 What the Tool Checks For

- 📄 Missing entries in Zotero
- 🗃 Extra entries in Zotero not listed in your links
- ⚠ Incomplete entries (missing title, authors, journal/book title, or year)
- 🏫 Suspect authors like `"University of X"` (often incorrectly listed as authors)

---

## 🗂 Output File

The result file `zotero_check_result.txt` contains 3 sections:

```
==== MISSING LINKS (in file, not in Zotero) ====
...

==== EXTRA ENTRIES (in Zotero, not in file) ====
...

==== INCOMPLETE METADATA ====
...
```

Use it to clean up your Zotero folder or your source list.

---

## 🆘 Need Help?

If something doesn't work:
- Make sure your `.bib` file is exported correctly from Zotero (right-click → Export Collection → BibTeX | Uncheck all checkboxes).
- Make sure each line in your `.txt` file contains **one or more links or DOIs**.
