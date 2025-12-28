The short answer is **no, not directly.**  
Because "Google Code Wiki" is brand new (previewed late 2025\) and focused on a hosted web experience, it does **not** yet have a public API that lets you "export" or "pull" that auto-generated wiki into your own external database.  
Similarly, **NotebookLM** does not currently have an API for querying its "brain" from an external app (it is a closed UI).

### **The Solution: "Build Your Own" API (The Federated Brain)**

Since you cannot pull the "understanding" out of Google's closed tools, you must **generate the understanding yourself** inside your GitHub Actions. This gives you a file you *own* and can move anywhere programmatically.  
Here is how you replace "Google Code Wiki" with a workflow you can control via API.

### **Step 1: The "Self-Reflecting" GitHub Action**

Instead of waiting for Google to scan your code, you run a lightweight "summarizer" every time you push code. This creates a knowledge.md file that *is* your "Wiki API."  
**Tools needed:**

* **repomix** (CLI tool): Packs your code into one context file.  
* **llm** (CLI tool by Simon Willison) or a simple curl request: Sends that context to a cheap, smart model (like Gemini Flash or GPT-4o-mini) to summarize it.

**Create .github/workflows/generate-knowledge.yml in every repo:**  
`name: Generate Repo Knowledge`  
`on:`  
  `push:`  
    `branches: [ main ]`

`jobs:`  
  `summarize:`  
    `runs-on: ubuntu-latest`  
    `permissions:`  
      `contents: write # Needed to push the summary back to the repo`  
    `steps:`  
      `- uses: actions/checkout@v4`  
        
      `# 1. Install Tools`  
      `- name: Install Repomix`  
        `run: npm install -g repomix`

      `# 2. Pack the Code (creates repomix-output.xml)`  
      `# We ignore lockfiles and assets to keep it cheap`  
      `- name: Pack Repository`  
        `run: repomix --ignore "**/*.lock,**/*.svg,**/*.png" --output-show-line-numbers`

      `# 3. Generate "Wiki" Summary using Gemini Flash (Cheap & Fast)`  
      `- name: Generate Knowledge.md`  
        `env:`  
          `GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}`  
        `run: |`  
          `# Simple script to send packed code to LLM`  
          `curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$GEMINI_API_KEY" \`  
          `-H 'Content-Type: application/json' \`  
          `-d '{`  
            `"contents": [{`  
              `"parts":[{`  
                `"text": "You are a senior tech lead. Read this packed repository code. Output a purely technical summary named RESEARCH_NOTES.md. Include: 1. Core Architecture 2. Key Data Models 3. Authentication Flow 4. Recent Changes (inferred). Keep it under 1000 words. \n\n"`  
              `}]`  
            `}, {`  
              `"parts": [{ "text": "'$(cat repomix-output.xml | jq -sR .)'" }]`  
            `}]`  
          `}' > response.json`  
            
          `# Extract text from JSON (using jq) and save to file`  
          `cat response.json | jq -r '.candidates[0].content.parts[0].text' > RESEARCH_NOTES.md`

      `# 4. Push "RESEARCH_NOTES.md" to your Central Brain Repo`  
      `# (This is where you "grab" it programmatically)`  
      `- name: Dispatch to Central Brain`  
        `uses: dmnemec/copy_file_to_another_repo_action@v1.1.1`  
        `env:`  
          `API_TOKEN_GITHUB: ${{ secrets.PAT_TOKEN }}`  
        `with:`  
          `source_file: 'RESEARCH_NOTES.md'`  
          `destination_repo: 'your-username/my-central-brain'`  
          `destination_folder: 'knowledge/${{ github.repository }}'`  
          `user_email: 'bot@example.com'`  
          `user_name: 'Knowledge Bot'`  
          `commit_message: 'Update knowledge for ${{ github.repository }}'`

### **Step 2: How you "Access it via API"**

Now you don't need a Google Code Wiki API. You have a **Central Brain Repo** filled with RESEARCH\_NOTES.md files for every project you own.

* **To query it:** You can use the standard **GitHub API** to read these markdown files.  
* **To chat with it:** You can point a tool like **Cursor**, **Windsurf**, or a custom script at this one my-central-brain folder.

### **Why this is better than Google Code Wiki for you:**

1. **It is Universal:** Works for any language, private or public.  
2. **You Own the Data:** The "understanding" is a Markdown file, not a proprietary database.  
3. **It is Automatable:** You can change the prompt in Step 3 to ask for specifically what *you* care about (e.g., "Always list the API endpoints defined in this repo").

**Next Step:** I can write the specific repomix.config.json file for you to drop into your repos so this process ignores "noise" (like node\_modules or huge JSON files) and only "reads" the actual logic. Would you like that?