# Python to Rust Migration Plan: Aeries API Backend

## High-Level Summary

This migration plan provides a phased, incremental approach for refactoring the Aeries API Python backend into idiomatic, performant Rust. The strategy follows a **bottom-up refactoring pattern**, starting with data models and core services, then building up to HTTP endpoints and export functionality.

### Core Philosophy
- **Incremental Progress**: Each phase is independently testable and deployable
- **Solo Developer Focused**: Phases are designed for 1-2 weeks of focused work
- **Pragmatic Stack Choices**: Balance between learning curve and production-readiness
- **Parallel Deployment**: Run Python and Rust versions side-by-side during migration

### Recommended Rust Stack
- **Web Framework**: **Axum** (recommended for modern async patterns, excellent ergonomics, backed by Tokio team)
- **Async Runtime**: **Tokio** (industry standard, comprehensive ecosystem)
- **HTTP Client**: **reqwest** (feature-rich, async-first, TLS support)
- **Serialization**: **serde** with **serde_json** (de facto standard)
- **Error Handling**: **anyhow** for applications, **thiserror** for libraries
- **Configuration**: **dotenvy** (environment variables), **config** crate
- **CSV Export**: **csv** crate
- **Excel Export**: **rust_xlsxwriter** or **calamine**
- **PDF Export**: **printpdf** or **genpdf**
- **Logging**: **tracing** with **tracing-subscriber** (structured logging)
- **Testing**: Built-in **cargo test** + **wiremock** for HTTP mocking

---

## Current Python Architecture Analysis

### Application Structure
```
AeriesAPI/
├── src/
│   ├── models/           # Data models (Student, School, Report)
│   ├── services/         # Business logic layer
│   │   ├── aeries_service.py       # Core API client (certificate auth)
│   │   ├── students_service.py     # Student endpoint logic
│   │   ├── schools_service.py      # School endpoint logic
│   │   ├── reports_service.py      # Report endpoint logic
│   │   ├── formatting_service.py   # Data transformation
│   │   └── export_service.py       # CSV/Excel/PDF export
│   └── cli/              # Click-based CLI commands
├── tests/                # Three-layer test suite
│   ├── unit/            # Service and model tests
│   ├── contract/        # API contract validation
│   └── integration/     # Export pipeline tests
├── APIfunctions.py       # Legacy functions (direct DB + API access)
└── main.py              # Legacy entry point
```

### Key Components

**1. Data Models** (`src/models/`)
- Python `@dataclass` objects: `Student`, `School`, `Report`
- Methods: `to_dict()`, `from_dict(cls, data)`
- Fields use `Optional[T]` for nullable values

**2. AeriesService** (`src/services/aeries_service.py`)
- Core API client with certificate-based authentication
- Methods: `get_students()`, `get_schools()`, `get_reports()`
- Environment-based configuration: `AERIES_BASE_URL`, `AERIES_CERT_PATH`, `AERIES_KEY_PATH`
- Uses `requests` library with `cert=(cert_path, key_path)`

**3. Domain Services**
- Thin wrappers around `AeriesService`
- Convert model objects to dictionaries
- Handle export format selection

**4. Export Service**
- CSV: Python `csv.DictWriter`
- Excel: `pandas` + `openpyxl`
- PDF: `reportlab` (basic text rendering)

**5. Legacy Code** (`APIfunctions.py`)
- Direct database access via `pymssql`
- Complex data transformations with pandas
- Hardcoded credentials (security issue to address)
- School demographics, test scores, attendance calculations

### Dependencies
```
requests==2.31.0
pandas==2.2.0
pymssql==2.2.8
pytest==7.4.3
openpyxl==3.1.2
reportlab==4.0.7
```

### Missing Components
- No web server/API endpoints (CLI-only currently)
- No authentication/authorization layer
- No rate limiting or caching
- Limited error recovery mechanisms

---

## Proposed Rust Architecture & Stack

### Recommended Web Framework: Axum

**Why Axum?**
- Modern, ergonomic API built on Tower middleware
- Excellent type safety with compile-time guarantees
- Strong integration with Tokio ecosystem
- Lower learning curve than Actix Web
- Active development backed by Tokio team
- Great documentation and community support

**Alternatives Considered:**
- **Actix Web**: More mature, slightly better performance, but more complex actor model
- **Rocket**: Simpler syntax, but requires nightly Rust (deal-breaker for production)

### Core Libraries

| Purpose | Crate | Version | Justification |
|---------|-------|---------|---------------|
| HTTP Server | `axum` | 0.7 | Modern async patterns, excellent ergonomics |
| Async Runtime | `tokio` | 1.35 | Industry standard, required by Axum |
| HTTP Client | `reqwest` | 0.11 | Feature-rich, TLS/certificate support |
| Serialization | `serde`, `serde_json` | 1.0 | De facto standard for Rust |
| Error Handling | `anyhow`, `thiserror` | 1.0 | Anyhow for apps, thiserror for custom errors |
| Configuration | `dotenvy`, `config` | Latest | Environment variables + structured config |
| CSV Export | `csv` | 1.3 | Lightweight, fast CSV writer |
| Excel Export | `rust_xlsxwriter` | 0.60 | Pure Rust, no Excel runtime needed |
| PDF Export | `printpdf` | 0.7 | Pure Rust PDF generation |
| Logging | `tracing`, `tracing-subscriber` | 0.1 | Structured logging, async-aware |
| Testing (HTTP) | `axum-test` or `tower::ServiceExt` | Latest | Request/response testing |
| Testing (Mocking) | `wiremock` | 0.6 | HTTP mocking for external APIs |

