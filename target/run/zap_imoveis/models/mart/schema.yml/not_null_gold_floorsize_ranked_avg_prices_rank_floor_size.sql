select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
    



select rank_floor_size
from "foo"."zap"."gold_floorsize_ranked_avg_prices"
where rank_floor_size is null



      
    ) dbt_internal_test