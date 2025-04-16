with source as (
    SELECT * FROM {{source('zap_imo', 'silver_zapimoveis')}} 
),
rank_floorsize as (
	select 
	*, 
	case 
		when sz.floor_size > 20 and sz.floor_size <= 50
		then 'C'
		when sz.floor_size > 50 and sz.floor_size <= 80
		then 'B'
		when sz.floor_size > 80 and sz.floor_size <= 110
		then 'A'
        WHEN sz.floor_size > 110
        THEN 'S'
	end as floor_size_rank
	from source sz 
)
select
*,
price_rent/floor_size as price_rent_per_m2
from rank_floorsize 
order by price_rent_per_m2