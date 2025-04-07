terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.25.0"
    }
  }
}

provider "google" {
  # credentials = file(var.credentials) # uncomment if using credential file
  project = var.project
  region  = var.region
}

# Add permissions to service account
resource "google_project_iam_member" "setup_svc_account" {
  for_each = toset([
    "roles/storage.admin",
    "roles/bigquery.admin",
    "roles/run.admin"
  ])
  project = var.project
  role    = each.value
  member  = "serviceAccount:${var.svc_account}@${var.project}.iam.gserviceaccount.com"
}

# Create GCS bucket
resource "google_storage_bucket" "chi-traffic-bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  force_destroy = true
}

# Create BQ dataset
resource "google_bigquery_dataset" "chi-traffic-dataset" {
  dataset_id = var.bq_dataset_name
  location   = var.location
}

# Create firewall to access Kestra
resource "google_compute_firewall" "allow-https" {
  project     = var.project
  name        = "allow-https"
  network     = "default"
  description = "Creates firewall rule allowing https targeting tagged instances"

  allow {
    protocol = "tcp"
    ports    = ["443", "8080"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["https-server"]
}

# Create Kestra VM
resource "google_compute_instance" "kestra_vm" {
  name         = "kestra-server"
  machine_type = "n2-standard-4"
  zone         = var.zone

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2204-jammy-v20250305"
      size  = 10
    }
  }

  tags = ["https-server"]

  network_interface {
    network = "default"
    access_config {} # Enables external IP
  }

  metadata = {
    file_b64    = file(var.creds)
  }

  metadata_startup_script = <<-EOT
    #!/bin/bash
    sudo apt update && sudo apt install -y docker.io docker-compose curl

    # Enable and start Docker
    sudo systemctl start docker
    sudo systemctl enable docker

    sudo mkdir -p /home/kestra
    cd /home/kestra

    sudo curl -s -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/attributes/file_b64 | base64 --decode > creds.json
    sudo chmod 644 creds.json

    # Download docker files for kestra
    sudo curl -o docker-compose.yml https://raw.githubusercontent.com/alepanti/ChiTrafficInsights/refs/heads/main/kestra/docker-compose.yml
    sudo curl -o Dockerfile https://raw.githubusercontent.com/alepanti/ChiTrafficInsights/refs/heads/main/kestra/Dockerfile

    # Run Kestra
    sudo docker-compose up -d
  EOT
}
