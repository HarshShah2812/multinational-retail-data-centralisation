select sum(staff_numbers) total_staff_numbers,
case 
	when country_code = 'GB' then 'GB'
	when country_code = 'DE' then 'DE'
	when country_code = 'US' then 'US'
	else 'Web'
end as country_code
from dim_store_details 
group by country_code
order by total_staff_numbers desc;