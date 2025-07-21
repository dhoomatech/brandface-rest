from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Metric, Dimension, RunReportRequest
from google.oauth2 import service_account

# Path to your service account key
KEY_PATH = "ga_credentials.json"
PROPERTY_ID = "YOUR-GA4-PROPERTY-ID"

credentials = service_account.Credentials.from_service_account_file(KEY_PATH)

client = BetaAnalyticsDataClient(credentials=credentials)

request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[Dimension(name="country"), Dimension(name="browser")],
    metrics=[Metric(name="activeUsers")],
    date_ranges=[DateRange(start_date="7daysAgo", end_date="today")]
)

response = client.run_report(request)

# Print rows
for row in response.rows:
    print([dimension_value.value for dimension_value in row.dimension_values],
          [metric_value.value for metric_value in row.metric_values])
