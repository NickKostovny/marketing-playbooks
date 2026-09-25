# Recipe: set a sensitive environment variable from a file

Why: a secret pasted into a chat, a terminal command, or a notes app is now in a history somewhere. And a text file exported from a notes app can carry a UTF-8 byte-order mark, which becomes the first three bytes of your stored secret. That happened here, and because sensitive values cannot be read back, it took a redeploy and a live 401 to find.

Vercel CLI shown. The shape holds for any host that reads a value from stdin.

## 1. Get the secret into a clean file without displaying it

Whoever holds the secret copies it to the clipboard, then:

```bash
pbpaste | tr -d '\r\n' > ~/Downloads/secret.txt
```

No echo, no cat, no editor.

## 2. Check the file, not the value

```bash
wc -c ~/Downloads/secret.txt
head -c 3 ~/Downloads/secret.txt | xxd
```

- The byte count should match the expected token length exactly.
- The first three bytes must not be `ef bb bf`. That is a BOM. If it is there, strip it: `tail -c +4 file > file2`.
- Check the shape without printing it, for example an Airtable personal access token is `pat`, 14 characters, a dot, 64 hex characters:

```bash
grep -cE '^pat[A-Za-z0-9]{14}\.[0-9a-f]{64}$' ~/Downloads/secret.txt
```

`1` means the shape is right.

## 3. Add it from inside the linked project folder

The CLI refuses outside a linked folder ("codebase isn't linked"). From the project root:

```bash
tr -d '\r\n' < ~/Downloads/secret.txt | vercel env add NAME production --sensitive --scope TEAM
```

Repeat for `preview` if previews need it. The interactive form of `vercel env add` stalls on the Sensitive prompt when stdin is not a terminal; passing `--sensitive` avoids the prompt.

## 4. Redeploy, then test live

Environment changes apply to the next deployment. `vercel redeploy <alias-or-url> --scope TEAM` rebuilds the current deployment with the new variables.

Sensitive variables come back empty from `vercel env pull`, so there is no local test. Test the flow on the redeployed preview or on production, then delete the test data.

## 5. Delete the file

```bash
rm ~/Downloads/secret.txt
```

If the value was wrong, remove the variable from every environment before adding it again. Two values for one name in one environment is a rejected add, not an overwrite.
