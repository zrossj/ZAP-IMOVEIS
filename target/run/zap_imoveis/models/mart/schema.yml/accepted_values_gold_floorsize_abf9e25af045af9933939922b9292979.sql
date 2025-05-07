select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    

with all_values as (

    select
        rank_floor_size as value_field,
        count(*) as n_records

    from "foo"."zap"."gold_floorsize_ranked_avg_prices"
    group by rank_floor_size

)

select *
from all_values
where value_field not in (
    'A','B','C','D','E'
)



      
    ) dbt_internal_test