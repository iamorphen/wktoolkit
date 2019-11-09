# Tampermonkey Scripts
Scripts in this directory are to be loaded by Tampermonkey and interact with the content on WaniKani.

These scripts are developed and tested on Google Chrome (v. 78+) for GNU/Linux.

# Format
Most if not all scripts in this directory use the following general format and conventions:

* `IDPrefix`: This const string acts as the script-unique prefix for things like local storage keys and HTML element classes and IDs.
* HTML, CSS, Classes, Functions: The utilities of the script.
* `Main()`: The runtime pseudo entry point of the script, written to show the general order of execution of the above utilities.

# Dependencies
* Modern Tampermonkey

# Local Development
To ease local development of these scripts:
1. Open a script in your editor of choice.
1. Cut the userscript header.
1. Add a script to Tampermonkey which will load your script from your local machine.
1. In your browser's extension properties, enable reading files from disk for Tampermonkey.
1. In your in-browser Tampermonkey script, paste the userscript header cut in an earlier step.
1. Add `// @require      file://<full_path_to_file_on_your_disk>` to the in-browser userscript header.

# Scripts
| Script | Use |
| ------ | --- |
| `context_sentence_blurrer` | Blurs the vocabulary context sentences in lessons. |
| `lesson_timer` | A configurable timer for measuring lesson duration. |
| `lesson_reorder` | [Incomplete.] Reorder subjects by type in lessons. |
