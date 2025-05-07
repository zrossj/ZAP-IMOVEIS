with source as (
    SELECT * FROM {{source('zap_imo', 'silver_zapimoveis')}} 
),
rank_floorsize as (
	select 
	*, 
	case 
		when sz.floor_size <= 30
		then 'E'
		when sz.floor_size <= 60
		then 'D'
		when sz.floor_size <= 90
		then 'C'
		when sz.floor_size <= 120
		then 'B'
        WHEN sz.floor_size > 120
        THEN 'A'
	end as floor_size_rank
	from source sz 
)
select
*,
price_rent/floor_size as price_rent_per_m2
from rank_floorsize 
order by price_rent_per_m2