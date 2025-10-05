# Phase 0-3: Foundation (Detailed Implementation Guide)

**Total Duration**: 10-16 days (~2-3 weeks)
**Prerequisite Knowledge**: Basic understanding of HTTP APIs, familiarity with Python (for comparison)
**Goal**: Establish a solid, tested foundation for the Rust Aeries API with project setup, data models, error handling, and configuration management

---

## Table of Contents

1. [Phase 0: Preparation & Environment Setup](#phase-0-preparation--environment-setup)
2. [Phase 1: Core Data Models](#phase-1-core-data-models)
3. [Phase 2: Error Handling Foundation](#phase-2-error-handling-foundation)
4. [Phase 3: Configuration Management](#phase-3-configuration-management)
5. [Foundation Validation Checklist](#foundation-validation-checklist)

---

# Phase 0: Preparation & Environment Setup

**Duration**: 3-5 days
**Goal**: Install Rust, set up the project structure, and validate the development environment

## Day 1: Install Rust and Essential Tools

### Step 1.1: Install Rust via rustup

```bash
# Install rustup (Rust toolchain installer)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Follow prompts, select default installation

# Add to PATH (or restart terminal)
source $HOME/.cargo/env

# Verify installation
rustc --version  # Should show: rustc 1.75.0 (or newer)
cargo --version  # Should show: cargo 1.75.0 (or newer)
```

**Expected Output**:
```
rustc 1.75.0 (82e1608df 2023-12-21)
cargo 1.75.0 (1d8b05cdd 2023-11-20)
```

**Troubleshooting**:
- If `rustc` not found: Restart terminal or manually add `~/.cargo/bin` to PATH
- Windows users: Download from https://rustup.rs and use the installer
- macOS users: May need Xcode Command Line Tools: `xcode-select --install`

### Step 1.2: Install Essential Development Tools

```bash
# Install cargo-watch (auto-recompile on file changes)
cargo install cargo-watch

# Install cargo-edit (for adding dependencies easily)
cargo install cargo-edit

# Install clippy (Rust linter - usually included)
rustup component add clippy

# Install rustfmt (code formatter)
rustup component add rustfmt

# Verify installations
cargo watch --version
cargo clippy --version
cargo fmt --version
```

**What each tool does**:
- **cargo-watch**: Automatically rebuilds on file changes (like Python's `flask run --reload`)
- **cargo-edit**: Adds `cargo add` command for easy dependency management
- **clippy**: Linter that catches common mistakes and suggests improvements
- **rustfmt**: Formats code according to Rust conventions

### Step 1.3: Set Up IDE/Editor

**Recommended: Visual Studio Code**

```bash
# Install VS Code extensions
code --install-extension rust-lang.rust-analyzer
code --install-extension vadimcn.vscode-lldb  # Debugger
code --install-extension serayuzgur.crates    # Cargo.toml helper
```

**VS Code Settings** (`.vscode/settings.json`):
```json
{
    "rust-analyzer.checkOnSave.command": "clippy",
    "rust-analyzer.cargo.features": "all",
    "editor.formatOnSave": true,
    "[rust]": {
        "editor.defaultFormatter": "rust-lang.rust-analyzer"
    }
}
```

**Alternative IDEs**:
- **IntelliJ IDEA**: Install Rust plugin
- **Vim/Neovim**: Use rust.vim + coc-rust-analyzer
- **Emacs**: Use rustic or rust-mode

### Step 1.4: Learn Basic Cargo Commands

```bash
# Create a new project
cargo new my-project

# Build the project
cargo build           # Debug build (fast compile, slow runtime)
cargo build --release # Release build (slow compile, fast runtime)

# Run the project
cargo run             # Build + run

# Run tests
cargo test

# Check code without building
cargo check           # Fast syntax/type checking

# Format code
cargo fmt

# Run linter
cargo clippy

# Clean build artifacts
cargo clean
```

**Pro Tips**:
- Use `cargo check` while developing (faster than `build`)
- Use `cargo clippy` before committing
- Release builds are ~10-50x faster than debug builds

---

## Day 2: Create Project Structure

### Step 2.1: Initialize the Project

```bash
# Navigate to your projects directory
cd ~/projects/rust/ariesapi

# Create new library project (allows both lib and binary targets)
cargo new --lib aeries-api-rust

cd aeries-api-rust

# Verify structure
tree -L 2
```

**Expected Structure**:
```
aeries-api-rust/
├── Cargo.toml
├── src/
│   └── lib.rs
└── .git/
```

### Step 2.2: Configure Cargo.toml

Replace the default `Cargo.toml` with:

```toml
[package]
name = "aeries-api-rust"
version = "0.1.0"
edition = "2021"  # Use Rust 2021 edition (latest stable)
authors = ["Your Name <your.email@example.com>"]
description = "Rust backend API for Aeries student information system"
license = "MIT OR Apache-2.0"

# Binary target (the server)
[[bin]]
name = "aeries-server"
path = "src/main.rs"

# Optional: CLI tool binary
[[bin]]
name = "aeries-cli"
path = "src/bin/cli.rs"
required-features = ["cli"]

[dependencies]
# HTTP Server
axum = "0.7"
tokio = { version = "1.35", features = ["full"] }
tower = "0.4"
tower-http = { version = "0.5", features = ["trace", "cors"] }

# HTTP Client
reqwest = { version = "0.11", features = ["json", "native-tls"] }

# Serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

# Error Handling
anyhow = "1.0"
thiserror = "1.0"

# Configuration
dotenvy = "0.15"

# Logging & Tracing
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter", "json"] }

# Optional: CLI features
clap = { version = "4.5", features = ["derive"], optional = true }

[dev-dependencies]
# Testing
wiremock = "0.6"
tokio-test = "0.4"
tempfile = "3.8"  # For testing file operations

[features]
default = []
cli = ["clap"]

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
```

**Cargo.toml Explained**:
- **`[package]`**: Metadata about your crate
- **`[[bin]]`**: Defines binary executables (vs library crates)
- **`[dependencies]`**: Runtime dependencies
- **`[dev-dependencies]`**: Dependencies only for tests/benchmarks
- **`[features]`**: Optional functionality (e.g., CLI tool)
- **`[profile.release]`**: Optimization settings

### Step 2.3: Create Directory Structure

```bash
# Create all directories
mkdir -p src/{models,clients,services,export,handlers}
mkdir -p src/bin
mkdir -p tests/{common,fixtures}
mkdir -p .vscode

# Create initial files
touch src/main.rs
touch src/lib.rs
touch src/error.rs
touch src/config.rs
touch src/models/mod.rs
touch src/clients/mod.rs
touch src/services/mod.rs
touch src/export/mod.rs
touch src/handlers/mod.rs
touch src/routes.rs
touch tests/common/mod.rs

# Create configuration files
touch .env
touch .env.example
touch .gitignore
```

**Full Structure**:
```
aeries-api-rust/
├── Cargo.toml
├── Cargo.lock              # Generated after first build
├── .env                    # Local config (not committed)
├── .env.example            # Template (committed)
├── .gitignore
├── README.md
├── .vscode/
│   └── settings.json
├── src/
│   ├── main.rs             # Server entry point
│   ├── lib.rs              # Library root (re-exports)
│   ├── error.rs            # Error types
│   ├── config.rs           # Configuration management
│   ├── routes.rs           # Route definitions
│   ├── models/             # Domain models
│   │   ├── mod.rs
│   │   ├── student.rs
│   │   ├── school.rs
│   │   └── report.rs
│   ├── clients/            # External API clients
│   │   ├── mod.rs
│   │   └── aeries.rs
│   ├── services/           # Business logic
│   │   ├── mod.rs
│   │   ├── students.rs
│   │   ├── schools.rs
│   │   └── reports.rs
│   ├── export/             # Export functionality
│   │   ├── mod.rs
│   │   ├── csv.rs
│   │   ├── excel.rs
│   │   └── pdf.rs
│   ├── handlers/           # HTTP handlers
│   │   ├── mod.rs
│   │   ├── students.rs
│   │   ├── schools.rs
│   │   └── reports.rs
│   └── bin/
│       └── cli.rs          # CLI tool entry point
└── tests/
    ├── common/
    │   └── mod.rs          # Shared test utilities
    ├── fixtures/           # Test data
    └── api_tests.rs        # Integration tests
```

### Step 2.4: Configure .gitignore

Create `.gitignore`:

```gitignore
# Rust
/target/
**/*.rs.bk
*.pdb
Cargo.lock  # Uncomment for libraries, keep for binaries

# Environment
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Test outputs
test_output/
```

### Step 2.5: Create Environment Configuration

**`.env.example`** (commit this):
```bash
# Aeries API Configuration
AERIES_BASE_URL=https://your-aeries-instance.com
AERIES_CERT_PATH=/path/to/certificate.pem
AERIES_KEY_PATH=/path/to/private-key.pem

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=3000

# Logging
RUST_LOG=info,aeries_api_rust=debug
```

**`.env`** (local only, not committed):
```bash
# Copy from .env.example and fill in actual values
AERIES_BASE_URL=https://millercreeksd.aeries.net/admin/api/v5
AERIES_CERT_PATH=./certs/client-cert.pem
AERIES_KEY_PATH=./certs/client-key.pem
SERVER_HOST=127.0.0.1
SERVER_PORT=3000
RUST_LOG=debug
```

---

## Day 3: Set Up Logging and Basic Structure

### Step 3.1: Initialize Library Root (`src/lib.rs`)

```rust
//! Aeries API Rust Backend
//!
//! This crate provides a modern, performant API for interacting with the
//! Aeries student information system.

// Module declarations
pub mod config;
pub mod error;
pub mod models;
pub mod clients;
pub mod services;
pub mod export;
pub mod handlers;
pub mod routes;

// Re-exports for convenience
pub use error::{AppError, Result};
pub use config::Config;
```

**What this does**:
- Declares all modules (tells Rust these directories exist)
- Re-exports commonly used types (ergonomics)
- Documentation comments (`//!`) for crate-level docs

### Step 3.2: Set Up Main Entry Point (`src/main.rs`)

```rust
//! Aeries API Server
//!
//! Main entry point for the HTTP server.

use aeries_api_rust::{Config, routes};
use std::sync::Arc;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize logging
    init_logging();

    tracing::info!("Starting Aeries API server...");

    // Load configuration
    let config = Config::from_env()?;
    tracing::info!("Configuration loaded successfully");
    tracing::debug!("Server will listen on {}:{}", config.server_host, config.server_port);

    // Build the application router
    // Note: We'll implement this in later phases
    let app = routes::create_placeholder_router();

    // Start the server
    let addr = format!("{}:{}", config.server_host, config.server_port);
    let listener = tokio::net::TcpListener::bind(&addr).await?;

    tracing::info!("Server listening on {}", addr);
    tracing::info!("Press Ctrl+C to stop");

    axum::serve(listener, app).await?;

    Ok(())
}

fn init_logging() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info,aeries_api_rust=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();
}
```

**Logging Explained**:
- `tracing`: Structured, async-aware logging framework
- `EnvFilter`: Reads from `RUST_LOG` environment variable
- Format: `level,crate::module=level`
  - `info`: Show info level for all crates
  - `aeries_api_rust=debug`: Show debug level for our crate

### Step 3.3: Create Placeholder Router (`src/routes.rs`)

```rust
use axum::{routing::get, Router};

/// Creates the application router
///
/// This is a placeholder that will be expanded in Phase 5
pub fn create_placeholder_router() -> Router {
    Router::new()
        .route("/health", get(health_check))
}

async fn health_check() -> &'static str {
    "OK"
}
```

### Step 3.4: Initialize Module Files

**`src/models/mod.rs`**:
```rust
// Module declarations - will be implemented in Phase 1
// pub mod student;
// pub mod school;
// pub mod report;

// Re-exports
// pub use student::Student;
// pub use school::School;
// pub use report::Report;
```

**`src/clients/mod.rs`**:
```rust
// Will be implemented in Phase 4
// pub mod aeries;
```

**`src/services/mod.rs`**:
```rust
// Will be implemented in Phase 5
// pub mod students;
// pub mod schools;
// pub mod reports;
```

**`src/export/mod.rs`**:
```rust
// Will be implemented in Phases 6-8
// pub mod csv;
// pub mod excel;
// pub mod pdf;
```

**`src/handlers/mod.rs`**:
```rust
// Will be implemented in Phase 5
// pub mod students;
// pub mod schools;
// pub mod reports;
```

---

## Day 4: Implement and Test Basic Server

### Step 4.1: Build the Project

```bash
# Check for errors without building
cargo check

# Build in debug mode
cargo build

# Expected output:
#    Compiling aeries-api-rust v0.1.0 (/path/to/project)
#     Finished dev [unoptimized + debuginfo] target(s) in 45.23s
```

**If you see errors**:
1. Read the error message carefully (Rust errors are very helpful)
2. Check for typos in module names
3. Ensure all files are saved
4. Run `cargo clean` and try again

### Step 4.2: Run the Server

```bash
# Terminal 1: Run the server
cargo run

# Expected output:
# 2024-01-15T10:30:00.123456Z  INFO aeries_api_rust: Starting Aeries API server...
# 2024-01-15T10:30:00.234567Z  INFO aeries_api_rust: Configuration loaded successfully
# 2024-01-15T10:30:00.345678Z DEBUG aeries_api_rust: Server will listen on 127.0.0.1:3000
# 2024-01-15T10:30:00.456789Z  INFO aeries_api_rust: Server listening on 127.0.0.1:3000
```

**If server fails to start**:
- Check if port 3000 is already in use: `lsof -i :3000`
- Verify `.env` file exists and has valid values
- Check file paths for certificates (they don't need to exist yet for this step)

### Step 4.3: Test the Health Endpoint

```bash
# Terminal 2: Test with curl
curl http://localhost:3000/health

# Expected output:
# OK

# Test with httpie (more readable)
http GET localhost:3000/health

# Test with Postman
# GET http://localhost:3000/health
```

### Step 4.4: Set Up Auto-Reload for Development

```bash
# Install cargo-watch if not already installed
cargo install cargo-watch

# Run with auto-reload
cargo watch -x run

# Or with clear screen on reload
cargo watch -c -x run
```

**Cargo Watch Tips**:
- Watches all `.rs` files in `src/`
- Automatically rebuilds and restarts on file changes
- Use `-c` flag to clear screen on each rebuild
- Use `-x check` for faster feedback during development

---

## Day 5: Documentation and Phase 0 Completion

### Step 5.1: Write README.md

Create `README.md`:

```markdown
# Aeries API - Rust Backend

A modern, performant Rust backend for the Aeries student information system API.

## Features

- 🚀 High-performance async HTTP server (Axum)
- 🔒 Certificate-based authentication
- 📊 Data export to CSV, Excel, and PDF formats
- ✅ Comprehensive test coverage
- 📝 Structured logging with tracing

## Prerequisites

- Rust 1.75 or newer
- Access to Aeries API with valid certificates

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd aeries-api-rust
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Aeries credentials
   ```

3. **Build and run**
   ```bash
   cargo run
   ```

4. **Test the health endpoint**
   ```bash
   curl http://localhost:3000/health
   ```

## Development

### Build Commands

```bash
# Development build (fast compile, slow runtime)
cargo build

# Production build (slow compile, fast runtime)
cargo build --release

# Run tests
cargo test

# Run with auto-reload
cargo watch -x run

# Format code
cargo fmt

# Run linter
cargo clippy
```

### Project Structure

```
src/
├── main.rs          # Server entry point
├── lib.rs           # Library root
├── config.rs        # Configuration management
├── error.rs         # Error types
├── models/          # Domain models
├── clients/         # External API clients
├── services/        # Business logic
├── handlers/        # HTTP request handlers
├── export/          # Export functionality
└── routes.rs        # Route definitions
```

## Configuration

Environment variables (set in `.env`):

- `AERIES_BASE_URL`: Aeries API base URL
- `AERIES_CERT_PATH`: Path to client certificate (.pem)
- `AERIES_KEY_PATH`: Path to private key (.pem)
- `SERVER_HOST`: Server bind address (default: 0.0.0.0)
- `SERVER_PORT`: Server port (default: 3000)
- `RUST_LOG`: Log level (default: info)

## Testing

```bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_name
```

## License

MIT OR Apache-2.0
```

### Step 5.2: Generate Documentation

```bash
# Generate and open documentation in browser
cargo doc --open

# Generate docs without dependencies
cargo doc --no-deps --open
```

**Documentation Tips**:
- Use `///` for item documentation
- Use `//!` for module/crate documentation
- Documentation supports Markdown
- Code examples in docs are tested with `cargo test`

### Step 5.3: Run Code Quality Checks

```bash
# Format all code
cargo fmt

# Run linter
cargo clippy

# Run with pedantic lints (very strict)
cargo clippy -- -W clippy::pedantic

# Fix auto-fixable issues
cargo clippy --fix
```

### Step 5.4: Create Initial Git Commit

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Phase 0: Initial project setup

- Configure Cargo.toml with dependencies
- Set up project structure
- Implement basic server with health check
- Configure logging with tracing
- Add documentation and README"
```

---

## Phase 0 Validation Checklist

Before proceeding to Phase 1, verify:

- [ ] `cargo --version` shows Rust 1.75+
- [ ] `cargo build` compiles without errors
- [ ] `cargo run` starts the server
- [ ] `curl http://localhost:3000/health` returns "OK"
- [ ] `cargo test` runs (even if no tests yet)
- [ ] `cargo clippy` shows no warnings
- [ ] `cargo fmt` has formatted all code
- [ ] `.env` file configured with your credentials
- [ ] IDE/editor has Rust language support
- [ ] Git repository initialized with first commit

**Troubleshooting Common Issues**:

| Issue | Solution |
|-------|----------|
| "cargo: command not found" | Restart terminal or `source ~/.cargo/env` |
| Port already in use | Change `SERVER_PORT` in `.env` |
| TLS/certificate errors | Verify paths in `.env`, ensure files exist |
| Slow compile times | This is normal; use `cargo check` for feedback |
| "edition 2021 not found" | Update Rust: `rustup update` |

---

# Phase 1: Core Data Models

**Duration**: 3-5 days
**Goal**: Implement Student, School, and Report models with full serialization support

## Day 6: Student Model Implementation

### Step 1.1: Understand the Python Model

**Python Version** (`src/models/student.py`):
```python
@dataclass
class Student:
    id: int
    name: str
    grade: str
    school_id: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {...}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        return cls(...)
```

**Key Observations**:
- Mix of required and optional fields
- Integer and string types
- Serialization to/from dictionaries (for JSON)

### Step 1.2: Create Student Model in Rust

**`src/models/student.rs`**:

```rust
use serde::{Deserialize, Serialize};

/// Represents a student in the Aeries system
///
/// # Fields
///
/// * `id` - Unique student identifier
/// * `name` - Full name of the student
/// * `grade` - Grade level (e.g., "9", "10", "11", "12")
/// * `school_id` - Optional school identifier
/// * `email` - Optional student email address
/// * `phone` - Optional student phone number
///
/// # Examples
///
/// ```
/// use aeries_api_rust::models::Student;
///
/// let student = Student::new(12345, "Jane Doe".to_string(), "10".to_string());
/// assert_eq!(student.id, 12345);
/// ```
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Student {
    pub id: i64,
    pub name: String,
    pub grade: String,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub school_id: Option<i64>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub email: Option<String>,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub phone: Option<String>,
}

impl Student {
    /// Creates a new Student with only required fields
    ///
    /// # Arguments
    ///
    /// * `id` - Unique student identifier
    /// * `name` - Full name
    /// * `grade` - Grade level
    ///
    /// # Examples
    ///
    /// ```
    /// # use aeries_api_rust::models::Student;
    /// let student = Student::new(1, "John Doe".to_string(), "9".to_string());
    /// ```
    pub fn new(id: i64, name: String, grade: String) -> Self {
        Self {
            id,
            name,
            grade,
            school_id: None,
            email: None,
            phone: None,
        }
    }

    /// Creates a new Student with all fields
    pub fn with_details(
        id: i64,
        name: String,
        grade: String,
        school_id: Option<i64>,
        email: Option<String>,
        phone: Option<String>,
    ) -> Self {
        Self {
            id,
            name,
            grade,
            school_id,
            email,
            phone,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_student_new() {
        let student = Student::new(1, "Jane Doe".to_string(), "11".to_string());
        assert_eq!(student.id, 1);
        assert_eq!(student.name, "Jane Doe");
        assert_eq!(student.grade, "11");
        assert_eq!(student.school_id, None);
        assert_eq!(student.email, None);
        assert_eq!(student.phone, None);
    }

    #[test]
    fn test_student_with_details() {
        let student = Student::with_details(
            2,
            "John Smith".to_string(),
            "12".to_string(),
            Some(100),
            Some("john@example.com".to_string()),
            Some("555-1234".to_string()),
        );

        assert_eq!(student.id, 2);
        assert_eq!(student.school_id, Some(100));
        assert_eq!(student.email, Some("john@example.com".to_string()));
    }

    #[test]
    fn test_student_serialization() {
        let student = Student::new(1, "Jane Doe".to_string(), "10".to_string());
        let json = serde_json::to_string(&student).unwrap();

        // Verify JSON contains required fields
        assert!(json.contains("\"id\":1"));
        assert!(json.contains("\"name\":\"Jane Doe\""));
        assert!(json.contains("\"grade\":\"10\""));

        // Verify optional fields are excluded when None
        assert!(!json.contains("school_id"));
        assert!(!json.contains("email"));
        assert!(!json.contains("phone"));
    }

    #[test]
    fn test_student_serialization_with_optionals() {
        let student = Student::with_details(
            2,
            "John".to_string(),
            "11".to_string(),
            Some(50),
            Some("test@test.com".to_string()),
            None,
        );

        let json = serde_json::to_string(&student).unwrap();

        // Verify optional fields included when Some
        assert!(json.contains("\"school_id\":50"));
        assert!(json.contains("\"email\":\"test@test.com\""));

        // Verify None fields excluded
        assert!(!json.contains("phone"));
    }

    #[test]
    fn test_student_deserialization() {
        let json = r#"{
            "id": 1,
            "name": "Jane Doe",
            "grade": "10"
        }"#;

        let student: Student = serde_json::from_str(json).unwrap();

        assert_eq!(student.id, 1);
        assert_eq!(student.name, "Jane Doe");
        assert_eq!(student.grade, "10");
        assert_eq!(student.school_id, None);
    }

    #[test]
    fn test_student_deserialization_with_optionals() {
        let json = r#"{
            "id": 2,
            "name": "John Smith",
            "grade": "12",
            "school_id": 100,
            "email": "john@example.com",
            "phone": "555-1234"
        }"#;

        let student: Student = serde_json::from_str(json).unwrap();

        assert_eq!(student.id, 2);
        assert_eq!(student.school_id, Some(100));
        assert_eq!(student.email, Some("john@example.com".to_string()));
        assert_eq!(student.phone, Some("555-1234".to_string()));
    }

    #[test]
    fn test_student_roundtrip() {
        let original = Student::with_details(
            99,
            "Test Student".to_string(),
            "9".to_string(),
            Some(42),
            Some("test@school.edu".to_string()),
            Some("555-9999".to_string()),
        );

        // Serialize to JSON
        let json = serde_json::to_string(&original).unwrap();

        // Deserialize back
        let deserialized: Student = serde_json::from_str(&json).unwrap();

        // Verify they match
        assert_eq!(original, deserialized);
    }

    #[test]
    fn test_student_clone() {
        let student = Student::new(1, "Clone Test".to_string(), "10".to_string());
        let cloned = student.clone();

        assert_eq!(student, cloned);
    }

    #[test]
    fn test_student_debug() {
        let student = Student::new(1, "Debug Test".to_string(), "11".to_string());
        let debug_str = format!("{:?}", student);

        assert!(debug_str.contains("Student"));
        assert!(debug_str.contains("id: 1"));
        assert!(debug_str.contains("Debug Test"));
    }
}
```

**Code Explanations**:

1. **Derives**:
   - `Debug`: Enables `{:?}` formatting for debugging
   - `Clone`: Allows creating copies
   - `PartialEq, Eq`: Enables equality comparisons
   - `Serialize, Deserialize`: Automatic JSON conversion via serde

2. **`#[serde(skip_serializing_if = "Option::is_none")]`**:
   - Excludes `None` values from JSON (matches Python behavior)
   - Results in cleaner JSON output

3. **Types**:
   - `i64` instead of `int`: Rust requires explicit integer sizes
   - `String` instead of `str`: Owned string data
   - `Option<T>`: Rust's way of expressing nullable values

### Step 1.3: Run Tests

```bash
# Run all tests
cargo test

# Run only student tests
cargo test student

# Run with output visible
cargo test student -- --nocapture

# Expected output:
# running 10 tests
# test models::student::tests::test_student_clone ... ok
# test models::student::tests::test_student_debug ... ok
# test models::student::tests::test_student_deserialization ... ok
# ...
# test result: ok. 10 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
```

---

## Day 7: School and Report Models

### Step 2.1: Implement School Model

**`src/models/school.rs`**:

```rust
use serde::{Deserialize, Serialize};

/// Represents a school in the Aeries system
///
/// # Examples
///
/// ```
/// use aeries_api_rust::models::School;
///
/// let school = School::new(
///     100,
///     "Miller Creek Middle School".to_string(),
///     "123 School Lane, Anytown, CA 12345".to_string(),
/// );
/// ```
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct School {
    pub id: i64,
    pub name: String,
    pub address: String,

    #[serde(skip_serializing_if = "Option::is_none")]
    pub phone: Option<String>,
}

impl School {
    /// Creates a new School
    pub fn new(id: i64, name: String, address: String) -> Self {
        Self {
            id,
            name,
            address,
            phone: None,
        }
    }

    /// Creates a new School with phone number
    pub fn with_phone(id: i64, name: String, address: String, phone: String) -> Self {
        Self {
            id,
            name,
            address,
            phone: Some(phone),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_school_new() {
        let school = School::new(
            1,
            "Test School".to_string(),
            "123 Main St".to_string(),
        );

        assert_eq!(school.id, 1);
        assert_eq!(school.name, "Test School");
        assert_eq!(school.address, "123 Main St");
        assert_eq!(school.phone, None);
    }

    #[test]
    fn test_school_with_phone() {
        let school = School::with_phone(
            2,
            "Phone School".to_string(),
            "456 Oak Ave".to_string(),
            "555-1234".to_string(),
        );

        assert_eq!(school.phone, Some("555-1234".to_string()));
    }

    #[test]
    fn test_school_serialization() {
        let school = School::new(
            100,
            "Serialize School".to_string(),
            "789 Pine Rd".to_string(),
        );

        let json = serde_json::to_string(&school).unwrap();

        assert!(json.contains("\"id\":100"));
        assert!(json.contains("\"name\":\"Serialize School\""));
        assert!(json.contains("\"address\":\"789 Pine Rd\""));
        assert!(!json.contains("phone")); // Should be excluded
    }

    #[test]
    fn test_school_deserialization() {
        let json = r#"{
            "id": 200,
            "name": "Deserialize School",
            "address": "321 Elm St",
            "phone": "555-9999"
        }"#;

        let school: School = serde_json::from_str(json).unwrap();

        assert_eq!(school.id, 200);
        assert_eq!(school.name, "Deserialize School");
        assert_eq!(school.phone, Some("555-9999".to_string()));
    }

    #[test]
    fn test_school_roundtrip() {
        let original = School::with_phone(
            300,
            "Roundtrip School".to_string(),
            "999 Test Ave".to_string(),
            "555-0000".to_string(),
        );

        let json = serde_json::to_string(&original).unwrap();
        let deserialized: School = serde_json::from_str(&json).unwrap();

        assert_eq!(original, deserialized);
    }
}
```

### Step 2.2: Implement Report Model

**`src/models/report.rs`**:

```rust
use serde::{Deserialize, Serialize};

/// Represents a report in the Aeries system
///
/// # Examples
///
/// ```
/// use aeries_api_rust::models::Report;
///
/// let report = Report::new(
///     1,
///     "Attendance Summary".to_string(),
///     "Monthly attendance report".to_string(),
///     "summary".to_string(),
/// );
/// ```
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Report {
    pub id: i64,
    pub name: String,
    pub description: String,

    /// The type of report (e.g., "summary", "detailed")
    ///
    /// Note: `type` is a keyword in Rust, so we use `report_type`
    /// but serialize it as "type" to match the API
    #[serde(rename = "type")]
    pub report_type: String,
}

impl Report {
    /// Creates a new Report
    pub fn new(id: i64, name: String, description: String, report_type: String) -> Self {
        Self {
            id,
            name,
            description,
            report_type,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_report_new() {
        let report = Report::new(
            1,
            "Test Report".to_string(),
            "A test report".to_string(),
            "summary".to_string(),
        );

        assert_eq!(report.id, 1);
        assert_eq!(report.name, "Test Report");
        assert_eq!(report.description, "A test report");
        assert_eq!(report.report_type, "summary");
    }

    #[test]
    fn test_report_serialization() {
        let report = Report::new(
            100,
            "Serialize Report".to_string(),
            "Testing serialization".to_string(),
            "detailed".to_string(),
        );

        let json = serde_json::to_string(&report).unwrap();

        assert!(json.contains("\"id\":100"));
        assert!(json.contains("\"name\":\"Serialize Report\""));
        assert!(json.contains("\"type\":\"detailed\"")); // Note: "type", not "report_type"
    }

    #[test]
    fn test_report_deserialization() {
        let json = r#"{
            "id": 200,
            "name": "Deserialize Report",
            "description": "Testing deserialization",
            "type": "summary"
        }"#;

        let report: Report = serde_json::from_str(json).unwrap();

        assert_eq!(report.id, 200);
        assert_eq!(report.name, "Deserialize Report");
        assert_eq!(report.report_type, "summary");
    }

    #[test]
    fn test_report_roundtrip() {
        let original = Report::new(
            300,
            "Roundtrip Report".to_string(),
            "Full cycle test".to_string(),
            "comprehensive".to_string(),
        );

        let json = serde_json::to_string(&original).unwrap();
        let deserialized: Report = serde_json::from_str(&json).unwrap();

        assert_eq!(original, deserialized);
    }

    #[test]
    fn test_report_type_rename() {
        // Verify that `report_type` field is serialized as "type"
        let report = Report::new(
            1,
            "Type Test".to_string(),
            "Testing rename".to_string(),
            "test".to_string(),
        );

        let json = serde_json::to_value(&report).unwrap();
        let type_value = json.get("type").expect("'type' field should exist");

        assert_eq!(type_value, "test");

        // Verify "report_type" doesn't exist in JSON
        assert!(json.get("report_type").is_none());
    }
}
```

**Key Concept - `#[serde(rename = "type")]`**:
- `type` is a reserved keyword in Rust
- We use `report_type` in Rust code
- Serde renames it to `type` in JSON
- This maintains API compatibility with Python version

### Step 2.3: Update models/mod.rs

**`src/models/mod.rs`**:

```rust
//! Data models for the Aeries API
//!
//! This module contains all domain models used throughout the application.

pub mod student;
pub mod school;
pub mod report;

// Re-export for convenience
pub use student::Student;
pub use school::School;
pub use report::Report;
```

### Step 2.4: Update lib.rs

Add models to the public API in **`src/lib.rs`**:

```rust
//! Aeries API Rust Backend
//!
//! # Examples
//!
//! ```no_run
//! use aeries_api_rust::{Config, models::Student};
//!
//! # fn main() -> anyhow::Result<()> {
//! let config = Config::from_env()?;
//! let student = Student::new(1, "Jane Doe".to_string(), "10".to_string());
//! # Ok(())
//! # }
//! ```

pub mod config;
pub mod error;
pub mod models;
pub mod clients;
pub mod services;
pub mod export;
pub mod handlers;
pub mod routes;

// Re-exports
pub use error::{AppError, Result};
pub use config::Config;
```

### Step 2.5: Run All Model Tests

```bash
# Run all model tests
cargo test models

# Expected output:
# running 25 tests (approx)
# test models::report::tests::test_report_deserialization ... ok
# test models::report::tests::test_report_new ... ok
# test models::report::tests::test_report_roundtrip ... ok
# test models::report::tests::test_report_serialization ... ok
# test models::report::tests::test_report_type_rename ... ok
# test models::school::tests::test_school_deserialization ... ok
# test models::school::tests::test_school_new ... ok
# test models::school::tests::test_school_roundtrip ... ok
# test models::school::tests::test_school_serialization ... ok
# test models::school::tests::test_school_with_phone ... ok
# test models::student::tests::test_student_clone ... ok
# test models::student::tests::test_student_debug ... ok
# test models::student::tests::test_student_deserialization ... ok
# test models::student::tests::test_student_deserialization_with_optionals ... ok
# test models::student::tests::test_student_new ... ok
# test models::student::tests::test_student_roundtrip ... ok
# test models::student::tests::test_student_serialization ... ok
# test models::student::tests::test_student_serialization_with_optionals ... ok
# test models::student::tests::test_student_with_details ... ok
#
# test result: ok. 19 passed; 0 failed

# Check code quality
cargo clippy

# Format code
cargo fmt
```

---

## Day 8: Model Integration Tests

### Step 3.1: Create Integration Test File

**`tests/model_integration_tests.rs`**:

```rust
//! Integration tests for data models
//!
//! These tests verify cross-model behavior and JSON compatibility

use aeries_api_rust::models::{Student, School, Report};
use serde_json;

#[test]
fn test_all_models_serialize_to_valid_json() {
    let student = Student::new(1, "Test Student".to_string(), "10".to_string());
    let school = School::new(100, "Test School".to_string(), "123 Main".to_string());
    let report = Report::new(1000, "Test Report".to_string(), "Description".to_string(), "summary".to_string());

    // All should serialize without panic
    assert!(serde_json::to_string(&student).is_ok());
    assert!(serde_json::to_string(&school).is_ok());
    assert!(serde_json::to_string(&report).is_ok());
}

#[test]
fn test_models_serialize_to_json_array() {
    let students = vec![
        Student::new(1, "Student 1".to_string(), "9".to_string()),
        Student::new(2, "Student 2".to_string(), "10".to_string()),
        Student::new(3, "Student 3".to_string(), "11".to_string()),
    ];

    let json = serde_json::to_string(&students).unwrap();

    // Verify it's a JSON array
    assert!(json.starts_with('['));
    assert!(json.ends_with(']'));

    // Verify it contains all students
    assert!(json.contains("Student 1"));
    assert!(json.contains("Student 2"));
    assert!(json.contains("Student 3"));
}

#[test]
fn test_models_deserialize_from_api_response() {
    // Simulate API response format
    let api_response = r#"[
        {
            "id": 1,
            "name": "Jane Doe",
            "grade": "10",
            "school_id": 100,
            "email": "jane@school.edu"
        },
        {
            "id": 2,
            "name": "John Smith",
            "grade": "11"
        }
    ]"#;

    let students: Vec<Student> = serde_json::from_str(api_response).unwrap();

    assert_eq!(students.len(), 2);
    assert_eq!(students[0].id, 1);
    assert_eq!(students[0].email, Some("jane@school.edu".to_string()));
    assert_eq!(students[1].id, 2);
    assert_eq!(students[1].email, None);
}

#[test]
fn test_model_size_optimization() {
    use std::mem::size_of;

    // Document sizes for performance awareness
    println!("Student size: {} bytes", size_of::<Student>());
    println!("School size: {} bytes", size_of::<School>());
    println!("Report size: {} bytes", size_of::<Report>());

    // These are reasonable sizes for our use case
    assert!(size_of::<Student>() < 200); // Should be compact
}

#[test]
fn test_optional_field_handling_consistency() {
    // Test that all models handle None values consistently
    let student = Student::new(1, "Test".to_string(), "10".to_string());
    let school = School::new(100, "School".to_string(), "Address".to_string());

    let student_json = serde_json::to_value(&student).unwrap();
    let school_json = serde_json::to_value(&school).unwrap();

    // None values should not appear in JSON
    assert!(!student_json.to_string().contains("null"));
    assert!(!school_json.to_string().contains("null"));
}
```

### Step 3.2: Run Integration Tests

```bash
# Run all tests including integration tests
cargo test

# Run only integration tests
cargo test --test model_integration_tests

# Expected output:
# running 5 tests
# test test_all_models_serialize_to_valid_json ... ok
# test test_model_size_optimization ... ok
# test test_models_deserialize_from_api_response ... ok
# test test_models_serialize_to_json_array ... ok
# test test_optional_field_handling_consistency ... ok
#
# test result: ok. 5 passed; 0 failed
```

---

## Phase 1 Validation Checklist

Before proceeding to Phase 2:

- [ ] All three models (Student, School, Report) implemented
- [ ] All unit tests pass (cargo test models)
- [ ] Integration tests pass (cargo test --test model_integration_tests)
- [ ] Serialization produces valid JSON
- [ ] Deserialization works with API-formatted JSON
- [ ] Optional fields excluded when None
- [ ] `cargo clippy` shows no warnings
- [ ] `cargo fmt` has formatted all code
- [ ] Documentation examples work (cargo test --doc)
- [ ] Models re-exported in mod.rs and lib.rs

---

# Phase 2: Error Handling Foundation

**Duration**: 2-3 days
**Goal**: Create comprehensive error types that integrate with Axum

## Day 9: Custom Error Types

### Step 1.1: Understand Error Handling in Rust

**Key Concepts**:
- Rust uses `Result<T, E>` instead of exceptions
- `?` operator propagates errors up the call stack
- Error types should implement `std::error::Error` trait
- `thiserror` crate automates Error trait implementation
- `anyhow` crate provides ergonomic error handling for applications

**Comparison to Python**:
```python
# Python
def get_data():
    try:
        return api_call()
    except RequestException as e:
        logger.error(f"API error: {e}")
        raise

# Rust
fn get_data() -> Result<Data> {
    let data = api_call()?;  // Propagates error if it occurs
    Ok(data)
}
```

### Step 1.2: Implement Error Types

**`src/error.rs`**:

```rust
//! Error types for the Aeries API
//!
//! This module defines all error types used throughout the application.
//! Errors are designed to integrate with Axum's error handling and provide
//! appropriate HTTP responses.

use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;
use thiserror::Error;

/// Main error type for the application
///
/// All errors in the application should be convertible to this type.
#[derive(Error, Debug)]
pub enum AppError {
    /// Configuration errors (missing env vars, invalid paths, etc.)
    #[error("Configuration error: {0}")]
    Config(String),

    /// Errors from the Aeries API client
    #[error("Aeries API error: {0}")]
    AeriesApi(#[from] reqwest::Error),

    /// JSON serialization/deserialization errors
    #[error("Serialization error: {0}")]
    Serialization(#[from] serde_json::Error),

    /// Export functionality errors (CSV, Excel, PDF)
    #[error("Export error: {0}")]
    Export(String),

    /// Resource not found (404)
    #[error("Not found: {0}")]
    NotFound(String),

    /// Invalid input from client
    #[error("Invalid input: {0}")]
    InvalidInput(String),

    /// Internal server error (catch-all)
    #[error("Internal server error")]
    Internal,
}

/// Implement conversion to HTTP response
///
/// This allows AppError to be returned directly from Axum handlers
impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, error_message) = match self {
            AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),

            AppError::InvalidInput(msg) => (StatusCode::BAD_REQUEST, msg),

            AppError::Config(msg) => {
                tracing::error!("Configuration error: {}", msg);
                (StatusCode::INTERNAL_SERVER_ERROR, "Configuration error".to_string())
            }

            AppError::AeriesApi(ref err) => {
                tracing::error!("Aeries API error: {:?}", err);
                // Don't leak internal details to client
                (StatusCode::BAD_GATEWAY, "External API error".to_string())
            }

            AppError::Export(msg) => {
                tracing::error!("Export error: {}", msg);
                (StatusCode::INTERNAL_SERVER_ERROR, msg)
            }

            AppError::Serialization(ref err) => {
                tracing::error!("Serialization error: {:?}", err);
                (StatusCode::INTERNAL_SERVER_ERROR, "Data format error".to_string())
            }

            AppError::Internal => {
                tracing::error!("Internal server error");
                (StatusCode::INTERNAL_SERVER_ERROR, "Internal error".to_string())
            }
        };

        let body = Json(json!({
            "error": error_message,
        }));

        (status, body).into_response()
    }
}

/// Type alias for Results using AppError
///
/// This allows writing `Result<T>` instead of `Result<T, AppError>`
pub type Result<T> = std::result::Result<T, AppError>;

#[cfg(test)]
mod tests {
    use super::*;
    use axum::http::StatusCode;

    #[test]
    fn test_config_error_creation() {
        let err = AppError::Config("Missing AERIES_BASE_URL".to_string());
        assert_eq!(err.to_string(), "Configuration error: Missing AERIES_BASE_URL");
    }

    #[test]
    fn test_not_found_error_creation() {
        let err = AppError::NotFound("Student with ID 123".to_string());
        assert_eq!(err.to_string(), "Not found: Student with ID 123");
    }

    #[test]
    fn test_export_error_creation() {
        let err = AppError::Export("Failed to write CSV".to_string());
        assert_eq!(err.to_string(), "Export error: Failed to write CSV");
    }

    #[tokio::test]
    async fn test_not_found_response() {
        let err = AppError::NotFound("Resource".to_string());
        let response = err.into_response();

        assert_eq!(response.status(), StatusCode::NOT_FOUND);
    }

    #[tokio::test]
    async fn test_invalid_input_response() {
        let err = AppError::InvalidInput("Invalid ID".to_string());
        let response = err.into_response();

        assert_eq!(response.status(), StatusCode::BAD_REQUEST);
    }

    #[tokio::test]
    async fn test_config_error_response() {
        let err = AppError::Config("Test config error".to_string());
        let response = err.into_response();

        assert_eq!(response.status(), StatusCode::INTERNAL_SERVER_ERROR);
    }

    #[test]
    fn test_error_from_serde_json() {
        // Test automatic conversion from serde_json::Error
        let invalid_json = "{ invalid json }";
        let result: std::result::Result<serde_json::Value, _> = serde_json::from_str(invalid_json);

        let err: AppError = result.unwrap_err().into();

        match err {
            AppError::Serialization(_) => {}, // Expected
            _ => panic!("Expected Serialization error"),
        }
    }

    #[test]
    fn test_result_type_alias() {
        // Verify that Result<T> alias works
        fn returns_result() -> Result<i32> {
            Ok(42)
        }

        fn returns_error() -> Result<i32> {
            Err(AppError::Internal)
        }

        assert!(returns_result().is_ok());
        assert!(returns_error().is_err());
    }

    #[test]
    fn test_error_propagation_with_question_mark() {
        fn inner_function() -> Result<String> {
            Err(AppError::NotFound("Inner error".to_string()))
        }

        fn outer_function() -> Result<String> {
            let _value = inner_function()?; // Propagates error
            Ok("Success".to_string())
        }

        let result = outer_function();
        assert!(result.is_err());

        match result.unwrap_err() {
            AppError::NotFound(msg) => assert_eq!(msg, "Inner error"),
            _ => panic!("Expected NotFound error"),
        }
    }
}
```

**Code Explanations**:

1. **`#[derive(Error, Debug)]`**:
   - `Error` from `thiserror` implements `std::error::Error` trait
   - Provides automatic implementation of `Display` trait

2. **`#[error("...")]`**:
   - Defines error message format
   - `{0}` is placeholder for tuple variant data

3. **`#[from]`**:
   - Automatic `From` trait implementation
   - Allows `?` operator to convert errors automatically

4. **`IntoResponse` trait**:
   - Allows returning `AppError` directly from Axum handlers
   - Converts errors to appropriate HTTP responses

5. **Type alias `Result<T>`**:
   - Ergonomic shorthand
   - Reduces boilerplate in function signatures

### Step 1.3: Update lib.rs

**`src/lib.rs`** (add error exports):

```rust
//! Aeries API Rust Backend

pub mod config;
pub mod error;
pub mod models;
pub mod clients;
pub mod services;
pub mod export;
pub mod handlers;
pub mod routes;

// Re-exports for convenience
pub use error::{AppError, Result};
pub use config::Config;
pub use models::{Student, School, Report};
```

### Step 1.4: Run Error Tests

```bash
# Run error tests
cargo test error

# Expected output:
# running 9 tests
# test error::tests::test_config_error_creation ... ok
# test error::tests::test_config_error_response ... ok
# test error::tests::test_error_from_serde_json ... ok
# test error::tests::test_error_propagation_with_question_mark ... ok
# test error::tests::test_export_error_creation ... ok
# test error::tests::test_invalid_input_response ... ok
# test error::tests::test_not_found_error_creation ... ok
# test error::tests::test_not_found_response ... ok
# test error::tests::test_result_type_alias ... ok

# Check that everything still compiles
cargo check
```

---

## Phase 2 Validation Checklist

Before proceeding to Phase 3:

- [ ] `AppError` enum implemented with all error variants
- [ ] `IntoResponse` trait implemented for Axum integration
- [ ] `Result<T>` type alias created
- [ ] Automatic conversion from `reqwest::Error` and `serde_json::Error`
- [ ] All error tests pass
- [ ] Error messages are user-friendly (no implementation details)
- [ ] Logging occurs for internal errors
- [ ] `cargo clippy` shows no warnings

---

# Phase 3: Configuration Management

**Duration**: 2-3 days
**Goal**: Implement robust configuration loading and validation

## Day 10-11: Configuration Implementation

### Step 1.1: Implement Configuration Module

**`src/config.rs`**:

```rust
//! Configuration management for the Aeries API
//!
//! This module handles loading and validating configuration from
//! environment variables.

use crate::error::{AppError, Result};
use std::path::PathBuf;

/// Application configuration
///
/// Configuration is loaded from environment variables.
/// See `.env.example` for all available options.
///
/// # Examples
///
/// ```no_run
/// use aeries_api_rust::Config;
///
/// # fn main() -> anyhow::Result<()> {
/// let config = Config::from_env()?;
/// println!("API URL: {}", config.aeries_base_url);
/// # Ok(())
/// # }
/// ```
#[derive(Debug, Clone)]
pub struct Config {
    /// Base URL for the Aeries API
    pub aeries_base_url: String,

    /// Path to the client certificate (.pem file)
    pub aeries_cert_path: PathBuf,

    /// Path to the private key file
    pub aeries_key_path: PathBuf,

    /// Server bind address (default: 0.0.0.0)
    pub server_host: String,

    /// Server port (default: 3000)
    pub server_port: u16,
}

impl Config {
    /// Load configuration from environment variables
    ///
    /// This method reads from a `.env` file if present, then reads from
    /// environment variables.
    ///
    /// # Errors
    ///
    /// Returns an error if:
    /// - Required environment variables are missing
    /// - Certificate or key files don't exist
    /// - Configuration values are invalid
    ///
    /// # Examples
    ///
    /// ```no_run
    /// # use aeries_api_rust::Config;
    /// # fn main() -> anyhow::Result<()> {
    /// let config = Config::from_env()?;
    /// # Ok(())
    /// # }
    /// ```
    pub fn from_env() -> Result<Self> {
        // Load .env file if present (doesn't error if missing)
        dotenvy::dotenv().ok();

        let config = Self {
            aeries_base_url: get_env_var("AERIES_BASE_URL")?,
            aeries_cert_path: get_env_path("AERIES_CERT_PATH")?,
            aeries_key_path: get_env_path("AERIES_KEY_PATH")?,
            server_host: std::env::var("SERVER_HOST")
                .unwrap_or_else(|_| default_host()),
            server_port: std::env::var("SERVER_PORT")
                .ok()
                .and_then(|s| s.parse().ok())
                .unwrap_or_else(default_port),
        };

        config.validate()?;
        Ok(config)
    }

    /// Validate the configuration
    ///
    /// Checks that file paths exist and values are sensible
    fn validate(&self) -> Result<()> {
        // Validate certificate path
        if !self.aeries_cert_path.exists() {
            return Err(AppError::Config(
                format!("Certificate file not found: {:?}", self.aeries_cert_path)
            ));
        }

        // Validate key path
        if !self.aeries_key_path.exists() {
            return Err(AppError::Config(
                format!("Private key file not found: {:?}", self.aeries_key_path)
            ));
        }

        // Validate URL format (basic check)
        if !self.aeries_base_url.starts_with("http://")
            && !self.aeries_base_url.starts_with("https://") {
            return Err(AppError::Config(
                "AERIES_BASE_URL must start with http:// or https://".to_string()
            ));
        }

        // Validate port range
        if self.server_port == 0 {
            return Err(AppError::Config(
                "SERVER_PORT must be greater than 0".to_string()
            ));
        }

        Ok(())
    }
}

/// Get a required environment variable
fn get_env_var(name: &str) -> Result<String> {
    std::env::var(name).map_err(|_| {
        AppError::Config(format!("Environment variable {} not set", name))
    })
}

/// Get a path from environment variable
fn get_env_path(name: &str) -> Result<PathBuf> {
    let path_str = get_env_var(name)?;
    Ok(PathBuf::from(path_str))
}

/// Default server host
fn default_host() -> String {
    "0.0.0.0".to_string()
}

/// Default server port
fn default_port() -> u16 {
    3000
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::env;
    use tempfile::NamedTempFile;

    /// Helper to set environment variables for tests
    struct TestEnv {
        vars: Vec<String>,
    }

    impl TestEnv {
        fn new() -> Self {
            Self { vars: Vec::new() }
        }

        fn set(&mut self, key: &str, value: &str) {
            env::set_var(key, value);
            self.vars.push(key.to_string());
        }
    }

    impl Drop for TestEnv {
        fn drop(&mut self) {
            for var in &self.vars {
                env::remove_var(var);
            }
        }
    }

    #[test]
    fn test_default_values() {
        assert_eq!(default_host(), "0.0.0.0");
        assert_eq!(default_port(), 3000);
    }

    #[test]
    fn test_config_from_env_missing_required() {
        let mut env = TestEnv::new();

        // Clear all required vars
        env::remove_var("AERIES_BASE_URL");
        env::remove_var("AERIES_CERT_PATH");
        env::remove_var("AERIES_KEY_PATH");

        let result = Config::from_env();
        assert!(result.is_err());
    }

    #[test]
    fn test_config_validation_invalid_url() {
        let mut env = TestEnv::new();

        // Create temporary files for cert and key
        let cert_file = NamedTempFile::new().unwrap();
        let key_file = NamedTempFile::new().unwrap();

        env.set("AERIES_BASE_URL", "not-a-url");
        env.set("AERIES_CERT_PATH", cert_file.path().to_str().unwrap());
        env.set("AERIES_KEY_PATH", key_file.path().to_str().unwrap());

        let result = Config::from_env();
        assert!(result.is_err());

        let err = result.unwrap_err();
        assert!(matches!(err, AppError::Config(_)));
    }

    #[test]
    fn test_config_validation_missing_cert_file() {
        let mut env = TestEnv::new();

        env.set("AERIES_BASE_URL", "https://example.com");
        env.set("AERIES_CERT_PATH", "/nonexistent/cert.pem");
        env.set("AERIES_KEY_PATH", "/nonexistent/key.pem");

        let result = Config::from_env();
        assert!(result.is_err());

        let err_msg = result.unwrap_err().to_string();
        assert!(err_msg.contains("Certificate file not found"));
    }

    #[test]
    fn test_config_with_valid_values() {
        let mut env = TestEnv::new();

        // Create temporary files
        let cert_file = NamedTempFile::new().unwrap();
        let key_file = NamedTempFile::new().unwrap();

        env.set("AERIES_BASE_URL", "https://example.com/api");
        env.set("AERIES_CERT_PATH", cert_file.path().to_str().unwrap());
        env.set("AERIES_KEY_PATH", key_file.path().to_str().unwrap());
        env.set("SERVER_HOST", "127.0.0.1");
        env.set("SERVER_PORT", "8080");

        let config = Config::from_env().unwrap();

        assert_eq!(config.aeries_base_url, "https://example.com/api");
        assert_eq!(config.server_host, "127.0.0.1");
        assert_eq!(config.server_port, 8080);
    }

    #[test]
    fn test_config_with_defaults() {
        let mut env = TestEnv::new();

        // Create temporary files
        let cert_file = NamedTempFile::new().unwrap();
        let key_file = NamedTempFile::new().unwrap();

        // Set only required vars
        env.set("AERIES_BASE_URL", "https://example.com");
        env.set("AERIES_CERT_PATH", cert_file.path().to_str().unwrap());
        env.set("AERIES_KEY_PATH", key_file.path().to_str().unwrap());

        // Don't set SERVER_HOST or SERVER_PORT

        let config = Config::from_env().unwrap();

        // Should use defaults
        assert_eq!(config.server_host, "0.0.0.0");
        assert_eq!(config.server_port, 3000);
    }

    #[test]
    fn test_config_invalid_port() {
        let mut env = TestEnv::new();

        let cert_file = NamedTempFile::new().unwrap();
        let key_file = NamedTempFile::new().unwrap();

        env.set("AERIES_BASE_URL", "https://example.com");
        env.set("AERIES_CERT_PATH", cert_file.path().to_str().unwrap());
        env.set("AERIES_KEY_PATH", key_file.path().to_str().unwrap());
        env.set("SERVER_PORT", "0");

        let result = Config::from_env();
        assert!(result.is_err());

        let err_msg = result.unwrap_err().to_string();
        assert!(err_msg.contains("SERVER_PORT must be greater than 0"));
    }

    #[test]
    fn test_config_clone() {
        let mut env = TestEnv::new();

        let cert_file = NamedTempFile::new().unwrap();
        let key_file = NamedTempFile::new().unwrap();

        env.set("AERIES_BASE_URL", "https://example.com");
        env.set("AERIES_CERT_PATH", cert_file.path().to_str().unwrap());
        env.set("AERIES_KEY_PATH", key_file.path().to_str().unwrap());

        let config = Config::from_env().unwrap();
        let cloned = config.clone();

        assert_eq!(config.aeries_base_url, cloned.aeries_base_url);
        assert_eq!(config.server_port, cloned.server_port);
    }
}
```

### Step 1.2: Update main.rs to Use Config

**`src/main.rs`** (updated):

```rust
use aeries_api_rust::{Config, routes};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize logging
    init_logging();

    tracing::info!("Starting Aeries API server...");

    // Load configuration
    let config = match Config::from_env() {
        Ok(cfg) => {
            tracing::info!("Configuration loaded successfully");
            cfg
        }
        Err(e) => {
            tracing::error!("Failed to load configuration: {}", e);
            return Err(e.into());
        }
    };

    tracing::debug!("Server will listen on {}:{}", config.server_host, config.server_port);

    // Build the application router
    let app = routes::create_placeholder_router();

    // Start the server
    let addr = format!("{}:{}", config.server_host, config.server_port);
    let listener = tokio::net::TcpListener::bind(&addr).await?;

    tracing::info!("Server listening on {}", addr);
    tracing::info!("Press Ctrl+C to stop");

    axum::serve(listener, app).await?;

    Ok(())
}

fn init_logging() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info,aeries_api_rust=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();
}
```

### Step 1.3: Create Test Certificates (for Development)

```bash
# Create certs directory
mkdir -p certs

# Generate self-signed certificate for testing
openssl req -x509 -newkey rsa:4096 -keyout certs/client-key.pem \
    -out certs/client-cert.pem -days 365 -nodes \
    -subj "/CN=localhost"

# Verify certificate
openssl x509 -in certs/client-cert.pem -text -noout

# Update .env with actual paths
cat >> .env << EOF
AERIES_BASE_URL=https://millercreeksd.aeries.net/admin/api/v5
AERIES_CERT_PATH=./certs/client-cert.pem
AERIES_KEY_PATH=./certs/client-key.pem
SERVER_HOST=127.0.0.1
SERVER_PORT=3000
RUST_LOG=debug
EOF
```

**Add certs to .gitignore**:
```bash
echo "certs/" >> .gitignore
```

### Step 1.4: Run Configuration Tests

```bash
# Run config tests
cargo test config

# Expected output:
# running 9 tests
# test config::tests::test_config_clone ... ok
# test config::tests::test_config_from_env_missing_required ... ok
# test config::tests::test_config_invalid_port ... ok
# test config::tests::test_config_validation_invalid_url ... ok
# test config::tests::test_config_validation_missing_cert_file ... ok
# test config::tests::test_config_with_defaults ... ok
# test config::tests::test_config_with_valid_values ... ok
# test config::tests::test_default_values ... ok

# Test the server with real config
cargo run

# Expected:
# Server should start successfully
# Check health endpoint: curl http://localhost:3000/health
```

---

## Phase 3 Validation Checklist

Before proceeding to Phase 4:

- [ ] `Config` struct implemented with all fields
- [ ] `from_env()` method loads from environment
- [ ] Configuration validation checks file existence
- [ ] Default values work for optional settings
- [ ] All config tests pass
- [ ] Server starts with valid configuration
- [ ] Server fails gracefully with invalid configuration
- [ ] Test certificates generated
- [ ] `.env` file configured with test values

---

# Foundation Validation Checklist

## Complete Phase 0-3 Validation

Before moving to Phase 4 (Aeries API Client), ensure **all** of the following are complete:

### Project Setup
- [ ] Rust 1.75+ installed and working
- [ ] Cargo commands execute successfully
- [ ] IDE/editor configured with Rust support
- [ ] Project directory structure created
- [ ] All module files created and properly declared

### Build & Run
- [ ] `cargo build` compiles without errors or warnings
- [ ] `cargo run` starts the server
- [ ] Server responds to `curl http://localhost:3000/health`
- [ ] `cargo watch -x run` auto-reloads on file changes

### Models (Phase 1)
- [ ] Student model implemented with tests
- [ ] School model implemented with tests
- [ ] Report model implemented with tests
- [ ] All model unit tests pass (19+ tests)
- [ ] Model integration tests pass (5+ tests)
- [ ] Serialization/deserialization works correctly
- [ ] Optional fields handled properly (excluded when None)

### Error Handling (Phase 2)
- [ ] `AppError` enum with all variants
- [ ] `Result<T>` type alias created
- [ ] `IntoResponse` trait implemented
- [ ] Automatic error conversion (`#[from]`) working
- [ ] All error tests pass (9+ tests)
- [ ] Error messages are user-friendly

### Configuration (Phase 3)
- [ ] `Config` struct implemented
- [ ] Environment variable loading works
- [ ] Configuration validation implemented
- [ ] Default values work correctly
- [ ] All config tests pass (9+ tests)
- [ ] Test certificates created
- [ ] `.env` file configured

### Code Quality
- [ ] `cargo clippy` shows no warnings
- [ ] `cargo fmt` has formatted all code
- [ ] All tests pass: `cargo test` (40+ tests total)
- [ ] Documentation examples work: `cargo test --doc`
- [ ] README.md is complete and accurate

### Git & Documentation
- [ ] Git repository initialized
- [ ] `.gitignore` configured
- [ ] Initial commits made
- [ ] README.md complete
- [ ] Code has documentation comments

---

## Next Steps

With the foundation complete, you're ready to proceed to:

- **Phase 4**: Aeries API Client (certificate-based HTTP client)
- **Phase 5**: HTTP Server & Endpoints (Axum handlers and routes)
- **Phase 6-8**: Export Functionality (CSV, Excel, PDF)

---

## Common Issues and Solutions

### Issue: Tests Fail with "no such file or directory"

**Solution**: Tests run in a different working directory. Use absolute paths or create temporary files in tests:

```rust
use tempfile::NamedTempFile;

let temp_file = NamedTempFile::new().unwrap();
let path = temp_file.path();
```

### Issue: "error: could not compile due to previous error"

**Solution**:
1. Read the error message carefully (Rust errors are helpful)
2. Run `cargo clean` then `cargo build` again
3. Check for missing module declarations in `mod.rs` files
4. Ensure all `use` statements are correct

### Issue: Server starts but doesn't respond to requests

**Solution**:
1. Check that port isn't blocked by firewall
2. Verify `SERVER_HOST` in `.env` (use `127.0.0.1` for local testing)
3. Check logs with `RUST_LOG=debug cargo run`
4. Test with `curl -v` for verbose output

### Issue: "environment variable not found"

**Solution**:
1. Verify `.env` file exists in project root
2. Check that `dotenvy::dotenv()` is called before reading env vars
3. For tests, use the `TestEnv` helper to set variables
4. Restart terminal/IDE after modifying `.env`

### Issue: Compile times are very slow

**Solution**:
1. Use `cargo check` during development (faster than `build`)
2. Enable incremental compilation (default in debug mode)
3. Consider using `sccache` for caching
4. First build is always slow; subsequent builds are much faster

---

## Summary

You've now completed the foundation phase! You have:

✅ A working Rust development environment
✅ Properly structured project with all modules
✅ Three fully-tested data models (Student, School, Report)
✅ Comprehensive error handling system
✅ Robust configuration management
✅ 40+ passing tests with high coverage
✅ Clean, formatted, and documented code
✅ A running HTTP server with health check

**Time to celebrate!** 🎉

This solid foundation will make the remaining phases significantly easier. The patterns you've established (error handling, testing, documentation) will be reused throughout the project.

When ready, proceed to the main migration plan document and begin **Phase 4: Aeries API Client**.