### Proposed Project Structure

```
aeries-api-rust/
├── Cargo.toml                    # Workspace configuration
├── .env.example                  # Environment template
├── src/
│   ├── main.rs                   # Application entry point
│   ├── lib.rs                    # Library root (for testing)
│   ├── config.rs                 # Configuration management
│   ├── error.rs                  # Custom error types
│   │
│   ├── models/                   # Domain models
│   │   ├── mod.rs
│   │   ├── student.rs
│   │   ├── school.rs
│   │   └── report.rs
│   │
│   ├── clients/                  # External API clients
│   │   ├── mod.rs
│   │   └── aeries.rs             # Aeries API client
│   │
│   ├── services/                 # Business logic
│   │   ├── mod.rs
│   │   ├── students.rs
│   │   ├── schools.rs
│   │   └── reports.rs
│   │
│   ├── export/                   # Export functionality
│   │   ├── mod.rs
│   │   ├── csv.rs
│   │   ├── excel.rs
│   │   └── pdf.rs
│   │
│   ├── handlers/                 # HTTP request handlers
│   │   ├── mod.rs
│   │   ├── students.rs
│   │   ├── schools.rs
│   │   └── reports.rs
│   │
│   └── routes.rs                 # Route definitions
│
├── tests/                        # Integration tests
│   ├── common/
│   │   └── mod.rs                # Shared test utilities
│   ├── api_tests.rs              # API endpoint tests
│   ├── export_tests.rs           # Export functionality tests
│   └── contract_tests.rs         # Contract validation
│
└── benches/                      # Performance benchmarks (optional)
    └── api_benchmark.rs
```

---

## Phased Migration Plan for Solo Developer

### Phase 0: Preparation & Environment Setup (3-5 days)

**Goal**: Set up Rust development environment and project scaffolding.

**Steps**:
1. **Install Rust toolchain**:
   ```bash
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   rustup default stable
   ```

2. **Create new Cargo project**:
   ```bash
   cargo new --lib aeries-api-rust
   cd aeries-api-rust
   ```

3. **Initialize Cargo.toml** with core dependencies:
   ```toml
   [package]
   name = "aeries-api-rust"
   version = "0.1.0"
   edition = "2021"

   [dependencies]
   # HTTP Server
   axum = "0.7"
   tokio = { version = "1.35", features = ["full"] }
   tower = "0.4"
   tower-http = { version = "0.5", features = ["trace"] }

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
   config = "0.14"

   # Logging
   tracing = "0.1"
   tracing-subscriber = { version = "0.3", features = ["env-filter"] }

   [dev-dependencies]
   wiremock = "0.6"
   ```

4. **Create directory structure** as outlined above

5. **Set up `.env.example`**:
   ```
   AERIES_BASE_URL=https://your-aeries-instance.com
   AERIES_CERT_PATH=/path/to/certificate.pem
   AERIES_KEY_PATH=/path/to/private-key.pem
   RUST_LOG=info,aeries_api_rust=debug
   ```

6. **Configure logging in `main.rs`**:
   ```rust
   use tracing_subscriber;

   #[tokio::main]
   async fn main() {
       tracing_subscriber::fmt()
           .with_env_filter("info,aeries_api_rust=debug")
           .init();

       tracing::info!("Starting Aeries API server...");
   }
   ```

**Definition of Done**:
- ✅ Rust toolchain installed and `cargo --version` works
- ✅ Project compiles with `cargo build`
- ✅ Basic logging displays with `cargo run`
- ✅ `.env` file loads successfully

---

### Phase 1: Core Data Models (3-5 days)

**Goal**: Translate Python `@dataclass` models to Rust structs with serialization.

**Steps**:

1. **Create `src/models/mod.rs`**:
   ```rust
   pub mod student;
   pub mod school;
   pub mod report;
   ```

2. **Implement `Student` model** (`src/models/student.rs`):
   ```rust
   use serde::{Deserialize, Serialize};

   #[derive(Debug, Clone, Serialize, Deserialize)]
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
   }
   ```

3. **Implement `School` model** (`src/models/school.rs`):
   ```rust
   use serde::{Deserialize, Serialize};

   #[derive(Debug, Clone, Serialize, Deserialize)]
   pub struct School {
       pub id: i64,
       pub name: String,
       pub address: String,
       #[serde(skip_serializing_if = "Option::is_none")]
       pub phone: Option<String>,
   }
   ```

4. **Implement `Report` model** (`src/models/report.rs`):
   ```rust
   use serde::{Deserialize, Serialize};

   #[derive(Debug, Clone, Serialize, Deserialize)]
   pub struct Report {
       pub id: i64,
       pub name: String,
       pub description: String,
       #[serde(rename = "type")]
       pub report_type: String,
   }
   ```

5. **Write unit tests** for each model:
   ```rust
   #[cfg(test)]
   mod tests {
       use super::*;

       #[test]
       fn test_student_serialization() {
           let student = Student::new(1, "John Doe".to_string(), "10".to_string());
           let json = serde_json::to_string(&student).unwrap();
           assert!(json.contains("\"id\":1"));
           assert!(json.contains("\"name\":\"John Doe\""));
       }

       #[test]
       fn test_student_deserialization() {
           let json = r#"{"id":1,"name":"Jane Doe","grade":"11"}"#;
           let student: Student = serde_json::from_str(json).unwrap();
           assert_eq!(student.id, 1);
           assert_eq!(student.name, "Jane Doe");
       }
   }
   ```

