## Helping Chicagoans Avoid Traffic Headaches

### The Everyday Struggle
If you've ever driven a car in Chicago you know how crazy traffic can be. To help drivers plan out commutes, I used traffic data from Chicago Data Portal to analyse traffic speeds in different regions throughout the Chicago area.  

---

### Dashboard
insert screenshot

#### "When Should I Leave?"  
**Hourly speed trends show:**  
- Best/worst times to drive through specific areas  

**Daily speed trends show:**  
- Best/worst days to drive through specific areas  

#### "Which Route is Faster?"  
**Regional speed comparisons reveal:**  
- Consistent bottlenecks
- Possible hidden shortcuts

---

### Traffic Analytics Pipeline Architecture

#### Overview
A batch processing data pipeline that transforms csv Chicago traffic API data into actionable insights for commuters.

```mermaid
graph TD
    A[Chicago Traffic API] -->|Python Script| B[GCS Bucket<br><small>Raw CSV Files</small>]
    B -->|dlt Pipeline| C[BigQuery<br><small>Staging Tables</small>]
    C -->|dbt Models| D[BigQuery<br><small>Analytics Tables</small>]
    D --> E[Looker Studio<br><small>Dashboards</small>]
    
    subgraph GCE VM
        F[Kestra Orchestrator]
        F -->|Triggers| A
        F -->|Manages| B
        F -->|Controls| C
        F -->|Schedules| D
    end

    style A fill:#2ecc71,stroke:#27ae60
    style B fill:#3498db,stroke:#2980b9
    style C fill:#9b59b6,stroke:#8e44ad
    style D fill:#e74c3c,stroke:#c0392b
    style E fill:#f39c12,stroke:#e67e22
    style F fill:#1abc9c,stroke:#16a085
```
#### Tech Stack

| Component              | Purpose                                                                 | Key Features Used                     |
|------------------------|-------------------------------------------------------------------------|---------------------------------------|
| **Google Compute Engine (GCE)** | Hosts pipeline execution environment                                  | - Docker container runtime for kestra            |
| **Kestra (Docker)**     | Workflow orchestration                                                 | - Scheduled job execution<br>- Dependency management |
| **Google Cloud Storage**     | Datalake                                               | - Destination for extracted csv files |
| **BigQuery**     | Data Warehouse                                              | - Tables/views for analytics  |
| **dlt**     | ETL                                             | - Extract data from GCS and load it into BigQuery  |
| **dbt**     | Transformations                                             | - Create fact/dimension tables for analytics  |
| **terraform**     | IaC Deployments                                             | - Ease redeployment of required cloud resources  |

---

