output "raw_data_bucket_name" {
  description = "Name of the Cloud Storage bucket for raw data."
  value       = google_storage_bucket.raw_data_bucket.name
}

output "raw_dataset_id" {
  description = "BigQuery raw dataset ID."
  value       = google_bigquery_dataset.raw.dataset_id
}

output "analytics_dataset_id" {
  description = "BigQuery analytics dataset ID."
  value       = google_bigquery_dataset.analytics.dataset_id
}

output "dbt_service_account_email" {
  description = "Service account email used by dbt."
  value       = google_service_account.dbt_service_account.email
}