**Definition of Done**:
- ✅ All three models compile without warnings
- ✅ Models serialize to JSON matching Python output
- ✅ Models deserialize from JSON successfully
- ✅ Unit tests pass: `cargo test models`
- ✅ Optional fields handled correctly (excluded from JSON when `None`)

---

### Phase 2: Error Handling Foundation (2-3 days)

**Goal**: Create robust error types for API and business logic errors.

**Steps**:

1. **Create `src/error.rs`**:
   ```rust
   use axum::{
       http::StatusCode,
       response::{IntoResponse, Response},
       Json,
   };
   use serde_json::json;
   use thiserror::Error;

   #[derive(Error, Debug)]
   pub enum AppError {
       #[error("Configuration error: {0}")]
       Config(String),

       #[error("Aeries API error: {0}")]
       AeriesApi(#[from] reqwest::Error),

       #[error("Serialization error: {0}")]
       Serialization(#[from] serde_json::Error),

       #[error("Export error: {0}")]
       Export(String),

       #[error("Not found: {0}")]
       NotFound(String),

       #[error("Internal server error")]
       Internal,
   }

   impl IntoResponse for AppError {
       fn into_response(self) -> Response {
           let (status, error_message) = match self {
               AppError::NotFound(msg) => (StatusCode::NOT_FOUND, msg),
               AppError::Config(msg) => (StatusCode::INTERNAL_SERVER_ERROR, msg),
               AppError::AeriesApi(err) => {
                   tracing::error!("Aeries API error: {:?}", err);
                   (StatusCode::BAD_GATEWAY, "External API error".to_string())
               }
               AppError::Export(msg) => (StatusCode::INTERNAL_SERVER_ERROR, msg),
               AppError::Serialization(err) => {
                   tracing::error!("Serialization error: {:?}", err);
                   (StatusCode::INTERNAL_SERVER_ERROR, "Data format error".to_string())
               }
               AppError::Internal => {
                   (StatusCode::INTERNAL_SERVER_ERROR, "Internal error".to_string())
               }
           };

           let body = Json(json!({
               "error": error_message,
           }));

           (status, body).into_response()
       }
   }

   pub type Result<T> = std::result::Result<T, AppError>;
   ```

2. **Add to `src/lib.rs`**:
   ```rust
   pub mod error;
   pub mod models;

   pub use error::{AppError, Result};
   ```

**Definition of Done**:
- ✅ Error types compile and integrate with Axum
- ✅ Errors convert to appropriate HTTP status codes
- ✅ Error messages are user-friendly (no implementation details leaked)

---

### Phase 3: Configuration Management (2-3 days)

**Goal**: Load and validate configuration from environment variables.

**Steps**:

1. **Create `src/config.rs`**:
   ```rust
   use crate::error::{AppError, Result};
   use serde::Deserialize;
   use std::path::PathBuf;

   #[derive(Debug, Clone, Deserialize)]
   pub struct Config {
       pub aeries_base_url: String,
       pub aeries_cert_path: PathBuf,
       pub aeries_key_path: PathBuf,
       #[serde(default = "default_port")]
       pub server_port: u16,
       #[serde(default = "default_host")]
       pub server_host: String,
   }

   fn default_port() -> u16 {
       3000
   }

   fn default_host() -> String {
       "0.0.0.0".to_string()
   }

   impl Config {
       pub fn from_env() -> Result<Self> {
           dotenvy::dotenv().ok();

           let config = Self {
               aeries_base_url: std::env::var("AERIES_BASE_URL")
                   .map_err(|_| AppError::Config("AERIES_BASE_URL not set".into()))?,
               aeries_cert_path: std::env::var("AERIES_CERT_PATH")
                   .map_err(|_| AppError::Config("AERIES_CERT_PATH not set".into()))?
                   .into(),
               aeries_key_path: std::env::var("AERIES_KEY_PATH")
                   .map_err(|_| AppError::Config("AERIES_KEY_PATH not set".into()))?
                   .into(),
               server_port: std::env::var("SERVER_PORT")
                   .ok()
                   .and_then(|s| s.parse().ok())
                   .unwrap_or_else(default_port),
               server_host: std::env::var("SERVER_HOST")
                   .unwrap_or_else(|_| default_host()),
           };

           config.validate()?;
           Ok(config)
       }

       fn validate(&self) -> Result<()> {
           if !self.aeries_cert_path.exists() {
               return Err(AppError::Config(
                   format!("Certificate not found: {:?}", self.aeries_cert_path)
               ));
           }
           if !self.aeries_key_path.exists() {
               return Err(AppError::Config(
                   format!("Private key not found: {:?}", self.aeries_key_path)
               ));
           }
           Ok(())
       }
   }
   ```

2. **Add tests**:
   ```rust
   #[cfg(test)]
   mod tests {
       use super::*;

       #[test]
       fn test_default_values() {
           assert_eq!(default_port(), 3000);
           assert_eq!(default_host(), "0.0.0.0");
       }
   }
   ```

**Definition of Done**:
- ✅ Configuration loads from environment variables
- ✅ Missing required variables return clear errors
- ✅ File paths are validated to exist
- ✅ Default values apply for optional settings

---

### Phase 4: Aeries API Client (5-7 days)

**Goal**: Replicate `AeriesService` functionality with certificate-based auth.

**Steps**:

1. **Create `src/clients/mod.rs`**:
   ```rust
   pub mod aeries;
   ```

