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
  default     = "chi-traffic-csv"
}

variable "gcs_storage_class" {
  description = "GCS storage class type"
  default     = "STANDARD"
}

variable "zone" {
  description = "GCE Instance zone"
  default     = "us-central1-c"
}

variable "svc_account" {
  description = "Service account ID"
  default     = "chi-pipeline"
}

variable "env_b64" {
  description = "Base64 encoded environment variables"
  type        = string
  sensitive   = true
}