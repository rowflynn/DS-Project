-- Contains all sql commands used in analysis
--NOTE Use of ChatGPT was utilized to help formulate some queries
select 
    count(admission_date) as total_admissions,
    sum(billing_amount) as total_billing,
    avg(billing_amount) as avg_billing,
    avg(discharge_date - admission_date) as avg_length_of_stay
from admissions a
where a.admission_date >= '2024-01-01'
  and a.admission_date < '2024-05-07';


select 
    count(admission_date) as total_admissions,
    sum(billing_amount) as total_billing,
    avg(billing_amount) as avg_billing,
    avg(discharge_date - admission_date) as avg_length_of_stay
from admissions a
where a.admission_date >= '2023-01-01'
  and a.admission_date < '2023-05-07';



create view monthly_admissions as
select
    extract(year from admission_date) as year,
    extract(month from admission_date) as month,
    count(*) as admissions
from admissions
where extract(year from admission_date) between 2020 and 2024
  and extract(month from admission_date) between 1 and 5
group by year, month
order by year, month;


select 
	month, 
	avg(admissions) as historic_average
from monthly_admissions
where year between 2020 and 2023
group by month
order by month;

select 
	month,
	admissions
from monthly_admissions
where year = 2024
order by month;


create view monthly_billing as
select
    extract(year from admission_date) as year,
    extract(month from admission_date) as month,
    sum(billing_amount) as total_billing
from admissions
where extract(year from admission_date) between 2020 and 2024
  and extract(month from admission_date) between 1 and 5
group by year, month
order by year, month;


select 
	month, 
	avg(total_billing) as historic_average
from monthly_billing
where year between 2020 and 2023
group by month
order by month;


select 
	month,
	total_billing
from monthly_billing
where year = 2024
order by month;

select admission_type, count(admission_type)
from admissions
group by admission_type;

select
    extract(month from admission_date) as month,
    count(*) as admissions
from admissions
where extract(year from admission_date) between 2020 and 2023
group by month
order by month;


select
    extract(month from admission_date) as month,
    count(*) as admissions
from admissions
where extract(year from admission_date) = 2024
group by month
order by month;

select count(*)
from admissions
where extract(year from admission_date) = 2023

select sum(billing_amount )
from admissions
where extract(year from admission_date) = 2023

select
    h.hospital_name,
    sum(a.billing_amount) as total_billing
from admissions a
join hospitals h
    on a.hospital_id = h.hospital_id
where extract(year from admission_date) = 2024
group by h.hospital_id, h.hospital_name
order by total_billing desc
limit 3;

select
    h.hospital_name,
    sum(a.billing_amount) as total_billing
from admissions a
join hospitals h
    on a.hospital_id = h.hospital_id
where extract(year from admission_date) = 2024
group by h.hospital_id, h.hospital_name
order by total_billing asc
limit 3;

select discharge_date-admission_date, billing_amount
from admissions
where extract(year from admission_date) = 2024