2. **Implement `src/clients/aeries.rs`**:
   ```rust
   use crate::{
       config::Config,
       error::{AppError, Result},
       models::{Student, School, Report},
   };
   use reqwest::{Certificate, Client, Identity};
   use std::fs;
   use tracing::{info, error};

   #[derive(Clone)]
   pub struct AeriesClient {
       client: Client,
       base_url: String,
   }

   impl AeriesClient {
       pub fn new(config: &Config) -> Result<Self> {
           // Read certificate and key
           let cert_pem = fs::read(&config.aeries_cert_path)
               .map_err(|e| AppError::Config(
                   format!("Failed to read certificate: {}", e)
               ))?;
           let key_pem = fs::read(&config.aeries_key_path)
               .map_err(|e| AppError::Config(
                   format!("Failed to read private key: {}", e)
               ))?;

           // Combine cert and key for reqwest Identity
           let mut pem = cert_pem.clone();
           pem.extend_from_slice(&key_pem);

           let identity = Identity::from_pem(&pem)
               .map_err(|e| AppError::Config(
                   format!("Failed to create identity: {}", e)
               ))?;

           let client = Client::builder()
               .identity(identity)
               .build()
               .map_err(|e| AppError::Config(
                   format!("Failed to build HTTP client: {}", e)
               ))?;

           Ok(Self {
               client,
               base_url: config.aeries_base_url.clone(),
           })
       }

       pub async fn get_students(&self) -> Result<Vec<Student>> {
           let url = format!("{}/students", self.base_url);
           info!("Making request to {}", url);

           let response = self.client
               .get(&url)
               .send()
               .await?;

           if !response.status().is_success() {
               error!("API request failed: {}", response.status());
               return Err(AppError::AeriesApi(
                   response.error_for_status().unwrap_err()
               ));
           }

           let students: Vec<Student> = response.json().await?;
           info!("Successfully retrieved {} students", students.len());
           Ok(students)
       }

       pub async fn get_schools(&self) -> Result<Vec<School>> {
           let url = format!("{}/schools", self.base_url);
           info!("Making request to {}", url);

           let response = self.client
               .get(&url)
               .send()
               .await?;

           response.error_for_status_ref()?;
           let schools: Vec<School> = response.json().await?;
           info!("Successfully retrieved {} schools", schools.len());
           Ok(schools)
       }

       pub async fn get_reports(&self) -> Result<Vec<Report>> {
           let url = format!("{}/reports", self.base_url);
           info!("Making request to {}", url);

           let response = self.client
               .get(&url)
               .send()
               .await?;

           response.error_for_status_ref()?;
           let reports: Vec<Report> = response.json().await?;
           info!("Successfully retrieved {} reports", reports.len());
           Ok(reports)
       }
   }
   ```

3. **Write integration tests** with `wiremock`:
   ```rust
   #[cfg(test)]
   mod tests {
       use super::*;
       use wiremock::{MockServer, Mock, ResponseTemplate};
       use wiremock::matchers::{method, path};

       #[tokio::test]
       async fn test_get_students_success() {
           let mock_server = MockServer::start().await;

           let mock_students = vec![
               serde_json::json!({
                   "id": 1,
                   "name": "John Doe",
                   "grade": "10"
               })
           ];

           Mock::given(method("GET"))
               .and(path("/students"))
               .respond_with(ResponseTemplate::new(200).set_body_json(&mock_students))
               .mount(&mock_server)
               .await;

           // Test implementation
           // Note: This requires adjusting AeriesClient to accept base_url
       }
   }
   ```

**Definition of Done**:
- ✅ Client successfully loads certificate and key
- ✅ All three methods (`get_students`, `get_schools`, `get_reports`) implemented
- ✅ Errors are properly propagated and logged
- ✅ Mock tests pass for happy path
- ✅ Manual test against real Aeries API succeeds (if possible)

---

### Phase 5: HTTP Server & Basic Endpoints (5-7 days)

**Goal**: Create Axum server with GET endpoints for students, schools, and reports.

**Steps**:

1. **Create `src/handlers/mod.rs`**:
   ```rust
   pub mod students;
   pub mod schools;
   pub mod reports;
   ```

2. **Implement `src/handlers/students.rs`**:
   ```rust
   use crate::{
       clients::aeries::AeriesClient,
       error::Result,
       models::Student,
   };
   use axum::{extract::State, Json};
   use std::sync::Arc;

   pub async fn get_students(
       State(client): State<Arc<AeriesClient>>,
   ) -> Result<Json<Vec<Student>>> {
       let students = client.get_students().await?;
       Ok(Json(students))
   }
   ```

3. **Create `src/routes.rs`**:
   ```rust
   use crate::{
       clients::aeries::AeriesClient,
       handlers::{students, schools, reports},
   };
   use axum::{routing::get, Router};
   use std::sync::Arc;
   use tower_http::trace::TraceLayer;

   pub fn create_router(client: Arc<AeriesClient>) -> Router {
       Router::new()
           .route("/students", get(students::get_students))
           .route("/schools", get(schools::get_schools))
           .route("/reports", get(reports::get_reports))
           .layer(TraceLayer::new_for_http())
           .with_state(client)
   }
   ```

