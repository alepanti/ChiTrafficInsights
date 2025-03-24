variable "location" {
  description = "Project location"
  default     = "US"
}

variable "region" {
  description = "Project region"
  default     = "us-central1"
}

variable "project" {
  description = "Project ID"
  default     = "chicago-traffic-453615"
}

variable "bq_dataset_name" {
  description = "BiqQuery Dataset Name"
  default     = "chi_traffic"
}

variable "gcs_bucket_name" {
  description = "Google Cloud Storage bucket name"
  default     = "chi-traffic-json"
}

variable "gcs_storage_class" {
  description = "GCS storage class type"
  default     = "STANDARD"
}

variable "credentials" {
  # Path to Google credential file
  description = "My Google Creds"
  default     = "./keys/creds.json"
}

variable "zone" {
  description = "GCE Instance zone"
  default     = "us-central1-c"
}

variable "svc_account" {
  description = "Service account ID"
  default     = "chi-pipeline"
}

variable "dlt_repo" {
  description = "Repo name/ID for dlt service"
  default     = "dlt-repo"
}

variable "pipeline" {
  description = "dlt pipeline name"
  default     = "dlt-chi-traffic-pipeline"
}

variable "dlt_dockerfile_path" {
  description = "Path to dlt dockerfile"
  default     = "/home/realadmin/ChiTrafficInsights/dlt" # CHANGE to path of dlt Dockerfile
}