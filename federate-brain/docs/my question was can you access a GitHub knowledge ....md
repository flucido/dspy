The short answer is **no**.  
As of late 2025, GitHub **does not** provide a public API to programmatically "push" or "upload" files into a Copilot Knowledge Base (or its replacement, "Copilot Spaces").  
Currently, adding context to GitHub's native knowledge base is strictly a **manual, UI-driven process**: you must log into the website, click "New Knowledge Base" (or Space), and manually select repositories or upload markdown files via their web interface. You cannot "curl" a file into it.  
This limitation is exactly why the **"Federated Brain"** strategy (the central repo of Markdown summaries) I described earlier is the better technical approach.

### **Why the "Federated Brain" is Superior for Automation**

Since you cannot push to GitHub's proprietary brain via API, you should build your own "Brain" using standard Git.

| Feature | GitHub Knowledge Base / Spaces | Your "Federated Brain" Repo |
| :---- | :---- | :---- |
| **Input Method** | Manual UI (Click & Select) | **Programmatic** (git push) |
| **API Access** | None (Closed System) | **Full Access** (via GitHub API) |
| **Data Format** | Hidden / Internal Index | **Markdown / XML** (Universal) |
| **Portability** | Locked to GitHub Copilot | **Portable** (Works with Cursor, Claude, etc.) |

### **The "API" is just Git**

Because your "Central Brain" is just a standard GitHub repository, you already have the API you need.  
To "programmatically grab" your latest research notes and put them into your knowledge base, you don't need a special AI endpoint. You just use the standard Git commands in your workflow:  
`# This IS your "Knowledge Base API"`  
`git add context.xml`  
`git commit -m "Update knowledge for Repo A"`  
`git push origin main`

### **The "Advanced" Alternative: MCP (Model Context Protocol)**

If you really want to avoid copying files and want Copilot to "read" your data programmatically, the only official path is to build a **Model Context Protocol (MCP) Server**.

* **What it is:** A lightweight server you write (in Python/Node) that connects to your data.  
* **How it works:** Instead of "pushing" data to Copilot, Copilot "asks" your server for data when it needs it.  
* **Why avoid it for now:** It requires running a live server and is much more complex than simply pushing a Markdown file to a repo.

### **Summary Recommendation**

Stick to the **Central Repository** method. It gives you a tangible "Knowledge Base" that is:

1. **Readable** by humans.  
2. **Writable** by your CI/CD pipelines (via Git).  
3. **Future-proof** (you can feed these Markdown files into *any* future AI tool, not just GitHub Copilot).

### **Next Step**

Since you are interested in the programmable extraction, would you like the **repomix.config.json** file that filters out lockfiles and assets? This ensures your programmatic "grab" stays lightweight and cheap.  
[How to Use GitHub Copilot Knowledge Bases](https://www.youtube.com/watch?v=GsGmSequ8Eg) *This video demonstrates the manual, UI-focused nature of creating Knowledge Bases, highlighting why an API-based "Do It Yourself" approach is necessary for automation.*