4. **Update `src/main.rs`**:
   ```rust
   mod clients;
   mod config;
   mod error;
   mod handlers;
   mod models;
   mod routes;

   use crate::{
       clients::aeries::AeriesClient,
       config::Config,
       routes::create_router,
   };
   use std::sync::Arc;
   use tracing_subscriber;

   #[tokio::main]
   async fn main() -> anyhow::Result<()> {
       tracing_subscriber::fmt()
           .with_env_filter("info,aeries_api_rust=debug")
           .init();

       let config = Config::from_env()?;
       let client = Arc::new(AeriesClient::new(&config)?);
       let app = create_router(client);

       let addr = format!("{}:{}", config.server_host, config.server_port);
       let listener = tokio::net::TcpListener::bind(&addr).await?;
       tracing::info!("Server listening on {}", addr);

       axum::serve(listener, app).await?;
       Ok(())
   }
   ```

5. **Test with curl or Postman**:
   ```bash
   cargo run
   # In another terminal:
   curl http://localhost:3000/students
   ```

**Definition of Done**:
- ✅ Server starts without errors
- ✅ GET `/students` returns JSON array
- ✅ GET `/schools` returns JSON array
- ✅ GET `/reports` returns JSON array
- ✅ Errors return appropriate HTTP status codes
- ✅ Logs show request traces

---

### Phase 6: CSV Export Functionality (3-4 days)

**Goal**: Implement CSV export matching Python's `export_service.py`.

**Steps**:

1. **Add dependency to `Cargo.toml`**:
   ```toml
   csv = "1.3"
   ```

2. **Create `src/export/mod.rs`**:
   ```rust
   pub mod csv;
   pub mod excel;
   pub mod pdf;

   pub use self::csv::export_to_csv;
   ```

3. **Implement `src/export/csv.rs`**:
   ```rust
   use crate::error::{AppError, Result};
   use serde::Serialize;
   use std::io::Write;

   pub fn export_to_csv<T: Serialize>(data: &[T]) -> Result<String> {
       let mut wtr = csv::Writer::from_writer(vec![]);

       for record in data {
           wtr.serialize(record)
               .map_err(|e| AppError::Export(format!("CSV serialization failed: {}", e)))?;
       }

       let bytes = wtr.into_inner()
           .map_err(|e| AppError::Export(format!("CSV write failed: {}", e)))?;

       String::from_utf8(bytes)
           .map_err(|e| AppError::Export(format!("CSV UTF-8 conversion failed: {}", e)))
   }
   ```

4. **Add handler for CSV export**:
   ```rust
   // In src/handlers/students.rs
   use axum::{
       extract::State,
       response::{IntoResponse, Response},
       http::{header, StatusCode},
   };

   pub async fn export_students_csv(
       State(client): State<Arc<AeriesClient>>,
   ) -> Result<Response> {
       let students = client.get_students().await?;
       let csv_data = crate::export::export_to_csv(&students)?;

       Ok((
           StatusCode::OK,
           [(header::CONTENT_TYPE, "text/csv")],
           csv_data,
       ).into_response())
   }
   ```

5. **Add route**:
   ```rust
   .route("/students/export/csv", get(students::export_students_csv))
   ```

**Definition of Done**:
- ✅ CSV export produces valid CSV format
- ✅ GET `/students/export/csv` returns downloadable CSV
- ✅ CSV output matches Python version (column order, formatting)
- ✅ Empty data handled gracefully

---

### Phase 7: Excel Export Functionality (4-5 days)

**Goal**: Implement Excel export using `rust_xlsxwriter`.

**Steps**:

1. **Add dependency**:
   ```toml
   rust_xlsxwriter = "0.60"
   ```

2. **Implement `src/export/excel.rs`**:
   ```rust
   use crate::error::{AppError, Result};
   use rust_xlsxwriter::{Workbook, Worksheet, Format};
   use serde::Serialize;
   use serde_json;

   pub fn export_to_excel<T: Serialize>(data: &[T]) -> Result<Vec<u8>> {
       let mut workbook = Workbook::new();
       let worksheet = workbook.add_worksheet();

       if data.is_empty() {
           return Ok(workbook.save_to_buffer()
               .map_err(|e| AppError::Export(format!("Excel save failed: {}", e)))?);
       }

       // Convert to JSON then to Vec<Map> for flexible column extraction
       let json_data = serde_json::to_value(data)
           .map_err(|e| AppError::Export(format!("JSON conversion failed: {}", e)))?;
       let rows = json_data.as_array()
           .ok_or_else(|| AppError::Export("Invalid data structure".into()))?;

       // Write headers
       if let Some(first_row) = rows.first() {
           if let Some(obj) = first_row.as_object() {
               for (col, (key, _)) in obj.iter().enumerate() {
                   worksheet.write_string(0, col as u16, key)
                       .map_err(|e| AppError::Export(format!("Write header failed: {}", e)))?;
               }
           }
       }

       // Write data rows
       for (row_idx, row) in rows.iter().enumerate() {
           if let Some(obj) = row.as_object() {
               for (col_idx, (_, value)) in obj.iter().enumerate() {
                   let value_str = match value {
                       serde_json::Value::String(s) => s.clone(),
                       serde_json::Value::Number(n) => n.to_string(),
                       serde_json::Value::Bool(b) => b.to_string(),
                       serde_json::Value::Null => String::new(),
                       _ => value.to_string(),
                   };
                   worksheet.write_string((row_idx + 1) as u32, col_idx as u16, &value_str)
                       .map_err(|e| AppError::Export(format!("Write cell failed: {}", e)))?;
               }
           }
       }

       workbook.save_to_buffer()
           .map_err(|e| AppError::Export(format!("Excel save failed: {}", e)))
   }
   ```

