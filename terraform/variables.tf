variable "project_id" {
  description = "GCP project ID."
  type        = string
}

variable "region" {
  description = "Default GCP region."
  type        = string
  default     = "europe-west1"
}

variable "location" {
  description = "BigQuery and Cloud Storage location."
  type        = string
  default     = "EU"
}

variable "gcs_bucket_name" {
  description = "Cloud Storage bucket name for raw data."
  type        = string
}

variable "raw_dataset_id" {
  description = "BigQuery raw dataset ID."
  type        = string
  default     = "commerceflow_raw"
}

variable "analytics_dataset_id" {
  description = "BigQuery analytics dataset ID."
  type        = string
  default     = "commerceflow_analytics"
}

variable "dbt_service_account_id" {
  description = "Service account ID used by dbt."
  type        = string
  default     = "commerceflow-dbt"
}

variable "credentials_file" {
  description = "Path to the GCP service account key file."
  type        = string
}