# 90-day-retention
## SQL pull referenced in data.csv
select
  if((datediff(subscription_cancel_date, subscription_creation_date) > 90
      or subscription_cancel_date is null), 0, 1) as 90_churn
, case
  when customer_locale = 0 then 'Domestic'
  when customer_locale = 1 then 'Foreign'
  end as customer_locale
, case
  when sales_lead = 0 then 'Unknown'
  when sales_lead = 1 then 'Organic'
  when sales_lead = 2 then 'Marketing'
  when sales_lead = 3 then 'Affiliate'
  end as sales_lead
, case
  when sales_channel = 0 then 'Unknown'
  when sales_channel = 1 then 'Online Web'
  when sales_channel = 2 then 'Sales Team'
  when sales_channel = 3 then 'Internal'
  end as sales_channel
, (initial_discount/(initial_discount + initial_cash_collected)) as discount
, product_display_name as product
, if(product_data_center = 1, 'EC','WC') as 'DC'
, case
    when onboarding_courtesy_call = 0 then 'Unknown'
    when onboarding_courtesy_call = 1 then 'Requested'
    when onboarding_courtesy_call = 2 then 'Declined'
    end as 'call_needed'
, case
    when onboarding_courtesy_call_result = 0 then 'Unknown'
    when onboarding_courtesy_call_result = 1 then 'Pending'
    when onboarding_courtesy_call_result = 2 then 'Completed'
    when onboarding_courtesy_call_result = 3 then 'Voicemail'
    when onboarding_courtesy_call_result = 4 then 'Declined'
    when onboarding_courtesy_call_result = 5 then 'Invalid'
    end as 'call_result'
, case
  when product_line = 0 then 'Other'
  when product_line = 1 then 'Business Class'
  when product_line = 2 then 'Reseller'
  when product_line = 3 then 'VPS'
  when product_line = 4 then 'Dedicated'
  when product_line = 5 then 'Hub'
  when product_line = 6 then 'Domains'
  when product_line = 7 then 'Design'
  when product_line = 8 then 'Managed Hosting'
  when product_line = 9 then 'Wordpress'
  when product_line = 10 then 'Cloud'
  end as product_line
, case
  when subscription_type = 0 then 'Additional'
  when subscription_type = 1 then 'Initial'
  when subscription_type = 2 then 'Modified'
  end as subscription_type
, subscription_30_day_contacts as 30_contacts
, subscription_60_day_contacts as 60_contacts
, subscription_90_day_contacts as 90_contacts
from
  OBI.subscription_snapshots
where
  brand = 1
  and account_type = 0
  and product_type = 1
  and subscription_type != 2
  and subscription_status in(2, 3, 4, 6)
  and modification_id is null
  and subscription_age >= 90
  and subscription_creation_date > '2017-01-01';
####The above SQL is to be cleansed and stored in the project file in a '.csv' file