3. **Add handler**:
   ```rust
   pub async fn export_students_excel(
       State(client): State<Arc<AeriesClient>>,
   ) -> Result<Response> {
       let students = client.get_students().await?;
       let excel_data = crate::export::excel::export_to_excel(&students)?;

       Ok((
           StatusCode::OK,
           [(
               header::CONTENT_TYPE,
               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
           )],
           excel_data,
       ).into_response())
   }
   ```

**Definition of Done**:
- ✅ Excel file opens in Microsoft Excel/LibreOffice
- ✅ Column headers match field names
- ✅ Data is properly formatted
- ✅ GET `/students/export/excel` downloads valid `.xlsx` file

---

### Phase 8: PDF Export Functionality (4-5 days)

**Goal**: Implement basic PDF export (text-based, matching Python's simple approach).

**Steps**:

1. **Add dependency**:
   ```toml
   printpdf = "0.7"
   ```

2. **Implement `src/export/pdf.rs`**:
   ```rust
   use crate::error::{AppError, Result};
   use printpdf::*;
   use serde::Serialize;
   use serde_json;

   pub fn export_to_pdf<T: Serialize>(data: &[T]) -> Result<Vec<u8>> {
       let (doc, page1, layer1) = PdfDocument::new(
           "Aeries Report",
           Mm(210.0),
           Mm(297.0),
           "Layer 1",
       );

       let font = doc.add_builtin_font(BuiltinFont::Helvetica)
           .map_err(|e| AppError::Export(format!("Font loading failed: {}", e)))?;

       let current_layer = doc.get_page(page1).get_layer(layer1);

       let json_data = serde_json::to_value(data)
           .map_err(|e| AppError::Export(format!("JSON conversion failed: {}", e)))?;
       let rows = json_data.as_array()
           .ok_or_else(|| AppError::Export("Invalid data structure".into()))?;

       let mut y_position = 280.0; // Start from top

       for row in rows {
           if let Some(obj) = row.as_object() {
               for (key, value) in obj.iter() {
                   let text = format!("{}: {}", key, value);
                   current_layer.use_text(
                       text,
                       12.0,
                       Mm(10.0),
                       Mm(y_position),
                       &font,
                   );
                   y_position -= 5.0;
               }
               y_position -= 5.0; // Extra space between records

               if y_position < 20.0 {
                   // Would need to add new page here for production use
                   break;
               }
           }
       }

       let bytes = doc.save_to_bytes()
           .map_err(|e| AppError::Export(format!("PDF save failed: {}", e)))?;

       Ok(bytes)
   }
   ```

3. **Add handler** (similar pattern to Excel)

**Definition of Done**:
- ✅ PDF opens in PDF viewers
- ✅ Text is readable and properly formatted
- ✅ GET `/students/export/pdf` downloads valid PDF

---

### Phase 9: Integration Tests & Contract Validation (5-7 days)

**Goal**: Port Python test suite to Rust.

**Steps**:

1. **Create `tests/common/mod.rs`**:
   ```rust
   use wiremock::MockServer;

   pub async fn setup_mock_server() -> MockServer {
       MockServer::start().await
   }
   ```

2. **Create `tests/api_tests.rs`**:
   ```rust
   use axum::http::{Request, StatusCode};
   use tower::ServiceExt;
   use aeries_api_rust::routes::create_router;

   #[tokio::test]
   async fn test_get_students_endpoint() {
       // Test implementation
   }
   ```

3. **Port contract tests** from `tests/contract/` in Python

4. **Port integration tests** for export functionality

**Definition of Done**:
- ✅ All ported tests pass
- ✅ Contract tests validate JSON schema
- ✅ Integration tests cover full request/response cycle
- ✅ `cargo test` runs all tests successfully

---

### Phase 10: CLI Tool (Optional, 3-4 days)

**Goal**: Create CLI tool matching Python's Click-based interface.

**Steps**:

1. **Add dependency**:
   ```toml
   clap = { version = "4.5", features = ["derive"] }
   ```

2. **Create `src/bin/aeries-cli.rs`**:
   ```rust
   use clap::{Parser, Subcommand};
   use aeries_api_rust::{
       clients::aeries::AeriesClient,
       config::Config,
       export,
   };
   use std::fs;

   #[derive(Parser)]
   #[command(name = "aeries-cli")]
   #[command(about = "Aeries API CLI tool", long_about = None)]
   struct Cli {
       #[command(subcommand)]
       command: Commands,
   }

   #[derive(Subcommand)]
   enum Commands {
       Export {
           #[arg(value_enum)]
           resource: Resource,
           #[arg(value_enum)]
           format: Format,
           #[arg(short, long, default_value = "output")]
           output: String,
       },
   }

   #[derive(Clone, clap::ValueEnum)]
   enum Resource {
       Students,
       Schools,
       Reports,
   }

   #[derive(Clone, clap::ValueEnum)]
   enum Format {
       Csv,
       Excel,
       Pdf,
   }

   #[tokio::main]
   async fn main() -> anyhow::Result<()> {
       let cli = Cli::parse();
       let config = Config::from_env()?;
       let client = AeriesClient::new(&config)?;

       match cli.command {
           Commands::Export { resource, format, output } => {
               // Implementation
           }
       }

       Ok(())
   }
   ```

**Definition of Done**:
- ✅ CLI compiles and runs
- ✅ `aeries-cli export students csv --output students` works
- ✅ All format combinations functional

---

### Phase 11: Performance Optimization & Production Readiness (3-5 days)

**Goal**: Optimize for production deployment.

**Steps**:

1. **Add connection pooling** (if direct DB access needed later)
2. **Implement request timeout handling**:
   ```rust
   let client = Client::builder()
       .identity(identity)
       .timeout(std::time::Duration::from_secs(30))
       .build()?;
   ```

3. **Add structured logging with request IDs**:
   ```rust
   use tower_http::trace::TraceLayer;
   use uuid::Uuid;

   // Add request ID middleware
   ```

4. **Create Dockerfile**:
   ```dockerfile
   FROM rust:1.75 as builder
   WORKDIR /app
   COPY . .
   RUN cargo build --release

   FROM debian:bookworm-slim
   RUN apt-get update && apt-get install -y libssl3 ca-certificates
   COPY --from=builder /app/target/release/aeries-api-rust /usr/local/bin/
   CMD ["aeries-api-rust"]
   ```

5. **Add health check endpoint**:
   ```rust
   .route("/health", get(|| async { "OK" }))
   ```

6. **Performance benchmarking**:
   ```bash
   # Using Apache Bench
   ab -n 1000 -c 10 http://localhost:3000/students
   ```

**Definition of Done**:
- ✅ Application runs in Docker container
- ✅ Health check endpoint responds
- ✅ Request timeouts configured
- ✅ Performance meets or exceeds Python version

---

### Phase 12: Legacy Code Migration (`APIfunctions.py`) (7-10 days)

**Goal**: Migrate complex business logic from legacy script.

**Steps**:

1. **Add database dependencies**:
   ```toml
   sqlx = { version = "0.7", features = ["runtime-tokio-native-tls", "mssql"] }
   ```

2. **Create `src/db/mod.rs`** for direct database access
3. **Port `flatten_json` function**
4. **Port demographic calculations**
5. **Port test score aggregations**

**Note**: This phase is complex due to extensive pandas usage. Consider:
- Breaking into smaller sub-phases
- Using `polars` crate (Rust DataFrame library) if heavy data manipulation needed
- Potentially keeping Python for complex analytics, expose as microservice

**Definition of Done**:
- ✅ Core functions ported and tested
- ✅ Database queries execute successfully
- ✅ Output matches Python version

---

## Data Model & Database Interaction Strategy

### Translation Pattern: Python → Rust

| Python | Rust |
|--------|------|
| `@dataclass` | `#[derive(Serialize, Deserialize)]` struct |
| `Optional[T]` | `Option<T>` |
| `List[T]` | `Vec<T>` |
| `Dict[str, Any]` | `HashMap<String, Value>` or custom struct |
| `from_dict(cls, data)` | `serde_json::from_value()` |
| `to_dict(self)` | `serde_json::to_value()` |

### Database Access

For direct database access (from `APIfunctions.py`):

1. **Use SQLx** for type-safe SQL:
   ```rust
   let pool = sqlx::mssql::MssqlPoolOptions::new()
       .max_connections(5)
       .connect(&database_url)
       .await?;
   ```

2. **Create repository pattern**:
   ```rust
   pub struct StudentRepository {
       pool: sqlx::MssqlPool,
   }

   impl StudentRepository {
       pub async fn get_demographics(&self, school_code: i32) -> Result<Vec<StudentDemo>> {
           sqlx::query_as!(
               StudentDemo,
               "SELECT StudentID, Grade, Gender FROM STU WHERE SC = ?",
               school_code
           )
           .fetch_all(&self.pool)
           .await
           .map_err(Into::into)
       }
   }
   ```

---

## Testing Strategy

### Three-Layer Approach (Matching Python)

1. **Unit Tests**:
   ```rust
   #[cfg(test)]
   mod tests {
       use super::*;

       #[test]
       fn test_student_creation() {
           // Test model logic
       }
   }
   ```

2. **Integration Tests** (`tests/` directory):
   ```rust
   #[tokio::test]
   async fn test_students_endpoint() {
       let app = create_test_app();
       let response = app
           .oneshot(Request::builder().uri("/students").body(Body::empty()).unwrap())
           .await
           .unwrap();
       assert_eq!(response.status(), StatusCode::OK);
   }
   ```

3. **Contract Tests** (using JSON schemas):
   ```rust
   use jsonschema::JSONSchema;

   #[tokio::test]
   async fn test_student_schema() {
       let schema = load_schema("tests/contracts/students.yaml");
       let response = get_students().await;
       assert!(schema.is_valid(&response));
   }
   ```

### Tools
- **Mock HTTP**: `wiremock` crate
- **Assertions**: Built-in `assert!` + `pretty_assertions` crate
- **Coverage**: `cargo-tarpaulin`
- **Test fixtures**: `rstest` crate

---

## Potential Challenges & Mitigation

### Challenge 1: Rust Learning Curve

**Symptoms**: Compiler errors, ownership/borrowing confusion, lifetime annotations

**Mitigation**:
- Read "The Rust Programming Language" (free online book) chapters 1-10 before starting
- Use `clippy` (Rust linter): `cargo clippy` for helpful suggestions
- Start with Phase 1 (models) which has minimal complexity
- Use `Arc<T>` for shared state instead of wrestling with lifetimes initially
- Ask on Rust Discord/Forum when stuck (very friendly community)

### Challenge 2: Async Rust Complexity

**Symptoms**: `Send` trait errors, `'static` lifetime issues, tokio runtime confusion

**Mitigation**:
- Stick to Axum patterns (state with `Arc<T>`)
- Use `#[tokio::main]` macro (hides runtime complexity)
- Avoid mixing async and sync code
- Use `tokio::spawn` for background tasks
- Reference: [Tokio tutorial](https://tokio.rs/tokio/tutorial)

### Challenge 3: Certificate Authentication

**Symptoms**: TLS errors, certificate format issues, connection refused

**Mitigation**:
- Test certificate loading in isolation first (Phase 4)
- Use `openssl` command to verify certificate format:
  ```bash
  openssl x509 -in cert.pem -text -noout
  ```
- Check reqwest examples for TLS configuration
- Fall back to Python's `requests` approach if needed

### Challenge 4: Export Library Parity

**Symptoms**: Missing features in Rust libraries vs pandas/reportlab

**Mitigation**:
- Accept simpler export formats initially (CSV is easy, PDF may be basic)
- Use `rust_xlsxwriter` which is feature-rich for Excel
- Consider keeping Python microservice for complex PDF generation
- Prioritize CSV export (Phase 6) to validate architecture

### Challenge 5: Pandas Replacement

**Symptoms**: Complex data transformations in `APIfunctions.py` hard to port

**Mitigation**:
- Use `polars` crate (Rust DataFrame library, similar API to pandas)
- Break transformations into smaller functions
- Write comprehensive tests before porting
- Consider keeping Python analytics layer, expose via API

### Challenge 6: Error Handling Differences

**Symptoms**: Rust's `Result<T, E>` feels verbose compared to Python exceptions

**Mitigation**:
- Use `?` operator liberally (auto-propagates errors)
- Define custom `Result` type alias: `type Result<T> = std::result::Result<T, AppError>`
- Use `anyhow` for quick prototyping, refine to `thiserror` later
- Embrace compile-time error checking (prevents runtime surprises)

### Challenge 7: Performance Expectations

**Symptoms**: Rust code not significantly faster than Python

**Mitigation**:
- Profile first: `cargo flamegraph`
- Network I/O is bottleneck (not CPU), so gains may be modest
- Focus on memory efficiency and concurrency over raw speed
- Use `cargo build --release` (optimized builds are 10x+ faster than debug)

---

## Final Checklist

### Pre-Migration
- [ ] Rust toolchain installed
- [ ] Python codebase documented and tested
- [ ] Certificate/key files accessible
- [ ] Development environment configured

### Phase Completion
- [ ] **Phase 0**: Project setup complete
- [ ] **Phase 1**: Data models implemented and tested
- [ ] **Phase 2**: Error handling in place
- [ ] **Phase 3**: Configuration loading works
- [ ] **Phase 4**: Aeries API client functional
- [ ] **Phase 5**: HTTP server running with basic endpoints
- [ ] **Phase 6**: CSV export working
- [ ] **Phase 7**: Excel export working
- [ ] **Phase 8**: PDF export working
- [ ] **Phase 9**: Test suite ported and passing
- [ ] **Phase 10**: CLI tool complete (optional)
- [ ] **Phase 11**: Production-ready optimizations
- [ ] **Phase 12**: Legacy code migrated

### Production Deployment
- [ ] Docker image builds successfully
- [ ] Health check endpoint responds
- [ ] Environment variables configured
- [ ] Certificates deployed securely
- [ ] Monitoring/logging configured
- [ ] Performance benchmarks meet requirements
- [ ] Documentation updated

### Post-Migration
- [ ] Python codebase archived
- [ ] Team trained on Rust codebase
- [ ] Deployment playbook documented
- [ ] Runbook for common issues created

---

## Recommended Resources

### Books
- *The Rust Programming Language* (free: https://doc.rust-lang.org/book/)
- *Rust for Rustaceans* by Jon Gjengset (advanced)

### Async Rust
- Tokio Tutorial: https://tokio.rs/tokio/tutorial
- Async Book: https://rust-lang.github.io/async-book/

### Web Development
- Axum Examples: https://github.com/tokio-rs/axum/tree/main/examples
- Tower Middleware: https://docs.rs/tower/

### Community
- Rust Users Forum: https://users.rust-lang.org/
- Rust Discord: https://discord.gg/rust-lang
- r/rust: https://reddit.com/r/rust

---

## Timeline Estimate

Assuming 20-30 hours/week of focused development:

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 0 | 3-5 days | 1 week |
| Phase 1 | 3-5 days | 2 weeks |
| Phase 2 | 2-3 days | 2.5 weeks |
| Phase 3 | 2-3 days | 3 weeks |
| Phase 4 | 5-7 days | 4.5 weeks |
| Phase 5 | 5-7 days | 6 weeks |
| Phase 6 | 3-4 days | 6.5 weeks |
| Phase 7 | 4-5 days | 7.5 weeks |
| Phase 8 | 4-5 days | 8.5 weeks |
| Phase 9 | 5-7 days | 10 weeks |
| Phase 10 (optional) | 3-4 days | 10.5 weeks |
| Phase 11 | 3-5 days | 11 weeks |
| Phase 12 | 7-10 days | 13 weeks |

**Total Estimated Duration**: **12-14 weeks** (3-3.5 months) for complete migration

---

## Conclusion

This migration plan provides a structured, incremental approach to refactoring the Aeries API from Python to Rust. By following the phases sequentially, you'll build a solid foundation and maintain working software at each step. The Rust version will offer improved performance, better error handling, and stronger compile-time guarantees while preserving the functionality of the Python implementation.

Remember: **Incremental progress is more important than perfection.** Complete each phase, validate with tests, and move forward. Good luck with your migration!
