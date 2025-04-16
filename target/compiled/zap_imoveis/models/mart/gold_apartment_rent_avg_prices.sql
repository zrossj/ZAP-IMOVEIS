with source as (
    SELECT * FROM "foo"."zap"."silver_zapimoveis" 
    WHERE kind in ('Apartamentos à Venda', 'Apartamentos para Alugar')
),
final as (
	select 
	neighborhood,
	count(id) as sample_size,
	ROUND(avg(price_rent), 2) as price_rent_avg,
	ROUND(avg(price_condominium), 2) as price_condominium_avg,
	ROUND(avg(rent_plus_condo), 2) as rent_plus_condo_avg,
	ROUND(avg(price_rent) / avg(floor_size) , 2) as price_rent_per_m2_avg,
	ROUND(avg(rent_plus_condo) / avg(floor_size), 2) as rent_plus_condo__per_m2_avg,
	ROUND(avg(price_sale), 2) as price_sale_avg,
	ROUND(avg(price_sale) / avg(floor_size), 2) as price_sale_per_m2_avg
	from source 
	group by neighborhood 
)
select * from final 
order by price_rent_per_m2_avg desc